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
from engine import UniEmoji

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
