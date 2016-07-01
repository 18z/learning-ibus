#! /usr/bin/env python
# -*- coding: utf-8 -*-
# UniEmoji: ibus engine for unicode emoji and symbols by name
#
# Copyright (c) 2013, 2015 Lalo Martins <lalo.martins@gmail.com>
#
# based on https://github.com/ibus/ibus-tmpl/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from __future__ import print_function

from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject

import os
import sys
import getopt
import locale


try:
    import Levenshtein
except ImportError:
    Levenshtein = None

try:
    import xdg
except ImportError:
    xdg = None
else:
    import xdg.BaseDirectory

debug_on = True


def debug(*a, **kw):
    if debug_on:
        print(*a, **kw)

# gee thank you IBus :-)
num_keys = []
for n in range(10):
    num_keys.append(getattr(IBus, str(n)))
del n

__base_dir__ = os.path.dirname(__file__)

if xdg:
    SETTINGS_DIRS = list(xdg.BaseDirectory.load_config_paths('uniemoji'))
else:
    SETTINGS_DIRS = [d for d in [os.path.expanduser('~/.config/uniemoji'), '/etc/xdg/uniemoji']
                     if os.path.isdir(d)]

###########################################################################


# the engine
class UniEmoji(IBus.Engine):
    __gtype_name__ = 'UniEmoji'

    def __init__(self):
        super(UniEmoji, self).__init__()
        self.is_invalidate = False
        self.preedit_string = u""
        self.lookup_table = IBus.LookupTable.new(10, 0, True, True)
        self.prop_list = IBus.PropList()

        debug("Create UniEmoji engine OK")

    def do_process_key_event(self, keyval, keycode, state):
        debug("process_key_event(%04x, %04x, %04x)" % (keyval, keycode, state))

        # ignore key release events
        is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.preedit_string:
            if keyval == IBus.Return:
                if self.lookup_table.get_number_of_candidates() > 0:
                    self.commit_candidate()
                else:
                    self.commit_string(self.preedit_string)
                return True
            elif keyval == IBus.Escape:
                self.preedit_string = u""
                self.update_candidates()
                return True
            elif keyval == IBus.BackSpace:
                self.preedit_string = self.preedit_string[:-1]
                self.invalidate()
                return True
            elif keyval in num_keys[1:]:
                index = num_keys.index(keyval) - 1
                page_size = self.lookup_table.get_page_size()
                if index > page_size:
                    return False
                page, pos_in_page = divmod(self.lookup_table.get_cursor_pos(),
                                           page_size)
                new_pos = page * page_size + index
                if new_pos > self.lookup_table.get_number_of_candidates():
                    return False
                self.lookup_table.set_cursor_pos(new_pos)
                self.commit_candidate()
                return True
            elif keyval == IBus.Page_Up or keyval == IBus.KP_Page_Up:
                self.page_up()
                return True
            elif keyval == IBus.Page_Down or keyval == IBus.KP_Page_Down:
                self.page_down()
                return True
            elif keyval == IBus.Up:
                self.cursor_up()
                return True
            elif keyval == IBus.Down:
                self.cursor_down()
                return True
            elif keyval == IBus.Left or keyval == IBus.Right:
                return True

        if keyval == IBus.space and len(self.preedit_string) == 0:
            # Insert space if that's all you typed (so you can more easily
            # type a bunch of emoji separated by spaces)
            return False

        # Allow typing all ASCII letters and punctuation, except digits
        if ord(' ') <= keyval < ord('0') or \
           ord('9') < keyval <= ord('~'):
            if state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK) == 0:
                self.preedit_string += unichr(keyval)
                self.invalidate()
                return True
        else:
            if keyval < 128 and self.preedit_string:
                self.commit_string(self.preedit_string)

        return False

    def invalidate(self):
        if self.is_invalidate:
            return
        self.is_invalidate = True
        GLib.idle_add(self.update_candidates)

    def page_up(self):
        if self.lookup_table.page_up():
            self._update_lookup_table()
            return True
        return False

    def page_down(self):
        if self.lookup_table.page_down():
            self._update_lookup_table()
            return True
        return False

    def cursor_up(self):
        if self.lookup_table.cursor_up():
            self._update_lookup_table()
            return True
        return False

    def cursor_down(self):
        if self.lookup_table.cursor_down():
            self._update_lookup_table()
            return True
        return False

    def commit_string(self, text):
        self.commit_text(IBus.Text.new_from_string(text))
        self.preedit_string = u""
        self.update_candidates()

    def commit_candidate(self):
        self.commit_string(self.candidates[self.lookup_table.get_cursor_pos()])

    def update_candidates(self):
        preedit_len = len(self.preedit_string)
        attrs = IBus.AttrList()
        self.lookup_table.clear()
        self.candidates = []
        # candidate_strings = set()

        # if preedit_len > 0:

        if self.preedit_string == "a":
            unicode_name = '1'
            ascii_match = 'first'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

            unicode_name = '2'
            ascii_match = 'number one'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "b":
            unicode_name = '3'
            ascii_match = 'second'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "c":
            unicode_name = '4'
            ascii_match = 'third'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "d":
            unicode_name = '5'
            ascii_match = 'fourth'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "e":
            unicode_name = '6'
            ascii_match = 'fifth'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "f":
            unicode_name = '7'
            ascii_match = 'sixth'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "g":
            unicode_name = '8'
            ascii_match = 'seventh'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        if self.preedit_string == "h":
            unicode_name = '9'
            ascii_match = 'eighth'
            display_str = u'{}: {} [{}]'.format(
                ascii_match, unicode_name, self.preedit_string)
            candidate = IBus.Text.new_from_string(display_str)
            self.candidates.append(ascii_match)
            self.lookup_table.append_candidate(candidate)

        text = IBus.Text.new_from_string(self.preedit_string)
        text.set_attributes(attrs)
        self.update_auxiliary_text(text, preedit_len > 0)

        attrs.append(IBus.Attribute.new(IBus.AttrType.UNDERLINE,
                                        IBus.AttrUnderline.SINGLE, 0, preedit_len))
        text = IBus.Text.new_from_string(self.preedit_string)
        text.set_attributes(attrs)
        self.update_preedit_text(text, preedit_len, preedit_len > 0)
        self._update_lookup_table()
        self.is_invalidate = False

    def _update_lookup_table(self):
        visible = self.lookup_table.get_number_of_candidates() > 0
        self.update_lookup_table(self.lookup_table, visible)

    def do_focus_in(self):
        debug("focus_in")
        self.register_properties(self.prop_list)

    def do_focus_out(self):
        debug("focus_out")
        self.do_reset()

    def do_reset(self):
        debug("reset")
        self.preedit_string = u""

    def do_property_activate(self, prop_name):
        debug("PropertyActivate(%s)" % prop_name)


###########################################################################
# the app (main interface to ibus)
class IMApp:

    def __init__(self, exec_by_ibus):
        if not exec_by_ibus:
            global debug_on
            debug_on = True
        self.mainloop = GLib.MainLoop()
        self.bus = IBus.Bus()
        self.bus.connect("disconnected", self.bus_disconnected_cb)
        self.factory = IBus.Factory.new(self.bus.get_connection())
        self.factory.add_engine("uniemoji", GObject.type_from_name("UniEmoji"))
        if exec_by_ibus:
            self.bus.request_name("org.freedesktop.IBus.UniEmoji", 0)
        else:
            xml_path = os.path.join(__base_dir__, 'uniemoji.xml')
            if os.path.exists(xml_path):
                component = IBus.Component.new_from_file(xml_path)
            else:
                xml_path = os.path.join(os.path.dirname(__base_dir__),
                                        'ibus', 'component', 'uniemoji.xml')
                component = IBus.Component.new_from_file(xml_path)
            self.bus.register_component(component)

    def run(self):
        self.mainloop.run()

    def bus_disconnected_cb(self, bus):
        self.mainloop.quit()


def launch_engine(exec_by_ibus):
    IBus.init()
    IMApp(exec_by_ibus).run()


def print_help(out, v=0):
    print("-i, --ibus             executed by IBus.", file=out)
    print("-h, --help             show this message.", file=out)
    print("-d, --daemonize        daemonize ibus", file=out)
    sys.exit(v)


def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    exec_by_ibus = False
    daemonize = False

    shortopt = "ihd"
    longopt = ["ibus", "help", "daemonize"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError:
        print_help(sys.stderr, 1)

    for o, a in opts:
        if o in ("-h", "--help"):
            print_help(sys.stdout)
        elif o in ("-d", "--daemonize"):
            daemonize = True
        elif o in ("-i", "--ibus"):
            exec_by_ibus = True
        else:
            print("Unknown argument: %s" % o, file=sys.stderr)
            print_help(sys.stderr, 1)

    if daemonize:
        if os.fork():
            sys.exit()

    launch_engine(exec_by_ibus)

if __name__ == "__main__":
    main()
