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
        return "\n".join([
            "",
            "{:>5}: {}".format("Šifra", self.__sifra),
            "{:>5}: {}".format("Naziv", self.__naziv),
            "{:>5}: {}".format("Cena", self.__cena)
        ])


def test():
    proizvod1 = Proizvod("0001", "Hleb 700g", 50.0)
    proizvod2 = Proizvod("0002", "Mleko 1l", 80.0)
    proizvod3 = Proizvod("0003", "Čokolada 100g", 120.0)
    print(proizvod1)
    print(proizvod2)
    print(proizvod3)

    print()
    proizvod1.cena = float(input("Unesite novu cenu za proizvod {}: ".format(proizvod1.naziv)))
    print("Nova cena proizvoda {} je {}.".format(proizvod1.naziv, proizvod1.cena))


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()