# -*- coding: utf-8 -*-

from itertools import product
from random import randint


#plansza = [[' ' for x in xrange(10)] for y in xrange(10)]
kulki = set()   # Zbiór przechowujący pozycje kul


def przesun(kulka, pozycja, kulki, plansza, szerokosc, wysokosc):
    """Przesunięcie kulki na inną pozycją
    
    Argumenty:
        kulka ((int, int)):         Pozycja kulki, która ma zostać przesunięta.
        pozycja ((int, int)):       Pozycja na planszy, na którą kulka ma zostać przesunięta.
        kulki (set(set(int, int))): Zbiór składający się z dwuelementowych zbiorów przechowujących pozycje kul.   
        plansza (list[str])):       Lista przechowująca y list składających się z x ciągów znaków, w których '-' oznacza wolną pozycję, 'Z' 
                                    kulę żółtą, 'N' kulę niebieską, 'C' kulę czerwoną, 'Z' kulę zieloną, a 'R' kulę różową.
        szerokosc (int):            Szerokość planszy.
        wysokosc (int):             Wysokość planszy.
        
    Metoda zmienia pozycję kulki na planszy na pozycję podaną jako drugi argument. Kulka zostanie przesunięta, jeżeli pozycja na planszy nie
    jest zajęta przez inną kulkę.
    """
    # Sprawdzanie, czy podane pozycje są prawidłowe
    if (0 <= kulka[1] < szerokosc) and (0 <= kulka[0] < wysokosc) and\
       (0 <= pozycja[1] < szerokosc) and (0 <= pozycja[0] < wysokosc): #and\
       #(plansza[pozycja[1]][pozycja[0]] == ' ') and (plansza[kulka[1]][kulka[0]] == 'O'):

        # Przesunięcie kulki na planszy
        # plansza[kulka[1]][kulka[0]] = ' '
        # plansza[pozycja[1]][pozycja[0]] = 'O'

        # Zmiana pozycji kuli w zbiorze
        kulki.remove((kulka[1], kulka[0]))
        kulki.add((pozycja[1], pozycja[0]))

    else:
        print 'Błędna pozycja!'


def losuj_kulki(kulki, n, plansza, szerokosc, wysokosc):
    """Losowanie kulek
    
    Argumenty:
        kulki (set(set(int, int))): Zbiór składający się z dwuelementowych zbiorów przechowujących pozycje kul.
        n (int):                    Ilość kul, które mają zostać wylosowane.
        plansza (list[str])):       Lista przechowująca listy składających się z x ciągów znaków, w których '-' oznacza wolną pozycję, 'Z' 
                                    kulę żółtą, 'N' kulę niebieską, 'C' kulę czerwoną, 'Z' kulę zieloną, a 'R' kulę różową.
        szerokosc (int):            Szerokość planszy.
        wysokosc (int):             Wysokość planszy.
        
        Metoda losuje n nowych kul, których pozycje dopisuje do zbioru 'kulki' oraz do planszy
    """
    # Losowanie n pozycji kul
    ilosc_kul = len(kulki)
    while len(kulki) < ilosc_kul + n:
        kulki.add((randint(0, 9), randint(0, 9)))

    # Zaznaczenie na planszy pozycji kul
    for kulka in kulki:
        plansza[kulka[0]][kulka[1]] = 'O'


while True:
    for i in plansza:
        print i

    p1 = input('kulka: ')
    p2 = input('pole: ')

    print type(p1)

    przesun(p1, p2, kulki, plansza, 10, 10)