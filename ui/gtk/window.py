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
        self.tree_view = None

        self.resize(800, 500)
        self.set_title(_('PyQuil'))

        self.vbox = vbox  = gtk.VBox()
        self.add(vbox)

        self.menubar = gtk.MenuBar()
        self.menus = {}
        self.menubar_items = {}

        vbox.pack_start(self.menubar, False, False)

        self.hbox = gtk.HBox()
        plugin_store = gtk.ListStore(gobject.TYPE_STRING)
        plugin_store.append ([_("Sql Alchemy")])
        plugin_store.append ([_("MSSQL")])

        self.combo_plugin = gtk.ComboBox()
        self.combo_plugin.set_model(plugin_store)
        cell = gtk.CellRendererText()
        self.combo_plugin.pack_start(cell, True)
        self.combo_plugin.add_attribute(cell, 'text', 0)
        self.combo_plugin.set_active(0)

        self.hbox.pack_start(self.combo_plugin, False, False)

        self.connection_string = gtk.Entry()
        self.connection_string.set_text(_('sqlite:///test.db'))
        self.hbox.pack_start(self.connection_string, True)

        self.button_execute = gtk.Button(label=_("Execute"))
        self.button_execute.connect('clicked', self.execute)
        self.hbox.pack_start(self.button_execute, False, False)

        self.vbox.pack_start(self.hbox, False, False)
        self.notebook = notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.set_scrollable(True)
        notebook.show_all()
        vbox.pack_start(notebook)

        self.documents = []

        file_menu = gtk.Menu()
        menu = self.add_menu('file', _('_File'), file_menu)

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
        editor = PyQuilGtkEditor()
        editor.get_buffer().set_text(_("SELECT * FROM memos"))

        document = PyQuilDocument(editor, None)
        self.notebook.insert_page(document)

        if position == -1:
            self.documents.append(document)
        else:
            self.documents.insert(position, document)

        editor.show()
        document.show()
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
        doc.show()

    def quit(self, *args):
        gtk.main_quit()

    def execute(self, *args):
        page = self.notebook.get_current_page()
        doc = self.notebook.get_nth_page(page)
        editor = doc.editor
        buf = editor.get_buffer()
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        query = buf.get_slice(start, end)
        conn_string = self.connection_string.get_text()

        data = None
        plugin = None
        selected_plugin = self.combo_plugin.get_active_text()

        if selected_plugin == _('Sql Alchemy'):
            from plugins.sqlalchemy import SAQueryPlugin
            plugin = SAQueryPlugin()
        elif selected_plugin == _('MSSQL'):
            from plugins.mssql import MSSQLQueryPlugin
            plugin = MSSQLQueryPlugin()

        try:
            columns, data = plugin.execute_query(conn_string, query)
            types = []
            if data:
                for item in data[0]:
                    types.append(str)

                liststore = gtk.ListStore(*types)

                for row in [b for a, b in enumerate(data)]:
                    liststore.append([b for a, b in enumerate(row)])

                if (doc.tree_view):
                    doc.remove(doc.tree_view)

                tree_view = gtk.TreeView(model=liststore)

                tvcolumns={} # the columns
                cells={} # the cells
                i=0
                for c in columns: # the actual column headers
                    # instantiate TVC
                    tvcolumns[c] = gtk.TreeViewColumn(c)

                    # add to the treeview
                    tree_view.append_column(tvcolumns[c])

                    # instantiate and add the cell object
                    cells[c]=gtk.CellRendererText()
                    tvcolumns[c].pack_start(cells[c], True) #add the cell to the column, allow it to expand

                    # now set the cell's text attribute to the treeview's column i (0,1)
                    tvcolumns[c].add_attribute(cells[c], 'text', i)

                    #make it searchable and sortable
                    tree_view.set_search_column(i)
                    tvcolumns[c].set_sort_column_id(i)
                    i+=1

                doc.set_treeview(tree_view)
                doc.show()
                doc.tree_view.show()
        except Exception as exc:
            md = gtk.MessageDialog(self, 
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                    gtk.BUTTONS_CLOSE, str(exc))
            md.run()
            md.destroy()


    def run(self):
        gtk.main()
