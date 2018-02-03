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

import os
import sys
from gi.repository import Gio


def debug(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def load_settings():
    settings_dir = os.path.dirname(os.path.realpath(__file__))
    settings_dir = os.path.join(settings_dir, "schema")
    schema_source = Gio.SettingsSchemaSource.new_from_directory(settings_dir,
                                                                None, False)
    schema = schema_source.lookup("org.gnome.rhythmbox.plugins.listenbrainz",
                                  False)
    return Gio.Settings.new_full(schema, None, None)
