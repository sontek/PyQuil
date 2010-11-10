#!/usr/bin/env python
# Copyright (c) 2010 by John Anderson <sontek@gmail.com>
# Copyright (c) 2010 by Thomas Holloway <nyxtom@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')
import gtk
import pango
from editor import PyQuilEditor

class PyQuilWindow(gtk.Window):
    def __init__(self):
        super(PyQuilWindow, self).__init__()
        self.set_title('PyQuil')
        win = gtk.ScrolledWindow()
        self.add(win)
        self.textview = PyQuilEditor()
        win.add(self.textview)
        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.textview.modify_font(pango.FontDescription('monospace'))

        self.resize(800, 500)
        self.show_all()

    def run(self):
        gtk.main()

if __name__ == '__main__':
    PyQuilWindow().run()
