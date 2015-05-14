Gedit Restore Tabs
==================

This is a plugin for [Gedit][2], the official text editor of the GNOME desktop
environment. This plugin is for Gedit versions 3 and above. **This plugin is NOT
compatible with Gedit 2.x**.

Upon starting Gedit, this plugin will try restore all open documents from the 
*last* Gedit window that was closed.


Installation
------------

1. Download the source code form this repository or using the `git clone` command.
2. Copy the files to the Gedit plugins directory `~/.local/share/gedit/plugins/`.
3. Copy and compile the settings schema **as root**.
4. Restart Gedit.
5. Activate the plugin in the Gedit preferences dialog.

### For Example...

    git clone git://github.com/Quixotix/gedit-restore-tabs.git
    mkdir -p ~/.local/share/gedit/plugins/
    cp gedit-restore-tabs/restoretabs.* ~/.local/share/gedit/plugins/
    
**With root access** (`su` or `sudo`)...
    
    cp gedit-restore-tabs/org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-2.0/schemas/
    glib-compile-schemas /usr/share/glib-2.0/schemas/


[2]: http://www.gedit.org



