# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING


import pygtk
pygtk.require('2.0')

import gtk
import pango
import gobject

from ui.gtk.editor import PyQuilGtkEditor, PyQuilDocument
from lib.common import _

class PyQuilGtkWindow(gtk.Window):
    def __init__(self):
        super(PyQuilGtkWindow, self).__init__()

        # A decent default size
        self.resize(800, 500)
        self.set_title(_('PyQuil'))

        self.vbox = gtk.VBox()
        self.add(self.vbox)

        # create our file menu
        self.__init_menubar()

        # create the tabbed interface
        self.__init_notebook()

        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.new_tab()

        self.show_all()

    def __init_menubar(self):
        self.menubar = gtk.MenuBar()
        self.menus = {}
        self.menubar_items = {}

        self.vbox.pack_start(self.menubar, False, False)

        file_menu = gtk.Menu()
        menu = self.add_menu('file', _('_File'), file_menu)

        new = gtk.ImageMenuItem(gtk.STOCK_NEW)
        new.connect('activate', self.new_tab)
        menu.append(new)

        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect('activate', self.quit)
        menu.append(quit)

        save = gtk.ImageMenuItem(gtk.STOCK_SAVE)
        save.connect('activate', self.save)
        menu.append(save)

    def __init_notebook(self):
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.set_scrollable(True)
        self.notebook.show_all()
        self.vbox.pack_start(self.notebook)

    def add_menu(self, name, title, menu=None, position=None):
        item = gtk.MenuItem(title)
        if menu is None:
            menu = gtk.Menu()
        item.set_submenu(menu)
        self.menus[name] = menu
        self.menubar_items[name] = item
        if position is None:
            self.menubar.append(item)
        else:
            self.menubar.insert(item, position)
        return menu

    def new_tab(self, *args):
        document = PyQuilDocument()
        self.notebook.insert_page(document)
        page_num = self.notebook.page_num(document)
        self.notebook.set_current_page(page_num)
        document.show()

    def quit(self, *args):
        num_pages = self.notebook.get_n_pages()

        for i in range(0, num_pages):
            page = self.notebook.get_nth_page(i)

            if page.plugin:
                page.plugin.disconnect()

        gtk.main_quit()

    def save(self, *args):
        self.notebook.get_current_page()
        page_num = self.notebook.get_current_page()
        doc = self.notebook.get_nth_page(page_num)
        if doc.result_window:
            dialog = gtk.FileChooserDialog("Save..",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))

            dialog.set_default_response(gtk.RESPONSE_OK)

            if dialog.run() == gtk.RESPONSE_OK:
                filename = dialog.get_filename()
                liststore = doc.tree_view.get_model()

                csv = ','.join([col.get_title() for col in doc.tree_view.get_columns()]) + '\n'

                for row in liststore:
                    csv += ','.join(row) + '\n'

                f = open(filename, "w")
                f.writelines(csv)
                f.close()

            dialog.destroy()

    def run(self):
        gtk.main()
