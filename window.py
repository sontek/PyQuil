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
        self.resize(800, 500)
        self.show_all()

    def run(self):
        gtk.main()
