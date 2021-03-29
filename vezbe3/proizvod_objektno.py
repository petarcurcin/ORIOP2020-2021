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

    __broj_decimala = 2

    def cena_sa_pdv(self, stopa = 0.18):
        return self.__cena*(1.0+stopa)

    @classmethod
    def prikazi_proizvode(cls, proizvodi):
        format_linije = "{:5} {:20} {:5} {:15}"

        print()

        print(format_linije.format("Sifra", "Naziv", "Cena", "Cena sa pdv-om"))
        print(format_linije.format("-"*5, "-"*20,"-"*5, "-"*15))

        for proizvod in proizvodi:
            print(format_linije.format(
                proizvod.__sifra,
                proizvod.__naziv,
                proizvod.__cena,
                round(proizvod.cena_sa_pdv(), cls.__broj_decimala)
            ))

    def __init__(self, sifra, naziv, cena):
        self.__sifra = sifra
        self.__naziv = naziv
        self.__cena = cena

    def __str__(self):
        return "\n".join([
            "",
            "{:>5}: {}".format("Šifra", self.__sifra),
            "{:>5}: {}".format("Naziv", self.__naziv),
            "{:>5}: {}".format("Cena", self.__cena),
            "{:>15}: {}".format("Cena sa pdv-om", round(self.cena_sa_pdv(), self.__broj_decimala))
        ])


def test():
    proizvod1 = Proizvod("0001", "Hleb 700g", 50.0)
    proizvod2 = Proizvod("0002", "Mleko 1l", 80.0)
    proizvod3 = Proizvod("0003", "Čokolada 100g", 120.0)
    print(proizvod1)
    print(proizvod2)
    print(proizvod3)

    proizvodi = [
        proizvod1,
        proizvod2,
        proizvod3
    ]
    print("Cena proizvoda1 sa pdv-om je " + str(proizvod1.cena_sa_pdv()))

    Proizvod.prikazi_proizvode(proizvodi)
    print()
    proizvod1.cena = float(input("Unesite novu cenu za proizvod {}: ".format(proizvod1.naziv)))
    print("Nova cena proizvoda {} je {}.".format(proizvod1.naziv, proizvod1.cena))


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()