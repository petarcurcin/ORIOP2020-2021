def prikazi_proizvod(proizvod):
    print("\n".join([
        "",
        "{:>5}: {}".format("Šifra", proizvod["sifra"]),
        "{:>5}: {}".format("Naziv", proizvod["naziv"]),
        "{:>5}: {}".format("Cena", proizvod["cena"])
    ]))


def test():
    proizvod1 = {
        "sifra": "0001",
        "naziv": "Hleb 700g",
        "cena": 50.0
    }
    proizvod2 = {
        "sifra": "0002",
        "naziv": "Mleko 1l",
        "cena": 80.0
    }
    proizvod3 = {
        "sifra": "0003",
        "naziv": "Čokolada 100g",
        "cena": 120.0
    }
    prikazi_proizvod(proizvod1)
    prikazi_proizvod(proizvod2)
    prikazi_proizvod(proizvod3)

    print()
    proizvod1["cena"] = float(input("Unesite novu cenu za proizvod {}: ".format(proizvod1["naziv"])))
    print("Nova cena proizvoda {} je {}.".format(proizvod1["naziv"], proizvod1["cena"]))


# da li se modul pokreće samostalno, tj. da li nije import-ovan?
if __name__ == "__main__":
    test()
