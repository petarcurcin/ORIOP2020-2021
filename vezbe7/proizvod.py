import uuid
from datetime import datetime
import pickle


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


class Podaci:

    @property
    def proizvodjaci(self):
        return self.__proizvodjaci

    @property
    def proizvodi(self):
        return self.__proizvodi

    @property
    def racuni(self):
        return self.__racuni

    def __init__(self):
        self.__proizvodjaci = []
        self.__proizvodi = []
        self.__racuni = []

    @classmethod
    def napravi_pocetne(cls):
        podaci = Podaci()

        proizvodjaci = podaci.proizvodjaci
        proizvodjaci.append(Proizvodjac("Naše zrno", "RS"))
        proizvodjaci.append(Proizvodjac("Imlek", "RS"))
        proizvodjaci.append(Proizvodjac("Samsung", "KR"))
        proizvodjaci.append(Proizvodjac("Apple", "US"))

        proizvodi = podaci.proizvodi
        proizvodi.append(Proizvod("0001", "Hleb 700g", 50.0, proizvodjaci[0]))
        proizvodi.append(Proizvod("0002", "Mleko 1l", 80.0, proizvodjaci[1]))
        proizvodi.append(Proizvod("0003", "Jogurt 1.5l", 130.0, proizvodjaci[1]))
        proizvodi.append(Proizvod("0004", "Samsung HDTV 42", 50000.0, proizvodjaci[2]))
        proizvodi.append(Proizvod("0005", "Samsung Galaxy S10", 95000.0, proizvodjaci[2]))
        proizvodi.append(Proizvod("0006", "iPhone XS", 110000.0, proizvodjaci[3]))

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

        racuni = podaci.racuni
        racuni.append(racun1)
        racuni.append(racun2)
        racuni.append(racun3)

        return podaci

    __naziv_datoteke = "podaci_proizvod"

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()

    @classmethod
    def ucitaj(cls):
        try:
            datoteka = open(cls.__naziv_datoteke, "rb")
            podaci = pickle.load(datoteka)
            datoteka.close()
        except FileNotFoundError:  # ako datoteka nije pronađena
            return Podaci.napravi_pocetne()  # kreiraj početne podatke

        return podaci


def test():
    podaci = Podaci.napravi_pocetne()

    print()
    print("Čuvanje...")
    Podaci.sacuvaj(podaci)

    print("Učitavanje...")
    podaci = Podaci.ucitaj()
    proizvodjaci = podaci.proizvodjaci
    proizvodi = podaci.proizvodi
    racuni = podaci.racuni

    for racun in racuni:
        print(racun)


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()
