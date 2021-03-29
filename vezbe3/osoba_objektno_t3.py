import datetime



class Osoba:

    @property
    def jmbg(self):
        return self.__jmbg

    @jmbg.setter
    def jmbg(self, jmbg):
        self.__jmbg = jmbg

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, ime):
        self.__ime = ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, prezime):
        self.__prezime = prezime

    @property
    def god_rodjenja(self):
        return self.__god_rodjenja

    @god_rodjenja.setter
    def god_rodjenja(self, god_rodjenja):
        self.__god_rodjenja = god_rodjenja

    __tekuca_godina = datetime.datetime.now().year

    def starost(self):
        return self.__tekuca_godina - self.__god_rodjenja

    def __init__(self, jmbg, ime, prezime, god_rodjenja):
        self.__jmbg = jmbg
        self.__ime = ime
        self.__prezime = prezime
        self.__god_rodjenja = god_rodjenja

    def __str__(self):
        return "\n".join([
            "",
            "{:>12}: {}".format("JMBG", self.__jmbg),
            "{:>12}: {}".format("Ime", self.__ime),
            "{:>12}: {}".format("Prezime", self.__prezime),
            "{:>12}: {}".format("God. rođenja", self.__god_rodjenja),
            "{:>12}: {}".format("Starost", self.starost())
        ])

    @classmethod
    def prikazi_osobe(cls, osobe):
        format_linije = "{:13} {:10} {:10} {:13} {:7}"
        print()

        print(format_linije.format("JMBG", "Ime", "Prezime", "God. rodjenja", "Starost"))
        print(format_linije.format("-"*13, "-"*10, "-"*10, "-"*13, "-"*7))

        for osoba in osobe:
            print(format_linije.format(
                osoba.__jmbg,
                osoba.__ime,
                osoba.__prezime,
                osoba.__god_rodjenja,
                osoba.starost()
            ))

    @classmethod
    def izvestaj_1(cls, osobe):
        # godine = []
        #
        # for osoba in osobe:
        #     godine.append(osoba.starost())
        #
        # print("Maksimalna starost je: " + str(max(godine)))
        # print("Minimalna starost je: " + str(min(godine)))
        # print("Prosecna starost je: " + str(sum(godine)/len(godine)))

        minimalna_starost = 100
        ukupna_starost = 0
        maksimalna_starost = 0

        for osoba in osobe:
            minimalna_starost = min(minimalna_starost, osoba.starost())
            maksimalna_starost = max(maksimalna_starost, osoba.starost())
            ukupna_starost = ukupna_starost + osoba.starost()

        prosecna_starost = ukupna_starost/len(osobe)

        print("{:15}: {}".format("Minimalna starost je", minimalna_starost))
        print("{:15}: {}".format("Maksimalna starost je", maksimalna_starost))
        print("{:15}: {}".format("Prosecna starost je", prosecna_starost))


def test():
    osoba1 = Osoba("1111111111111", "Aaa", "Aaa", 2001)
    osoba2 = Osoba("2222222222222", "Bbb", "Bbb", 2002)
    osoba3 = Osoba("3333333333333", "Ccc", "Ccc", 2003)
    osoba4 = Osoba("4444444444444", "Ddd", "Ddd", 2002)
    osoba5 = Osoba("5555555555555", "Eee", "Eee", 2003)
    osoba6 = Osoba("6666666666666", "Fff", "Fff", 2010)

    osobe = [
        osoba1,
        osoba2,
        osoba3,
        osoba4,
        osoba5,
        osoba6
    ]
    for osoba in osobe:
        print(osoba)

    print()
    print("Starost osobe {} {} je {}godina.".format(
        osoba1.ime,
        osoba1.prezime,
        osoba1.starost()
    ))

    Osoba.prikazi_osobe(osobe)
    Osoba.izvestaj_1(osobe)

    
if __name__ == "__main__":
    test()
