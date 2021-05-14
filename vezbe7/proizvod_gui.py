from tkinter import *
from tkinter import messagebox

from vezbe7.proizvod import *  # moraju se import-ovati sve klase iz modula da bi serijalizacija/deserijalizacija radili


class ProizvodiProzor(Tk):  # glavni prozor

    # čisti sve labele za prikaz
    def ocisti_labele(self):
        self.__sifra_labela["text"] = ""
        self.__naziv_labela["text"] = ""
        self.__cena_labela["text"] = ""
        self.__proizvodjac_labela["text"] = ""

    # popunjava labele za prikaz vrednostima atributa proizvoda
    def popuni_labele(self, proizvod):
        self.__sifra_labela["text"] = proizvod.sifra
        self.__naziv_labela["text"] = proizvod.naziv
        self.__cena_labela["text"] = str(proizvod.cena)
        self.__proizvodjac_labela["text"] = proizvod.proizvodjac.naziv

    def popuni_proizvodi_listbox(self, proizvodi):
        self.__proizvodi_listbox.delete(0, END)  # obrisati sve unose iz Listbox-a
        for proizvod in proizvodi:  # za svaki proizvod iz liste
            self.__proizvodi_listbox.insert(END, proizvod.naziv)  # napravi jedan unos u listi

        self.ocisti_labele()  # Listbox će izgubiti prethodnu selekciju; ne želimo da labele prikazuju bilo šta ako ništa nije selektovano

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__proizvodi_listbox.curselection():  # ako ništa nije obeleženo u Listbox-u
            self.ocisti_labele()
            return

        # u suprotnom popuniti labele podacima trenutno obeleženog proizvoda
        indeks = self.__proizvodi_listbox.curselection()[0]
        proizvod = self.__podaci.proizvodi[indeks]
        self.popuni_labele(proizvod)  # popuniti labele vrednostima atributa proizvoda

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Proizvodi", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()

    def komanda_ocisti(self):
        self.__proizvodi_listbox.selection_clear(0, END)
        self.promena_selekcije_u_listbox()

    def komanda_o_aplikaciji(self):
        messagebox.showinfo("Proizvodi", "Proizvodi v1.0")

    def __init__(self, podaci):
        super().__init__()

        self.__podaci = podaci  # podaci se čuvaju kao privatni atribut radi pristupa u ostalim metodama

        # pravljenje GUI-a
        # roditelj većine komponenata (widget-a) bi trebalo da bude frame, ili prozor (Tk)
        # ako će komponenti morati da se pristupa kasnije, potrebno je sačuvati njenu referencu kao privatni atribut klase
        # ////////////////////////////////////////////////////////////////////////////////////////
        self.__proizvodi_listbox = Listbox(self, activestyle="none")  # roditelj Listbox-a u ovom slučaju je glavni prozor, activestyle stil kada je element aktivan
        # pack je jedan od layout manager-a (služi za grubo raspoređivanje komponenata u odnosu na roditelja)
        # jedna roditeljska komponenta ne sme da ima 2 različita layout manager-a; za glavni prozor u ovom slučaju je to pack
        self.__proizvodi_listbox.pack(side=LEFT, fill=BOTH, expand=1)  # Listbox će da zauzme levi deo prozora i moći će da se širi po obe dimenzije; side može imati vrednost (LEFT, RIGHT, TOP, BOTTOM), a fill (X, Y i BOTH)
        #expand je dodavanje dodatnog prostora za kontejner od vidzeta
        # jedan od načina povezivanja callback funkcije sa komponentom
        # 1. parametar je identifikator događaja
        # 2. parametar je callback funkcija
        self.__proizvodi_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        # ako će na komponentu morati da se kače druge komponente, potrebno je sačuvati njenu referencu kao lokalnu promenljivu
        # svaka komponenta je naslednik rečnika; vrednosti se mogu zadati imenovanim argumentima kroz konstruktor, ili direktnom manipulacijom preko istoimenih ključeva u bilo kom momentu
        # frame služi za grupisanje komponenata
        proizvod_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)  # roditelj Frame-a u ovom slučaju je glavni prozor
        proizvod_frame.pack(side=RIGHT, fill=BOTH, expand=1)  # frame će da zauzme desni deo prozora i moći će da se širi po obe dimenzije

        # roditelj svih labela u ovom slučaju je proizvod_frame
        self.__sifra_labela = Label(proizvod_frame)  # labela je komponenta koja može da prikaže proizvoljan tekst i izmenljiva je isključivo programskim putem
        self.__naziv_labela = Label(proizvod_frame)
        self.__cena_labela = Label(proizvod_frame)
        self.__proizvodjac_labela = Label(proizvod_frame)

        # grid je jedan od layout manager-a; služi da organizuje komponente po vrstama i kolonama u roditeljskoj komponenti
        # ako se kolona ne navede, podrazumevana je 0-ta kolona
        # jedna roditeljska komponenta ne sme da ima 2 različita layout manager-a; za proizvod_frame u ovom slučaju je to grid
        red = 0
        Label(proizvod_frame, text="šifra:").grid(row=red, sticky=E)  # sticky argument određuje horinzotalno poravnanje kolone (E, W), odnosno vertikalno poravnanje reda (N, S)
        red += 1
        Label(proizvod_frame, text="naziv:").grid(row=red, sticky=E)
        red += 1
        Label(proizvod_frame, text="cena:").grid(row=red, sticky=E)
        red += 1
        Label(proizvod_frame, text="proizvođač:").grid(row=red, sticky=E)
        red += 1

        red = 0
        kolona = 1
        self.__sifra_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__naziv_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__cena_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__proizvodjac_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        # jedan od načina povezivanja callback funkcije sa komponentom; tipično se koristi za dugmad
        # command argument povezuje callback funkciju sa komponentom
        Button(proizvod_frame, text="Očisti", width=10, command=self.komanda_ocisti).grid(row=red, column=kolona, sticky=W)

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)# tearoff znaci da li moze da se otkaci
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        proizvod_meni = Menu(meni_bar, tearoff=0)
        proizvod_meni.add_command(label="Očisti", command=self.komanda_ocisti)
        meni_bar.add_cascade(label="Proizvod", menu=proizvod_meni)

        pomoc_meni = Menu(meni_bar, tearoff=0)
        pomoc_meni.add_command(label="O aplikaciji", command=self.komanda_o_aplikaciji)
        meni_bar.add_cascade(label="Pomoć", menu=pomoc_meni)

        self.config(menu=meni_bar)

        # jedan od načina povezivanja callback funkcije sa komponentom; koristi se za ugrađenu dugmad prozora
        # 1. parametar je identifikator događaja
        # 2. parametar je callback funkcija
        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)
        self.iconbitmap("@ftn.xbm")  # učitavanje ikonice prozora
        self.title("Proizvodi")  # naslov prozora

        self.update_idletasks()  # između ostalog forsira raspoređivanje komponenata pre prikazivanja prozora; neophodno za izračunavanje min. potrebne širine i visine
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)  # prozor ne sme biti manji od min. potrebnih dimenzija
        #self.maxsize(1280, 720)

        # programski izazvani događaji
        # ////////////////////////////
        self.popuni_proizvodi_listbox(self.__podaci.proizvodi)  # popuniti Listbox
        self.focus_force()  # fokusiran nakon prikazivanja


def main():
    podaci = Podaci.ucitaj()  # svi podaci

    proizvodi_prozor = ProizvodiProzor(podaci)  # glavni prozor; jedini se kreira bez roditelja; klasa Tk, ili njena naslednica
    # pokreće pozadinski GUI thread
    # program se ne završava nakon poziva ove funkcije, već traje sve dok se ne zatvori glavni prozor
    proizvodi_prozor.mainloop()


main()
