# Install the Tabs Rertore GEdit plugin.
# Written by Hildo Guillardi Júnior.
# Distributed by GNU General Propose License 3.0.

#git clone git://github.com/hildogjr/gedit-restore-tabs.git

echo 'Creating the plugin folder...'
mkdir $HOME/.local/share/gedit/plugins/ -p # Create the directories recursively.

echo 'Installing the files...'
cp restoretabs.* $HOME/.local/share/gedit/plugins/ # Copy: py, icon and plugin configuration.
sudo cp org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-*/schemas/

echo 'Updating Linux register...'
#sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
sudo glib-compile-schemas /usr/share/glib-*/schemas/
