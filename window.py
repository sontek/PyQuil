import pygtk
pygtk.require('2.0')
import gtk
import pango
from editor import PyQuilEditor

from sqlalchemy import create_engine
import pyodbc

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

        self.connection_string = gtk.Entry()
        self.connection_string.set_text('sqlite:///test.db')
        vbox.pack_start(self.connection_string)
        
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

        execute = gtk.MenuItem('Execute')
        execute.connect('activate', self.execute)
        menu.append(execute)

        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect('activate', self.quit)
        menu.append(quit)

        self.connect('delete-event', lambda *a: gtk.main_quit())

        self.add_fresh_document()

        self.show_all()

    def add_fresh_document(self, position=-1):
        document = gtk.ScrolledWindow()
        self.editor = PyQuilEditor()
        self.editor.get_buffer().set_text("SELECT * FROM memos")
        document.add(self.editor)

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

    def execute(self, *args):
        buf = self.editor.get_buffer()
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        query = buf.get_slice(start, end)
        conn_string = self.connection_string.get_text() 
        e = create_engine(conn_string)
        connection = e.connect()
        results = connection.execute(query)
        connection.close()
        result_view = gtk.ScrolledWindow()
        result_text = gtk.TextView()
        data = results.fetchall()
        text = ''

        for item in data:
            text +='\n' + str(item)

        result_text.get_buffer().set_text(text)
        result_view.add(result_text)
        self.vbox.pack_start(result_view)
        result_text.show()
        result_view.show()

    def run(self):
        gtk.main()
