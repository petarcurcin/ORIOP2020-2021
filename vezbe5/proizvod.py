import uuid
from datetime import datetime


class Proizvodjac:

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, naziv):
        self.__naziv = naziv

    @property
    def sediste(self):
        return self.__sediste

    @sediste.setter
    def sediste(self, sediste):
        self.__sediste = sediste

    def __init__(self, naziv, sediste):
        self.__naziv = naziv
        self.__sediste = sediste

    def __str__(self):
        format_linije = "{:>7}: {}"

        return "\n".join([
            "",
            format_linije.format("Naziv", self.__naziv),
            format_linije.format("Sedište", self.__sediste)
        ])


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

    @property
    def proizvodjac(self):
        return self.__proizvodjac

    @proizvodjac.setter
    def proizvodjac(self, proizvodjac):
        self.__proizvodjac = proizvodjac

    def __init__(self, sifra, naziv, cena, proizvodjac):
        self.__sifra = sifra
        self.__naziv = naziv
        self.__cena = cena
        self.__proizvodjac = proizvodjac

    def __str__(self):
        format_linije = "{:>10}: {}"

        return "\n".join([
            "",
            format_linije.format("Šifra", self.__sifra),
            format_linije.format("Naziv", self.__naziv),
            format_linije.format("Cena", self.__cena),
            format_linije.format("Proizvođač", self.__proizvodjac.naziv)
        ])

    def format(self, format_linije):
        return format_linije.format(self.sifra, self.naziv, self.cena, self.proizvodjac.naziv)

    @classmethod
    def prikazi_proizvode(cls, proizvodi):
        format_linije = "{:5} {:20} {:9} {:10}"

        print()
        # zaglavlje
        print(format_linije.format("Šifra", "Naziv", "Cena", "Proizvođač"))
        print(format_linije.format("-"*5, "-"*20, "-"*9, "-"*10))
        # podaci
        for proizvod in proizvodi:
            print(format_linije.format(
                proizvod.__sifra,
                proizvod.__naziv,
                proizvod.__cena,
                proizvod.__proizvodjac.naziv
            ))

    @classmethod
    def ukupna_cena(cls, proizvodi):
        ukupna_cena = 0.0
        for proizvod in proizvodi:
            ukupna_cena += proizvod.__cena

        return ukupna_cena

    @classmethod
    def tabela_sa_ukupnom_cenom(cls, proizvodi):
        format_linije = "{:5} {:20} {:9} {:10}"

        # zaglavlje
        prikaz = [
            "",
            format_linije.format("Šifra", "Naziv", "Cena", "Proizvođač"),
            format_linije.format("-" * 5, "-" * 20, "-" * 9, "-" * 10)
        ]
        # podaci
        for proizvod in proizvodi:
            prikaz.append(format_linije.format(
                proizvod.__sifra,
                proizvod.__naziv,
                proizvod.__cena,
                proizvod.__proizvodjac.naziv
            ))
        # ukupna cena
        prikaz.append(format_linije.format("-"*5, "-"*20, "-"*9, "-"*10))
        prikaz.append(format_linije.format("", "", cls.ukupna_cena(proizvodi), ""))

        return "\n".join(prikaz)


class Racun:

    @property
    def sifra(self):
        return self.__sifra

    @property
    def datum_i_vreme(self):
        return self.__datum_i_vreme

    @property
    def proizvodi(self):
        return self.__proizvodi

    def __init__(self):
        self.__sifra = uuid.uuid4()
        self.__datum_i_vreme = datetime.now()
        self.__proizvodi = []

    def dodaj_proizvod(self, proizvod):
        self.__proizvodi.append(proizvod)

    def __str__(self):
        format_linije = "{:>13}: {}"

        return "\n".join([
            "",
            format_linije.format("Šifra", self.__sifra),
            format_linije.format("Datum i vreme", self.__datum_i_vreme.strftime("%d.%m.%Y. %H:%M:%S")),
            Proizvod.tabela_sa_ukupnom_cenom(self.__proizvodi)
        ])


def test():
    nase_zrno = Proizvodjac("Naše zrno", "RS")
    proizvodjaci = [
        nase_zrno,
        Proizvodjac("Imlek", "RS"),
        Proizvodjac("Samsung", "KR"),
        Proizvodjac("Apple", "US")
    ]
    for proizvodjac in proizvodjaci:
        print(proizvodjac)

    proizvodi = [
        Proizvod("0001", "Hleb 700g", 50.0, nase_zrno),
        Proizvod("0002", "Mleko 1l", 80.0, proizvodjaci[1]),
        Proizvod("0003", "Jogurt 1.5l", 130.0, proizvodjaci[1]),
        Proizvod("0004", "Samsung HDTV 42", 50000.0, proizvodjaci[2]),
        Proizvod("0005", "Samsung Galaxy S10", 95000.0, proizvodjaci[2]),
        Proizvod("0006", "iPhone XS", 110000.0, proizvodjaci[3])
    ]
    for proizvod in proizvodi:
        print(proizvod)

    Proizvod.prikazi_proizvode(proizvodi)

    racun1 = Racun()
    racun1.dodaj_proizvod(proizvodi[0])
    racun1.dodaj_proizvod(proizvodi[2])
    racun1.dodaj_proizvod(proizvodi[4])
    racun2 = Racun()
    racun2.dodaj_proizvod(proizvodi[1])
    racun2.dodaj_proizvod(proizvodi[1])
    racun2.dodaj_proizvod(proizvodi[2])
    racun2.dodaj_proizvod(proizvodi[2])
    racun2.dodaj_proizvod(proizvodi[3])
    racun2.dodaj_proizvod(proizvodi[3])
    racun3 = Racun()
    racun3.dodaj_proizvod(proizvodi[1])
    racun3.dodaj_proizvod(proizvodi[3])
    racun3.dodaj_proizvod(proizvodi[5])
    racuni = [
        racun1,
        racun2,
        racun3
    ]
    for racun in racuni:
        print(racun)


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()
