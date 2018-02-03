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

import json
import ssl
import time
from http.client import HTTPSConnection
from listenbrainz_utils import debug, error

HOST_NAME = "api.listenbrainz.org"
PATH_SUBMIT = "/1/submit-listens"
SSL_CONTEXT = ssl.create_default_context()


class Track:
    """
    Represents a single track to submit.

    See https://listenbrainz.readthedocs.io/en/latest/dev/json.html
    """
    def __init__(self, artist_name, track_name,
                 release_name=None, additional_info={}):
        """
        Create a new Track instance
        @param artist_name as str
        @param track_name as str
        @param release_name as str
        @param additional_info as dict
        """
        self.artist_name = artist_name
        self.track_name = track_name
        self.release_name = release_name
        self.additional_info = additional_info

    def to_dict(self):
        return {
            "artist_name": self.artist_name,
            "track_name": self.track_name,
            "release_name": self.release_name,
            "additional_info": self.additional_info
        }


class ListenBrainzClient:
    """
    Submit listens to ListenBrainz.org.

    See https://listenbrainz.readthedocs.io/en/latest/dev/api.html
    """

    def __init__(self):
        self.__next_request_time = 0
        self.user_token = None

    def listen(self, listened_at, track):
        """
        Submit a listen for a track
        @param listened_at as int
        @param entry as Track
        """
        payload = self.__get_payload(track)
        payload[0]["listened_at"] = listened_at
        self.__submit("single", payload)

    def playing_now(self, track):
        """
        Submit a playing now notification for a track
        @param track as Track
        """
        payload = self.__get_payload(track)
        self.__submit("playing_now", payload)

    def __submit(self, listen_type, payload, retry=0):
        self.__wait_for_ratelimit()
        debug("ListenBrainz %s: %r" % (listen_type, payload))
        data = {
            "listen_type": listen_type,
            "payload": payload
        }
        headers = {
            "Authorization": "Token %s" % self.user_token,
            "Content-Type": "application/json"
        }
        body = json.dumps(data)
        conn = HTTPSConnection(HOST_NAME, context=SSL_CONTEXT)
        try:
            conn.request("POST", PATH_SUBMIT, body, headers)
            response = conn.getresponse()
            response_data = json.loads(response.read())
            if response.status == 200:
                debug("ListenBrainz response %s: %r" % (response.status,
                                                        response_data))
            else:
                error("ListenBrainz error %s: %r" % (response.status,
                                                     response_data))
            self.__handle_ratelimit(response)
            # Too Many Requests
            if response.status == 429 and retry < 5:
                self.__request(listen_type, payload, retry + 1)
        except Exception as e:
            error("ListenBrainz::__submit():", e)

    def __wait_for_ratelimit(self):
        now = time.time()
        if self.__next_request_time > now:
            delay = self.__next_request_time - now
            debug("ListenBrainz rate limit applies, delay %d" % delay)
            time.sleep(delay)

    def __handle_ratelimit(self, response):
        remaining = int(response.getheader("X-RateLimit-Remaining", 0))
        reset_in = int(response.getheader("X-RateLimit-Reset-In", 0))
        debug("ListenBrainz X-RateLimit-Remaining: %i" % remaining)
        debug("ListenBrainz X-RateLimit-Reset-In: %i" % reset_in)
        if remaining == 0:
            self.__next_request_time = time.time() + reset_in

    def __get_payload(self, track):
        payload = {
            "track_metadata": track.to_dict()
        }

        return [payload]
