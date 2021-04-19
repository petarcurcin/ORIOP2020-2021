class Proizvod:

    @property
    def sifra(self):
        return self.__sifra

    @sifra.setter
    def sifra(self, sifra):
        self.__sifra = sifra

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, naziv):
        self.__naziv = naziv

    @property
    def cena(self):
        return self.__cena

    @cena.setter
    def cena(self, cena):
        self.__cena = cena

    def __init__(self, sifra, naziv, cena):
        self.__sifra = sifra
        self.__naziv = naziv
        self.__cena = cena

    def __str__(self):
        format_linije = "{:>12}: {}"

        return "\n".join([
            "",
            format_linije.format("Šifra", self.__sifra),
            format_linije.format("Naziv", self.__naziv),
            format_linije.format("Cena", self.__cena)
        ])

    def format(self, format_linije):
        return format_linije.format(self.sifra, self.naziv, self.cena, "", "")

    @classmethod
    def prikazi_proizvode(cls, proizvodi):
        format_linije = "{:5} {:20} {:9} {:>12} {:>12}"

        print()
        # zaglavlje
        print(format_linije.format("Šifra", "Naziv", "Cena", "Rok trajanja", "Garancija"))
        print(format_linije.format("-"*5, "-"*20, "-"*9, "-"*12, "-"*12))
        # podaci
        for proizvod in proizvodi:
            print(proizvod.format(format_linije))

    @classmethod
    def prikazi_prebrojavanje(cls, proizvodi):
        prehrambeni = 0
        tehnicki = 0
        ostali = 0
        for proizvod in proizvodi:
            if isinstance(proizvod, PrehrambeniProizvod):
                prehrambeni += 1
            elif isinstance(proizvod, TehnickiProizvod):
                tehnicki += 1
            else:
                ostali += 1

        format_linije = "{:>11}: {}"

        print()
        print(format_linije.format("Prehrambeni", prehrambeni))
        print(format_linije.format("Tehnički", tehnicki))
        print(format_linije.format("Ostali", ostali))


class PrehrambeniProizvod(Proizvod):

    @property
    def rok_trajanja(self):
        return self.__rok_trajanja

    @rok_trajanja.setter
    def rok_trajanja(self, rok_trajanja):
        self.__rok_trajanja = rok_trajanja

    def __init__(self, sifra, naziv, cena, rok_trajanja):
        super().__init__(sifra, naziv, cena)

        self.__rok_trajanja = rok_trajanja

    def __str__(self):
        format_linije = "{:>12}: {}dana"

        return "\n".join([
            super().__str__(),
            format_linije.format("Rok trajanja", self.__rok_trajanja)
        ])

    def format(self, format_linije):
        return format_linije.format(
            self.sifra,
            self.naziv,
            self.cena,
            "{}dana".format(self.__rok_trajanja),
            ""
        )


class TehnickiProizvod(Proizvod):

    @property
    def garancija(self):
        return self.__garancija

    @garancija.setter
    def garancija(self, garancija):
        self.__garancija = garancija

    def __init__(self, sifra, naziv, cena, garancija):
        super().__init__(sifra, naziv, cena)

        self.__garancija = garancija

    def __str__(self):
        format_linije = "{:>12}: {}meseca"

        return "\n".join([
            super().__str__(),
            format_linije.format("Garancija", self.__garancija)
        ])

    def format(self, format_linije):
        return format_linije.format(
            self.sifra,
            self.naziv,
            self.cena,
            "",
            "{}meseca".format(self.__garancija)
        )


def test():
    proizvodi = [
        PrehrambeniProizvod("0001", "Hleb 700g", 50.0, 7),
        PrehrambeniProizvod("0002", "Mleko 1l", 80.0, 180),
        PrehrambeniProizvod("0003", "Čokolada 100g", 120.0, 60),
        TehnickiProizvod("0004", "Samsung HDTV 42", 50000.0, 24),
        TehnickiProizvod("0005", "iPhone XS", 110000.0, 24),
        Proizvod("0006", "Čačkalice 100kom.", 75.0)
    ]
    for proizvod in proizvodi:
        print(proizvod)

    Proizvod.prikazi_proizvode(proizvodi)
    Proizvod.prikazi_prebrojavanje(proizvodi)


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()
