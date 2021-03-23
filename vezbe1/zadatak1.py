def prikazi_osobu(osoba):

    format_linije = "{:>13}: {}"

    print()
    print(format_linije.format("JMBG", osoba["jmbg"]))
    print(format_linije.format("Ime", osoba["ime"]))
    print(format_linije.format("Prezime", osoba["prezime"]))
    print(format_linije.format("God. rodjenja", osoba["god_rodjenja"]))

def prikazi_osobe(osobe):
    format_linije = "{:13} {:10} {:10} {:13}"

    print()
    print(format_linije.format("JMBG", "Ime", "Prezime", "God. rodjenja"))
    print(format_linije.format("-"*13, "-"*10, "-"*10,"-"*13))

    for osoba in osobe:
        print(format_linije.format(osoba["jmbg"],osoba["ime"],osoba["prezime"],osoba["god_rodjenja"]))

def pronadji_osobu(osobe, jmbg):
    pronadjena_osoba = None
    for osoba in osobe:
        if osoba["jmbg"] == jmbg:
            pronadjena_osoba = osoba
            break

    return pronadjena_osoba

def unesi_osobu(osobe):
    print()
    print("Unos osobe:")

    print()

    jmbg = ""
    while len(jmbg) != 13 or not jmbg.isdigit() or pronadji_osobu(osobe, jmbg):
        jmbg = input("Unesite JMBG: ")

    ime, prezime, god_rodjenja = unesi_ime_prezime_god_rodjenja()

    osoba = {
        "jmbg": jmbg,
        "ime": ime,
        "prezime": prezime,
        "god_rodjenja": god_rodjenja
    }

    osobe.append(osoba)

def unesi_ime_prezime_god_rodjenja():
    ime = ""
    while len(ime) < 2 or len(ime) > 10:
        ime = input("Unesite ime: ")

    prezime = ""
    while len(prezime) < 2 or len(prezime) > 10:
        prezime = input("Unesite prezime: ")

    god_rodjenja = 0
    while god_rodjenja < 1900 or god_rodjenja > 2020:
        try:
            god_rodjenja = int(input("Unesite god. rodjenja : "))
        except ValueError:
            pass

    return ime, prezime, god_rodjenja


def izmeni_osobu(osobe):
    print()
    print("Izmena osobe: ")
    print()

    jmbg = ""

    while len(jmbg) != 13 or not jmbg.isdigit():
        jmbg = input("Unesite JMBG: ")

    pronadjena_osoba = pronadji_osobu(osobe, jmbg)
    if pronadjena_osoba is None:
        print()
        print("Osoba nije pronadjena!")
        print()
        return izmeni_osobu(osobe)

    ime, prezime, god_rodjenja = unesi_ime_prezime_god_rodjenja()
    pronadjena_osoba["ime"] = ime
    pronadjena_osoba["prezime"] = prezime
    pronadjena_osoba["god_rodjenja"] = god_rodjenja

def obrisi_osobu(osobe):
    print()
    print("Brisanje osobe: ")

    jmbg = ""
    while len(jmbg) < 13 or not jmbg.isdigit():
        jmbg = input("Unesite JMBG: ")

    pronadjena_osoba = pronadji_osobu(osobe, jmbg)
    if pronadjena_osoba is None:
        print()
        print("Osoba nije pronadjena!")
        print()
        return obrisi_osobu(osobe)

    osobe.remove(pronadjena_osoba)

def test():
    #recnici koji grupisu podatke o osobama u strukture
    osoba1 = {
        "jmbg": "1111111111111",
        "ime": "Jovan",
        "prezime": "Jovanovic",
        "god_rodjenja": 2001
    }

    osoba2 = {
        "jmbg": "2222222222222",
        "ime": "Nikola",
        "prezime": "Nikolic",
        "god_rodjenja": 2002
    }

    prikazi_osobu(osoba1)
    prikazi_osobu(osoba2)

    # predefinisana lista osoba
    osobe = [
        osoba1,
        osoba2
    ]
    prikazi_osobe(osobe)

    unesi_osobu(osobe)
    prikazi_osobe(osobe)

    izmeni_osobu(osobe)
    prikazi_osobe(osobe)

    obrisi_osobu(osobe)
    prikazi_osobe(osobe)

# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()
