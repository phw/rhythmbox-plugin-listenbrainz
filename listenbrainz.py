# Copyright (c) 2018 Philipp Wolfer <ph.wolfer@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from listenbrainz_client import ListenBrainzClient, Track
from listenbrainz_settings import ListenBrainzSettings
from listenbrainz_utils import debug, load_settings


class ListenBrainzPlugin(GObject.Object, Peas.Activatable):
    __gtype_name = 'ListenBrainzPlugin'
    object = GObject.property(type=GObject.GObject)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = load_settings()
        self.__client = ListenBrainzClient()
        self.settings.connect("changed::user-token",
                              self.on_user_token_changed)
        self.on_user_token_changed(self.settings)
        self.__current_entry = None
        self.__current_start_time = 0
        self.__current_elapsed = 0

    def do_activate(self):
        debug("activating ListenBrainz plugin")

        shell = self.object
        shell.props.shell_player.connect("playing-song-changed",
                                         self.on_playing_song_changed)
        shell.props.shell_player.connect("elapsed-changed",
                                         self.on_elapsed_changed)

    def do_deactivate(self):
        debug("deactivating ListenBrainz plugin")

    def on_playing_song_changed(self, player, entry):
        debug("playing-song-changed: %r, %r" % (player, entry))

        if self.__current_entry is not None:
            duration = self.__current_entry.get_ulong(
                            RB.RhythmDBPropType.DURATION)
            elapsed = self.__current_elapsed
            debug("Elapsed: %s / %s" % (elapsed, duration))
            if elapsed >= 240 or elapsed >= duration / 2:
                track = self.__entry_to_track(self.__current_entry)
                self.__client.listen(self.__current_start_time, track)

        self.__current_entry = entry
        self.__current_elapsed = 0

        if entry is None:
            return

        self.__current_start_time = int(time.time())
        track = self.__entry_to_track(entry)
        self.__client.playing_now(track)

    def on_elapsed_changed(self, player, elapsed):
        # debug("elapsed-changed: %r, %i" % (player, elapsed))
        if player.get_playing_entry() == self.__current_entry:
            self.__current_elapsed += 1

    def on_user_token_changed(self, settings, key="user-token"):
        self.__client.user_token = settings.get_string("user-token")

    def __entry_to_track(self, entry):
        artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
        title = entry.get_string(RB.RhythmDBPropType.TITLE)
        album = entry.get_string(RB.RhythmDBPropType.ALBUM)
        track_number = entry.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)
        mb_track_id = entry.get_string(RB.RhythmDBPropType.MB_TRACKID)
        mb_album_id = entry.get_string(RB.RhythmDBPropType.MB_ALBUMID)
        mb_artist_id = entry.get_string(RB.RhythmDBPropType.MB_ARTISTID)
        additional_info = {
            "release_mbid": mb_album_id,
            "recording_mbid": mb_track_id,
            "artist_mbids": [mb_artist_id],
            "tracknumber": track_number
        }
        return Track(artist, title, album, additional_info)


GObject.type_register(ListenBrainzSettings)
