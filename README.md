# ListenBrainz plugin for Rhythmbox

Listen to the Rhythm! Submit your listens to [ListenBrainz](https://listenbrainz.org).

## Installation

**Note:** This plugin is bundled in Rhythmbox 3.4.4 or later. If you are using an earlier version of Rhythmbox please see below on how to install this plugin.

### Distribution packages

#### Ubuntu

A Ubuntu package is available in the [MusicBrainz PPA](https://launchpad.net/~musicbrainz-developers/+archive/ubuntu/stable).
Install it with:

    sudo add-apt-repository ppa:musicbrainz-developers/stable
    sudo apt-get update
    sudo apt-get install rhythmbox-plugin-listenbrainz

### User install

You can easily install the plugin just for your user. Copy the `listenbrainz`
directory and all included files to `$HOME/.local/share/rhythmbox/plugins/`
and run:

    glib-compile-schemas $HOME/.local/share/rhythmbox/plugins/listenbrainz/schema

Launch Rhythmbox and activate the ListenBrainz plugin. You also have to
configure your [ListenBrainz user token](https://listenbrainz.org/profile/)
in the plugin settings.

### System wide install

You can perform a system wide install using meson:

    meson --prefix=/usr builddir
    cd builddir
    ninja install
    sudo glib-compile-schemas /usr/share/glib-2.0/schemas

## Usage

You need to signup for [ListenBrainz](https://listenbrainz.org) in order to use
this service. Once you have setup your account get your personal *user token*
on your [ListenBrainz profile page](https://listenbrainz.org/profile/).

Open the Plugins dialog in Rhythmbox, select the ListenBrainz plugin and open
the plugin's preferences. Copy and paste your ListenBrainz user token into the
dialog.

Now all songs you listen to in Rhythmbox will be sent to ListenBrainz. You can
see your listen history on ListenBrainz by clicking on "My Listens".
