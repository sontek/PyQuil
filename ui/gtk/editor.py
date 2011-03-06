import gtk
import pango
import gobject
from pygments.lexers import SqlLexer
from pygments.styles import get_style_by_name
from pygments.styles.colorful import ColorfulStyle
from pygments.token import STANDARD_TYPES, Token
from lib.common import _

STANDARD_TOKENS = STANDARD_TYPES.keys()

tag_name = lambda sn, token: sn + '_' + str(token).replace('.', '_').lower()

class PyQuilDocument(gtk.VBox):
    def __init__(self):
        super(gtk.VBox, self).__init__()
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
        self.result_window = None

        self.hbox.pack_start(self.combo_plugin, False, False)

        self.connection_string = gtk.Entry()
        self.connection_string.set_text(_('sqlite:///test.db'))
        self.hbox.pack_start(self.connection_string, True)

        self.button_execute = gtk.Button(label=_("Execute"))
        self.button_execute.connect('clicked', self.execute)
        self.hbox.pack_start(self.button_execute, False, False)

        self.pack_start(self.hbox, False, False)
        editor_window = gtk.ScrolledWindow()
        self.editor = PyQuilGtkEditor()
        self.editor.get_buffer().set_text(_("SELECT * FROM memos"))
        editor_window.add(self.editor)
        self.pack_start(editor_window)
        self.tree_view = None

        self.show_all()

    def execute(self, *args):
        buf = self.editor.get_buffer()
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

                self.set_treeview(tree_view)
                self.show_all()
        except Exception as exc:
            md = gtk.MessageDialog(None,
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                    gtk.BUTTONS_CLOSE, str(exc))
            md.run()
            md.destroy()

    def set_treeview(self, tree_view):
        self.tree_view = tree_view
        if self.result_window:
            self.remove(self.result_window)

        self.result_window = gtk.ScrolledWindow()
        self.result_window.add(self.tree_view)
        self.pack_start(self.result_window)

class PyQuilGtkEditor(gtk.TextView):
    def __init__(self):
        gtk.TextView.__init__(self)
        self.buf = buf = self.get_buffer()
        self.hl_style = None
        self._generated_styles = set()
        
        self.set_style(ColorfulStyle)
        self.set_lexer(SqlLexer())
        
        self._changehandler = buf.connect_after('changed', self._on_change)
        
        self.modify_font(pango.FontDescription('monospace'))
    
    def get_all_text(self):
        return self.buf.get_text(self.buf.get_start_iter(),
                                 self.buf.get_end_iter())
    
    def set_style(self, style):
        oldstyle = self.hl_style
        if isinstance(style, basestring):
            style = get_style_by_name(style)
        
        if style not in self._generated_styles:
            self._generate_tags(style)
        
        self.hl_style = style
        self.style_name = style.__name__
        
        bg_color = style.background_color
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(bg_color))
        fg_style = style.style_for_token(Token.Name)
        fg_color = '#' + (fg_style['color'] or '000')
        self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse(fg_color))
    
    def set_lexer(self, lexer):
        self.lexer = lexer
        self.rehighlight(self.buf)
    
    def _generate_tags(self, hl_style):
        buf = self.buf
        style_name = hl_style.__name__
        for token in STANDARD_TOKENS:
            name = tag_name(style_name, token)
            style = hl_style.style_for_token(token)
            tag = buf.create_tag(name)
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
    
    def _on_change(self, buf):
        buf.handler_block(self._changehandler)
        self.rehighlight(buf)
        buf.handler_unblock(self._changehandler)
    
    def rehighlight(self, buf):
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        text = buf.get_slice(start, end)
        buf.remove_all_tags(start, end)
        end = buf.get_start_iter()
        style_name = self.style_name
        for token, value in self.lexer.get_tokens(text):
            ln = len(value)
            end.forward_cursor_positions(ln)
            tag = tag_name(style_name, token)
            buf.apply_tag_by_name(tag, start, end)
            start.forward_cursor_positions(ln)
