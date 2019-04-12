# Rhythmbox ListenBrainz Changelog

## 1.2.1 - 2019-04-12
Properly close file handle when reading / saving queue cache.

## 1.2 - 2019-02-19
Submit listens for all sources played, not only local files. Only podcasts and
unidentified audio CD tracks are ignored.

## 1.1 - 2019-02-19
Restructured file layout. The `rhythmbox.plugin` file is now located inside the
`listenbrainz` directory. This simplifies the install procedure a bit:

Copy the `listenbrainz` directory and all included files to
`$HOME/.local/share/rhythmbox/plugins/` and run:

    glib-compile-schemas $HOME/.local/share/rhythmbox/plugins/listenbrainz/schema

## 1.0 - 2018-08-23

Initial release
