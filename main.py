import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from itertools import product


class Plansza(Gtk.Table):
    def __init__(self):
        Gtk.Table.__init__(self, 10, 10, True)
        self.przyciski = [[Gtk.ToggleButton() for x in xrange(10)] for y in xrange(10)]
        self.kulki = {1: 'kulka1.svg', 2: 'kulka2.svg', 3: 'kulka3.svg', 4: 'kulka4.svg', 5: 'kulka5.svg'}

        for x, y in product(xrange(10), repeat=2):
            self.attach(self.przyciski[x][y], x, x + 1, y, y + 1)
            self.przyciski[x][y].connect('clicked', self.kliknieto)

    def kliknieto(self, przycisk):
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('kulka1.svg', 35, 35)
        img.set_from_pixbuf(pixbuf)

        przycisk.set_image(img)


window = Gtk.Window()
window.set_default_size(400, 400)
window.add(Plansza())
window.show_all()
window.connect('delete-event', Gtk.main_quit)

Gtk.main()