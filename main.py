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
        self.kolory = {1: 'kulka1.svg', 2: 'kulka2.svg', 3: 'kulka3.svg', 4: 'kulka4.svg', 5: 'kulka5.svg'}

        # Ustawianie przycisków na planszy
        for x, y in product(xrange(10), repeat=2):
            self.przyciski[x][y].set_size_request(40, 40)
            self.attach(self.przyciski[x][y], x, x + 1, y, y + 1)

    def ustaw_przycisk(self, przycisk, kolor_nr):
        img = Gtk.Image()

        # Ustawienie obrazka na przycisku
        if 0 < kolor_nr <= 5:
            przycisk.set_image(img)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(self.kolory[kolor_nr], 35, 35)
            img.set_from_pixbuf(pixbuf)
        else:
            przycisk.set_image(Gtk.Image())


class App(object):
    def __init__(self):
        self.window = Gtk.Window(title='Kulki')
        self.plansza = Plansza()
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.vbox1 = Gtk.VBox()
        self.vbox2 = Gtk.VBox()
        self.label_punkty = Gtk.Label()
        self.label_ranking = Gtk.Label('Ranking:')
        self.nowa_gra_btn = Gtk.Button('Graj od początku')
        self.kulki_mx = [[0 for x in xrange(10)] for y in xrange(10)]   # Przechowuje kolory kulek
        self.kulki_set = set()                                          # Przechowuje pozycje kulek
        self.wcisnieta_kulka = ()
        self.punkty = 0
        self.lista_wynikow = []

        # Podłączenie wszystkich przycisków na planszy do metody
        for x, y in product(xrange(10), repeat=2):
            self.plansza.przyciski[x][y].connect('toggled', self.ruch, x, y)

        self.label_punkty.set_justify(Gtk.Justification.RIGHT)
        self.label_punkty.set_size_request(10, 30)
        self.label_ranking.set_size_request(50, 0)
        self.nowa_gra_btn.set_size_request(0, 30)
        self.nowa_gra_btn.connect('clicked', self.nowa_gra)

        self.hbox1.pack_start(self.label_punkty, False, True, 0)
        self.vbox2.pack_start(self.label_ranking, False, True, 0)
        self.hbox2.add(self.vbox2)
        self.hbox2.add(self.plansza)
        self.vbox1.add(self.hbox1)
        self.vbox1.add(self.hbox2)
        self.vbox1.add(self.nowa_gra_btn)
        self.window.add(self.vbox1)

        self.window.show_all()
        self.window.connect('delete-event', Gtk.main_quit)
        self.nowa_gra(self.nowa_gra_btn)

    def sprawdz(self, x, y):
        kolor = self.kulki_mx[x][y]
        czy_usunac = False
        do_usuniecia = []

        def sprawdz_linie(x, y, ix, iy, zlicz):
            while 0 <= x < 10 and 0 <= y < 10 and kolor == self.kulki_mx[x][y]:
                zlicz += 1
                do_usuniecia.append((x, y))
                x += 1 * ix
                y += 1 * iy
            return zlicz

        # Sprawdzanie dla linii pionowej, poziomej i ukośnych
        it_lst = [(i, j) for i, j in product(xrange(-1, 2), repeat=2)]
        for i, j in zip(it_lst[:-5], it_lst[5:][::-1]):
            w_linii = sprawdz_linie(x + i[0], y + i[1], i[0], i[1], 1)
            w_linii = sprawdz_linie(x + j[0], y + j[1], j[0], j[1], w_linii)

            if w_linii >= 5:
                for kulka in do_usuniecia:
                    self.kulki_mx[kulka[0]][kulka[1]] = 0
                    self.kulki_set.remove(kulka)
                czy_usunac = True
            do_usuniecia = []

        # Jeśli przycisk znajdował się w linii to go usuń
        if czy_usunac:
            self.kulki_mx[x][y] = 0
            self.kulki_set.remove((x, y))
            return True

    def przesun(self, kulka, pozycja):
        # Przesunięcie w zbiorze
        self.kulki_set.remove(kulka)
        self.kulki_set.add(pozycja)

        # Przesunięcie na macierzy
        self.kulki_mx[pozycja[0]][pozycja[1]] = self.kulki_mx[kulka[0]][kulka[1]]
        self.kulki_mx[kulka[0]][kulka[1]] = 0

    def ruch(self, przycisk, x, y):
        # Wciśnięty przycisk jest kulką
        if (x, y) in self.kulki_set:
            # Przed wciśnięciem przycisku wciśnięto inny przycisk
            if self.wcisnieta_kulka and (x, y) != self.wcisnieta_kulka:
                self.plansza.przyciski[self.wcisnieta_kulka[0]][self.wcisnieta_kulka[1]].set_active(False)
            self.wcisnieta_kulka = (x, y)

        # Została wciśnięta pusta pozycja
        else:
            # Pusta pozycja została wciśnięta przed wciśnięciem kulki
            if not self.wcisnieta_kulka:
                przycisk.set_active(False)

            # Pusta pozycja została wciśnięta po wciśnięciu kulki
            elif przycisk.get_active():
                self.przesun(self.wcisnieta_kulka, (x, y))
                self.plansza.przyciski[self.wcisnieta_kulka[0]][self.wcisnieta_kulka[1]].set_active(False)
                self.plansza.przyciski[x][y].set_active(False)

                # Jeśli przesunięta linia nie znajduje się w linii 5 kulek to wylosuj 3 nowe kulki
                if not self.sprawdz(x, y):
                    self.losuj_kulki(3)

                self.punkty += 1
                self.label_punkty.set_markup('Liczba punktów: <b>{}</b>'.format(self.punkty))
                self.wcisnieta_kulka = ()

                # Aktualizuj kulki na planszy
                for x, y in product(xrange(10), repeat=2):
                    self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])

    def losuj_kulki(self, n):
        ilosc_kul = len(self.kulki_set)

        while len(self.kulki_set) < ilosc_kul + n and len(self.kulki_set) < 100:
            rozmiar = len(self.kulki_set)
            nowa = (randint(0, 9), randint(0, 9))
            self.kulki_set.add(nowa)
            nowy_rozmiar = len(self.kulki_set)

            # Sprawdzanie, po wylowaniu każdej nowej kulki, czy w linii nie znajduje się 5 takich samych kulek
            if rozmiar != nowy_rozmiar:
                self.kulki_mx[nowa[0]][nowa[1]] = randint(1, 5)
                self.sprawdz(nowa[0], nowa[1])

    def nowa_gra(self, przycisk):
        # Przechowywanie niezeorwych wyników w kolejności malejącej
        if self.punkty:
            self.lista_wynikow.append(self.punkty)
            self.lista_wynikow.sort(reverse=True)
            self.label_ranking.set_text('Ranking:\n')

            # Dodawanie wyników do labeli
            i = 1
            for wynik in self.lista_wynikow[:5]:
                self.label_ranking.set_markup(self.label_ranking.get_text() + '<b>{}.</b>\t{}\n'.format(i, wynik))
                i += 1

        # Resetowanie danych
        self.punkty = 0
        self.kulki_mx = [[0 for x in xrange(10)] for y in xrange(10)]
        self.kulki_set = set()
        self.label_punkty.set_markup('Liczba punktów: <b>{}</b>'.format(self.punkty))

        # Na początku każdej rozgrywki wylosuj 50 kul
        self.losuj_kulki(50)

        # Aktualizuj kulki na planszy
        for x, y in product(xrange(10), repeat=2):
            self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])


if __name__ == '__main__':
    a = App()
    Gtk.main()