import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from itertools import product


class Plansza(Gtk.Table):
    def __init__(self):
        Gtk.Table.__init__(self, 10, 10, True)
        self.przyciski = [[Gtk.Button() for x in xrange(10)] for y in xrange(10)]

        for x, y in product(xrange(10), repeat=2):
            self.attach(self.przyciski[x][y], x, x + 1, y, y + 1)

window = Gtk.Window()
window.add(Plansza())
window.show_all()
window.connect('delete-event', Gtk.main_quit)

Gtk.main()