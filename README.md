# ListenBrainz plugin for Rhythmbox

Listen to the Rhythm! Submit your listens to [ListenBrainz](https://listenbrainz.org).

## User install

Copy the `listenbrainz` directory and all included files to
`$HOME/.local/share/rhythmbox/plugins/` and run:

    glib-compile-schemas $HOME/.local/share/rhythmbox/plugins/listenbrainz/schema

Launch Rhythmbox and activate the ListenBrainz plugin. You also have to
configure your [ListenBrainz user token](https://listenbrainz.org/profile/)
in the plugin settings.

## System wide install

You can perform a system wide install using meson:

    meson --prefix=/usr builddir
    cd builddir
    ninja install
    sudo glib-compile-schemas /usr/share/glib-2.0/schemas
    
