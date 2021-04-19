from vezbe3.osoba_objektno_t3 import Osoba


class Zaposlen(Osoba):

    def mesecna_zarada(self):
        pass

    @classmethod
    def prikazi(cls, zaposleni):
        print()
        print("1. prikaži lekare")
        print("2. prikaži tehničare")
        print("3. prikaži sve")
        print("-"*20)
        izbor = input("Uneste izbor: ")

        if izbor == "1":
            for zaposlen in zaposleni:
                if isinstance(zaposlen, Lekar):
                    print(zaposlen)
        elif izbor == "2":
            for zaposlen in zaposleni:
                if isinstance(zaposlen, Tehnicar):
                    print(zaposlen)
        else:
            for zaposlen in zaposleni:
                print(zaposlen)

    @classmethod
    def ukupna_mesecna_zarada(cls, zaposleni):
        ukupna_zarada = 0
        for zaposlen in zaposleni:
            ukupna_zarada += zaposlen.mesecna_zarada()

        print()
        print("Ukupna mesečna zarada: {}".format(ukupna_zarada))


class Lekar(Zaposlen):

    @property
    def specijalizacija(self):
        return self.__specijalizacija

    @specijalizacija.setter
    def specijalizacija(self, specijalizacija):
        self.__specijalizacija = specijalizacija

    def __init__(self, jmbg, ime, prezime, god_rodjenja, specijalizacija):
        super().__init__(jmbg, ime, prezime, god_rodjenja)

        self.__specijalizacija = specijalizacija

    def __str__(self):
        return "\n".join([
            super().__str__(),
            "{:>12}: {}".format("Spec.", self.__specijalizacija)
        ])

    def mesecna_zarada(self):
        if self.__specijalizacija == "opsti":
            return 65000.0
        else:
            return 75000.0


class Tehnicar(Zaposlen):

    @property
    def strucna_sprema(self):
        return self.__strucna_sprema

    @strucna_sprema.setter
    def strucna_sprema(self, strucna_sprema):
        self.__strucna_sprema = strucna_sprema

    def __init__(self, jmbg, ime, prezime, god_rodjenja, strucna_sprema):
        super().__init__(jmbg, ime, prezime, god_rodjenja)

        self.__strucna_sprema = strucna_sprema

    def __str__(self):
        return "\n".join([
            super().__str__(),
            "{:>12}: {}".format("Str. spr.", self.__strucna_sprema)
        ])

    def mesecna_zarada(self):
        if self.__strucna_sprema == "visoka":
            return 60000.0
        elif self.__strucna_sprema == "visa":
            return 50000.0
        else:
            return 35000.0


def test():
    zaposleni = [
        Lekar("1111111111111", "Aaa", "Aaa", 1981, "opsti"),
        Lekar("2222222222222", "Bbb", "Bbb", 1982, "internista"),
        Tehnicar("3333333333333", "Ccc", "Ccc", 1983, "visoka"),
        Tehnicar("4444444444444", "Ddd", "Ddd", 1984, "visa"),
        Tehnicar("5555555555555", "Eee", "Eee", 1985, "srednja")
    ]
    Zaposlen.prikazi(zaposleni)
    Zaposlen.ukupna_mesecna_zarada(zaposleni)


if __name__ == "__main__":
    test()
