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
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.vbox1 = Gtk.VBox()
        self.vbox2 = Gtk.VBox()
        self.label_ranking = Gtk.Label('Ranking:')
        self.label_punkty = Gtk.Label()
        self.nowa_gra_btn = Gtk.Button('Graj od początku')
        self.kulki_mx = [[0 for x in xrange(10)] for y in xrange(10)]
        self.kulki_set = set()
        self.kulka = (-1, -1)
        self.punkty = 0
        self.lista_rankingowa = []

        # Podłączenie wszystkich przycisków na planszy do metody
        for x, y in product(xrange(10), repeat=2):
            self.plansza.przyciski[x][y].connect('toggled', self.ruch, x, y)

        self.label_punkty.set_justify(Gtk.Justification.RIGHT)
        self.label_ranking.set_size_request(50, 0)
        self.label_punkty.set_size_request(10, 30)
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

        w_linii = 1
        kulki = []

        # Sprawdź w poziomie z lewej
        i = x - 1
        while i >= 0 and kolor == self.kulki_mx[i][y]:
            w_linii += 1
            kulki.append((i, y))
            i -= 1

        # Sprawdź w poziomie z prawej
        i = x + 1
        while i < 10 and kolor == self.kulki_mx[i][y]:
            w_linii += 1
            kulki.append((i, y))
            i += 1

        # Usuń sąsiednie kulki w poziomie
        if w_linii >= 5:
            for kulka in kulki:
                czy_usunac = True
                self.kulki_mx[kulka[0]][kulka[1]] = 0
                self.kulki_set.remove(kulka)

        # Sprawdź w pionie powyżej
        w_linii = 1
        kulki = []
        i = y - 1
        while i >= 0 and kolor == self.kulki_mx[x][i]:
            w_linii += 1
            kulki.append((x, i))
            i -= 1

        # Sprawdź w pionie poniżej
        i = y + 1
        while i < 10 and kolor == self.kulki_mx[x][i]:
            w_linii += 1
            kulki.append((x, i))
            i += 1

        # Usuń sąsiednie kulki w pionie
        if w_linii >= 5:
            for kulka in kulki:
                czy_usunac = True
                self.kulki_mx[kulka[0]][kulka[1]] = 0
                self.kulki_set.remove(kulka)

        w_linii = 1
        kulki = []

        # Sprawdź po ukosie od góry od lewej
        i = x - 1
        j = y - 1
        while i >= 0 and j >= 0 and kolor == self.kulki_mx[i][j]:
            w_linii += 1
            kulki.append((i, j))
            i -= 1
            j -= 1

        i = x + 1
        j = y + 1
        while i < 10 and j < 10 and kolor == self.kulki_mx[i][j]:
            w_linii += 1
            kulki.append((i, j))
            i += 1
            j += 1

        if w_linii >= 5:
            for kulka in kulki:
                czy_usunac = True
                self.kulki_mx[kulka[0]][kulka[1]] = 0
                self.kulki_set.remove(kulka)

            w_linii = 1
            kulki = []

        # Sprawdź po ukosie od góry od prawej
        i = x + 1
        j = y - 1
        while i < 10 and j >= 0 and kolor == self.kulki_mx[i][j]:
            w_linii += 1
            kulki.append((i, j))
            i += 1
            j -= 1

        i = x - 1
        j = y + 1
        while i >= 0 and j < 10 and kolor == self.kulki_mx[i][j]:
            w_linii += 1
            kulki.append((i, j))
            i -= 1
            j += 1

        if w_linii >= 5:
            for kulka in kulki:
                czy_usunac = True
                self.kulki_mx[kulka[0]][kulka[1]] = 0
                self.kulki_set.remove(kulka)

        # Usuń kulkę 'bazową'
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
            self.plansza.przyciski[self.kulka[0]][self.kulka[1]].set_active(False)
            self.kulka = (x, y)
        # Wciśnięty przycisk jest pusty
        else:
            # Jeśli pusta pozycja została wciśnięta przed kulką
            if self.kulka == (-1, -1):
                przycisk.set_active(False)
            # Pusta pozycja została wciśnięta po kulce
            elif przycisk.get_active():
                self.przesun(self.kulka, (x, y))
                self.plansza.przyciski[self.kulka[0]][self.kulka[1]].set_active(False)
                self.plansza.przyciski[x][y].set_active(False)
                if not self.sprawdz(x, y):
                    self.losuj_kulki(3)
                self.punkty += 1
                self.label_punkty.set_markup('Liczba punktów: <b>{}</b>'.format(self.punkty))
                self.kulka = (-1, -1)

                # DO USUNIĘCIA ???
                for x, y in product(xrange(10), repeat=2):
                    self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])

    def losuj_kulki(self, n):
        # Losowanie n pozycji kul
        ilosc_kul = len(self.kulki_set)
        nowe = set()
        while len(self.kulki_set) < ilosc_kul + n and len(self.kulki_set) < 100:
            self.kulki_set.add((randint(0, 9), randint(0, 9)))

        # SET ZMIENIA ROZMIAR PODCZAS ITEROWANIA
        # Losowanie koloru
        for kulka in self.kulki_set:
            if not self.kulki_mx[kulka[0]][kulka[1]]:
                self.kulki_mx[kulka[0]][kulka[1]] = randint(1, 5)
                self.sprawdz(kulka[0], kulka[1])

    def nowa_gra(self, przycisk):
        if self.punkty:
            self.lista_rankingowa.append(self.punkty)
            self.lista_rankingowa.sort(reverse=True)
            self.label_ranking.set_text('Ranking:\n')

            for i in xrange(len(self.lista_rankingowa)):
                self.label_ranking.set_markup(self.label_ranking.get_text() + '<b>{}.</b>\t{}\n'.format(i + 1, self.lista_rankingowa[i]))

        self.punkty = 0
        self.kulki_mx = [[0 for x in xrange(10)] for y in xrange(10)]
        self.kulki_set = set()
        self.label_punkty.set_markup('Liczba punktów: <b>{}</b>'.format(self.punkty))
        # Na początku każdej rozgrywki wylosuj 50 kul
        self.losuj_kulki(50)

        for x, y in product(xrange(10), repeat=2):
            self.plansza.ustaw_przycisk(self.plansza.przyciski[x][y], self.kulki_mx[x][y])


if __name__ == '__main__':
    a = App()
    Gtk.main()