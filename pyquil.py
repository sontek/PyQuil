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
from pygments.lexers import SqlLexer
from pygments.styles.colorful import ColorfulStyle

STYLE = ColorfulStyle
SOURCE = """ 
          SELECT * FROM tblRegistrations r
          JOIN tblCountries c on r.CountryID = c.CountryID
          JOIN tblActivityRegistrations ar on ar.RegId = r.RegId
          WHERE r.ProgramCode = 'FooBar'
          AND r.RegId IN (1234, 4321, 1337)
          ORDER BY r.FirstName, r.LastName
        """
#f = file(__file__)
#try:
#    SOURCE = f.read()
#finally:
#    f.close()


class PyQuilWindow(gtk.Window):

    def __init__(self):
        super(PyQuilWindow, self).__init__()
        self.set_title('PyQuil')

        win = gtk.ScrolledWindow()
        self.add(win)
        self.textview = gtk.TextView()
        win.add(self.textview)
        buf = gtk.TextBuffer()

        styles = {}
        for token, value in SqlLexer().get_tokens(SOURCE):
            while not STYLE.styles_token(token) and token.parent:
                token = token.parent
            if token not in styles:
                styles[token] = buf.create_tag()
            start = buf.get_end_iter()
            buf.insert_with_tags(start, value.encode('utf-8'), styles[token])

        for token, tag in styles.iteritems():
            style = STYLE.style_for_token(token)
            if style['bgcolor']:
                tag.set_property('background', '#' + style['bgcolor'])
            if style['color']:
                tag.set_property('foreground', '#' + style['color'])
            if style['bold']:
                tag.set_property('weight', pango.WEIGHT_BOLD)
            if style['italic']:
                tag.set_property('style', pango.STYLE_ITALIC)
            if style['underline']:
                tag.set_property('underline', pango.UNDERLINE_SINGLE)

        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.textview.set_buffer(buf)
        self.textview.set_editable(False)
        self.textview.modify_font(pango.FontDescription('monospace'))

        self.resize(800, 500)
        self.show_all()

    def run(self):
        gtk.main()


if __name__ == '__main__':
    PyQuilWindow().run()
