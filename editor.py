import gtk
import pango
from pygments.lexers import SqlLexer
from pygments.styles import get_style_by_name
from pygments.styles.colorful import ColorfulStyle
from pygments.token import STANDARD_TYPES, Token

STANDARD_TOKENS = STANDARD_TYPES.keys()

tag_name = lambda sn, token: sn + '_' + str(token).replace('.', '_').lower()


class PyQuilEditor(gtk.TextView):
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
