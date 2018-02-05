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

import logging
import sys
import time
from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from .listenbrainz import ListenBrainzClient, Track
from .settings import ListenBrainzSettings, load_settings

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ListenBrainzPlugin(GObject.Object, Peas.Activatable):
    __gtype_name = 'ListenBrainzPlugin'
    object = GObject.property(type=GObject.GObject)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = None
        self.__client = None
        self.__current_entry = None
        self.__current_start_time = 0
        self.__current_elapsed = 0

    def do_activate(self):
        self.settings = load_settings()
        self.__client = ListenBrainzClient()
        self.settings.connect("changed::user-token",
                              self.on_user_token_changed)
        self.on_user_token_changed(self.settings)
        self.__current_entry = None
        self.__current_start_time = 0
        self.__current_elapsed = 0
        shell_player = self.object.props.shell_player
        shell_player.connect("playing-song-changed",
                             self.on_playing_song_changed)
        shell_player.connect("elapsed-changed", self.on_elapsed_changed)

    def do_deactivate(self):
        shell_player = self.object.props.shell_player
        shell_player.disconnect_by_func(self.on_playing_song_changed)
        shell_player.disconnect_by_func(self.on_elapsed_changed)
        self.settings.disconnect_by_func(self.on_user_token_changed)

    def on_playing_song_changed(self, player, entry):
        logger.debug("playing-song-changed: %r, %r", player, entry)

        self._submit_current_entry()

        self.__current_entry = entry
        self.__current_elapsed = 0

        if entry is None:
            return

        self.__current_start_time = int(time.time())
        track = _entry_to_track(entry)
        try:
            self.__client.playing_now(track)
        except Exception as e:
            self.__handle_exception(e)

    def on_elapsed_changed(self, player, elapsed):
        # logger.debug("elapsed-changed: %r, %i" % (player, elapsed))
        if player.get_playing_entry() == self.__current_entry:
            self.__current_elapsed += 1

    def on_user_token_changed(self, settings, key="user-token"):
        self.__client.user_token = settings.get_string("user-token")

    def _submit_current_entry(self):
        if self.__current_entry is not None:
            duration = self.__current_entry.get_ulong(
                            RB.RhythmDBPropType.DURATION)
            elapsed = self.__current_elapsed
            logger.debug("Elapsed: %s / %s", elapsed, duration)
            if elapsed >= 240 or elapsed >= duration / 2:
                track = _entry_to_track(self.__current_entry)
                try:
                    self.__client.listen(self.__current_start_time, track)
                except Exception as e:
                    self._handle_exception(e)

    def _handle_exception(self, e):
        logger.error("ListenBrainz exception %s: %s", type(e).__name__, e)


def _entry_to_track(entry):
    artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
    title = entry.get_string(RB.RhythmDBPropType.TITLE)
    album = entry.get_string(RB.RhythmDBPropType.ALBUM)
    track_number = entry.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)
    mb_track_id = entry.get_string(RB.RhythmDBPropType.MB_TRACKID)
    mb_album_id = entry.get_string(RB.RhythmDBPropType.MB_ALBUMID)
    mb_artist_id = entry.get_string(RB.RhythmDBPropType.MB_ARTISTID)
    additional_info = {
        "release_mbid": mb_album_id or None,
        "recording_mbid": mb_track_id or None,
        "artist_mbids": [mb_artist_id] if mb_artist_id else [],
        "tracknumber": track_number or None
    }
    return Track(artist, title, album, additional_info)


GObject.type_register(ListenBrainzSettings)