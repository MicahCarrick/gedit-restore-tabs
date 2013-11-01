import os
from gi.repository import GObject, GLib, Gtk, Gio, Gedit

SETTINGS_SCHEMA = "org.gnome.gedit.plugins.restoretabs"

class RestoreTabsWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "RestoreTabsWindowActivatable"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._handlers = []
    
    def do_activate(self):
        """
        Connect signal handlers.
        """
        handlers = []
        handler_id = self.window.connect("delete-event", 
                                         self.on_window_delete_event)                             
        self._handlers.append(handler_id)
        
        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        uris = settings.get_value('uris')
        if uris:
            # temporary handler to catch the first time a window is shown
            self._temp_handler = self.window.connect("show", self.on_window_show, uris)

    def do_deactivate(self):
        """
        Disconect any signal handlers that were added in do_activate().
        """
        [self.window.disconnect(handler_id) for handler_id in self._handlers]
    
    def do_update_state(self):
        pass
        
    def is_first_window(self):
        """
        Return True if the window being added is the first window instance.
        """
        app = Gedit.App.get_default()
        if len(app.get_windows()) <= 1:
            return True
        else:
            return False

    def on_window_delete_event(self, window, event, data=None):
        uris = []
        for document in window.get_documents():
            gfile = document.get_location()
            if gfile:
                uris.append(gfile.get_uri())
        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        settings.set_value('uris', GLib.Variant("as", uris))
        return False
    
    def on_window_show(self, window, uris):
        """
        Only restore tabs if this window is the first Gedit window instance.
        """
        self.window.disconnect(self._temp_handler)
        self._temp_handler = None
        if self.is_first_window():
            active_tab = self.window.get_active_tab()
            # in gedit <= 3.6, tabs are added before the window is shown
            # in gedit >= 3.8, tabs are added after
            if active_tab:
                self.on_tab_added(window, active_tab)
            for uri in uris:
                location = Gio.file_new_for_uri(uri)
                tab = self.window.get_tab_from_location(location)
                if not tab:
                    self.window.create_tab_from_location(location, None, 0, 
                                                         0, False, True)
            if not active_tab:
                self._temp_handler = window.connect("tab-added", self.on_tab_added)

    def on_tab_added(self, window, tab):
        """
        Close the first tab if it is empty.
        """
        if tab.get_state() == Gedit.TabState.STATE_NORMAL and tab.get_document().is_untouched():
            (GLib if hasattr(GLib, "idle_add") else GObject).idle_add(window.close_tab, tab)
        if self._temp_handler is not None:
            window.disconnect(self._temp_handler)
            self._temp_handler = None

