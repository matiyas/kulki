# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from itertools import product
from random import randint


class Plansza(Gtk.Table):
    def __init__(self):
        Gtk.Table.__init__(self, 10, 10, True)
        # Macierz 10 x 10 przechowująca przyciski
        self.przyciski = [[Gtk.ToggleButton() for x in xrange(10)] for y in xrange(10)]
        self.kulki = {1: 'kulka1.svg', 2: 'kulka2.svg', 3: 'kulka3.svg', 4: 'kulka4.svg', 5: 'kulka5.svg'}

        # Ustawianie przycisków na planszy
        for x, y in product(xrange(10), repeat=2):
            self.przyciski[x][y].set_size_request(40, 40)
            self.attach(self.przyciski[x][y], x, x + 1, y, y + 1)

    def ustaw_przycisk(self, przycisk, kolor_nr):
        img = Gtk.Image()
        # Ustawienie obrazka na przycisku
        if 0 < kolor_nr <= 5:
            przycisk.set_image(img)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.kulki[kolor_nr], 35, 35)
            img.set_from_pixbuf(pixbuf)
        else:
            przycisk.set_image(Gtk.Image())


class App(object):
    def __init__(self):
        self.window = Gtk.Window()
        self.plansza = Plansza()
        self.box = Gtk.VBox()
        self.nowa_gra_gtn = Gtk.Button('Nowa gra')
        self.kulki_mx = [[0 for x in xrange(10)] for y in xrange(10)]
        self.kulki_set = set()
        self.kulka = (-1, -1)

        # Podłączenie wszystkich przycisków na planszy do metody
        for x, y in product(xrange(10), repeat=2):
            self.plansza.przyciski[x][y].connect('clicked', self.wcisnieto, x, y)

        self.nowa_gra_gtn.set_size_request(0, 30)
        self.nowa_gra_gtn.connect('clicked', self.nowa_gra)
        self.box.add(self.plansza)
        self.box.add(self.nowa_gra_gtn)
        self.window.add(self.box)
        self.window.show_all()
        self.window.connect('delete-event', Gtk.main_quit)
        self.nowa_gra()

    def przesun(self, kulka, pozycja):
        print kulka, pozycja    # <-- USUNĄĆ
        print self.kulki_set    # <-- USUNĄĆ

        # Przesunięcie w zbiorze
        self.kulki_set.remove(kulka)
        self.kulki_set.add(pozycja)

        # Przesunięcie na macierzy
        self.kulki_mx[pozycja[0]][pozycja[1]] = self.kulki_mx[kulka[0]][kulka[1]]
        self.kulki_mx[kulka[0]][kulka[1]] = 0

    def wcisnieto(self, przycisk, x, y):
        # Wciśnięty przycisk jest kulką
        if (x, y) in self.kulki_set:
            self.plansza.przyciski[self.kulka[0]][self.kulka[1]].set_active(False)
            self.kulka = (x, y)
        # wciśnięty przycisk jest pusty
        else:
            # Jeśli pusta pozycja została wciśnięta przed kulką
            if self.kulka == (-1, -1):
                przycisk.set_active(False)
            # Pusta pozycja została wciśnięta po kulce
            else:
                self.przesun(self.kulka, (x, y))
                self.plansza.przyciski[self.kulka[0]][self.kulka[1]].set_active(False)
                self.plansza.przyciski[x][y].set_active(False)
                self.kulka = (-1, -1)
                self.losuj_kulki(3)

                # DO USUNIĘCIA ???
                for x, y in product(xrange(10), repeat=2):
                    self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])

    def losuj_kulki(self, n):
        # Losowanie n pozycji kul
        ilosc_kul = len(self.kulki_set)
        while len(self.kulki_set) < ilosc_kul + n:
            self.kulki_set.add((randint(0, 9), randint(0, 9)))

        # Losowanie koloru
        for kulka in self.kulki_set:
            if not self.kulki_mx[kulka[0]][kulka[1]]:
                self.kulki_mx[kulka[0]][kulka[1]] = randint(1, 5)

    def nowa_gra(self):
        # Na początku każdej rozgrywki wylosuj 50 kul
        self.losuj_kulki(50)

        for x, y in product(xrange(10), repeat=2):
            if self.kulki_mx[x][y]:
                self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])


if __name__ == '__main__':
    a = App()
    Gtk.main()