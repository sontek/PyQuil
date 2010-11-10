import pygtk
pygtk.require('2.0')
import gtk
import pango
from editor import PyQuilEditor

class PyQuilWindow(gtk.Window):
    def __init__(self):
        super(PyQuilWindow, self).__init__()

        self.resize(800, 500)
        self.set_title('PyQuil')

        self.vbox = vbox  = gtk.VBox()
        self.add(vbox)

        self.menubar = gtk.MenuBar()
        self.menus = {}
        self.menubar_items = {}

        vbox.pack_start(self.menubar, False)
        
        self.notebook = notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.set_scrollable(True)
        notebook.show_all()
        vbox.pack_start(notebook)
        
        self.documents = []

        file_menu = gtk.Menu()
        menu = self.add_menu('file', '_File', file_menu)
        new = gtk.ImageMenuItem(gtk.STOCK_NEW)
        new.connect('activate', self.new_file)
        menu.append(new)
        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect('activate', self.quit)
        menu.append(quit)

        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.add_fresh_document()

        self.show_all()

    def add_fresh_document(self, position=-1):
        document = gtk.ScrolledWindow()
        document.add(PyQuilEditor())

        self.notebook.insert_page(document)
        if position == -1:
            self.documents.append(document)
        else:
            self.documents.insert(position, document)

        return document

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

    def new_file(self, *args):
        doc = self.add_fresh_document()
        page_num = self.notebook.page_num(doc)
        self.notebook.set_current_page(page_num)

    def quit(self, *args):
        gtk.main_quit()

    def run(self):
        gtk.main()
