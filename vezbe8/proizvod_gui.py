from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox

from vezbe8.proizvod import *  # moraju se import-ovati sve klase iz modula da bi serijalizacija/deserijalizacija radili


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
            self.__proizvodi_listbox.insert(END, "{}: {}".format(proizvod.sifra, proizvod.naziv))  # napravi jedan unos u listi

        self.ocisti_labele()  # Listbox će izgubiti prethodnu selekciju; ne želimo da labele prikazuju bilo šta ako ništa nije selektovano

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__proizvodi_listbox.curselection():  # ako ništa nije obeleženo u Listbox-u
            self.ocisti_labele()

            # blokirati dugmad za izmenu i brisanje
            self.__izmeni_button['state'] = DISABLED
            self.__proizvod_meni.entryconfig(2, state=DISABLED)
            self.__ukloni_button['state'] = DISABLED
            self.__proizvod_meni.entryconfig(3, state=DISABLED)
            return

        # u suprotnom popuniti labele podacima trenutno obeleženog proizvoda
        indeks = self.__proizvodi_listbox.curselection()[0]
        proizvod = self.__podaci.proizvodi[indeks]
        self.popuni_labele(proizvod)  # popuniti labele vrednostima atributa proizvoda

        # osposobiti dugmad za izmenu i brisanje
        self.__izmeni_button['state'] = NORMAL
        self.__proizvod_meni.entryconfig(2, state=NORMAL)
        self.__ukloni_button['state'] = NORMAL
        self.__proizvod_meni.entryconfig(3, state=NORMAL)

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Proizvodi", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()

    def komanda_ocisti(self):
        self.__proizvodi_listbox.selection_clear(0, END)  # ponišenje obeležavanja u listbox-u
        self.promena_selekcije_u_listbox()  # na svaku promenu obeležavanja

    def komanda_dodaj(self):
        dodavanje_proizvoda_prozor = DodavanjeProizvodaProzor(self, self.__podaci)  # kreiranje i prikaz prozora za dodavanje
        self.wait_window(dodavanje_proizvoda_prozor)  # čekanje da se prozor zatvori
        if dodavanje_proizvoda_prozor.otkazano:  # da li je unos potvrđen?
            return

        proizvod = self.__podaci.proizvodi[-1]  # dodati proizvod je na kraju liste

        self.__proizvodi_listbox.selection_clear(0, END)  # ponišenje obeležavanja u listbox-u
        self.__proizvodi_listbox.insert(END, "{}: {}".format(proizvod.sifra, proizvod.naziv))  # dodavanje proizvoda na kraj listbox-a
        self.__proizvodi_listbox.selection_set(END)  # obeležavanja dodatog proizvoda u listbox-u
        self.promena_selekcije_u_listbox()  # na svaku promenu obeležavanja

    def komanda_izmeni(self):
        # priprema trenutno obeleženog proizvoda za izmenu
        indeks = self.__proizvodi_listbox.curselection()[0]
        proizvod = self.__podaci.proizvodi[indeks]

        izmena_proizvoda_prozor = IzmenaProizvodaProzor(self, self.__podaci, proizvod)  # kreiranje i prikaz prozora za izmenu
        self.wait_window(izmena_proizvoda_prozor)
        if izmena_proizvoda_prozor.otkazano:
            return

        self.__proizvodi_listbox.delete(indeks)  # uklanjanje starog proizvoda iz listbox-a
        self.__proizvodi_listbox.insert(indeks, "{}: {}".format(proizvod.sifra, proizvod.naziv))  # dodavanje novog proizvod u listbox na isto mesto
        self.__proizvodi_listbox.selection_set(indeks)  # obeležavanje dodatog proizvoda
        self.promena_selekcije_u_listbox()  # na svaku promenu obeležavanja

    def komanda_obrisi(self):
        if messagebox.askquestion("Upozorenje", "Da li ste sigurni?", icon="warning") == "no":
            return

        # brisanje trenutno obeleženog proizvoda u podacima
        indeks = self.__proizvodi_listbox.curselection()[0]
        self.__podaci.obrisi_proizvod(indeks)

        self.config(cursor="wait")
        self.update()
        self.__podaci.sacuvaj_se()  # čuvanje nakon dodavanja, izmene i brisanja
        self.config(cursor="")

        self.__proizvodi_listbox.delete(indeks)  # uklanjanje proizvoda iz listbox-a po indeksu
        self.__proizvodi_listbox.selection_set(indeks)  # obeležavanje sledećeg proizvoda (koji je sada zauzeo poziciju obrisanog proizvoda) u listbox-u, ako postoji
        self.promena_selekcije_u_listbox()  # na svaku promenu obeležavanja

    def komanda_o_aplikaciji(self):
        messagebox.showinfo("Proizvodi", "Proizvodi v1.0")

    def __init__(self, podaci):
        super().__init__()

        self.__podaci = podaci  # podaci se čuvaju kao privatni atribut radi pristupa u ostalim metodama

        # pravljenje GUI-a
        # roditelj većine komponenata (widget-a) bi trebalo da bude frame, ili prozor (Tk)
        # ako će komponenti morati da se pristupa kasnije, potrebno je sačuvati njenu referencu kao privatni atribut klase
        # ////////////////////////////////////////////////////////////////////////////////////////
        self.__proizvodi_listbox = Listbox(self, activestyle="none", exportselection=False)  # roditelj Listbox-a u ovom slučaju je glavni prozor
        # pack je jedan od layout manager-a (služi za grubo raspoređivanje komponenata u odnosu na roditelja)
        # jedna roditeljska komponenta ne sme da ima 2 različita layout manager-a; za glavni prozor u ovom slučaju je to pack
        self.__proizvodi_listbox.pack(side=LEFT, fill=BOTH, expand=1)  # Listbox će da zauzme levi deo prozora i moći će da se širi po obe dimenzije; side može imati vrednost (LEFT, RIGHT, TOP, BOTTOM), a fill (X, Y i BOTH)
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

        # jedan od 2 načina povezivanja callback funkcije sa komponentom; tipično se koristi za dugmad
        # command argument povezuje callback funkciju sa komponentom
        self.__dodaj_button = Button(proizvod_frame, text="Dodaj", width=10, command=self.komanda_dodaj)
        self.__izmeni_button = Button(proizvod_frame, text="Izmeni", width=10, state=DISABLED, command=self.komanda_izmeni)
        self.__ukloni_button = Button(proizvod_frame, text="Obriši", width=10, state=DISABLED, command=self.komanda_obrisi)

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
        Button(proizvod_frame, text="Očisti", width=10, command=self.komanda_ocisti).grid(row=red, column=kolona, sticky=W)
        red += 1

        self.__dodaj_button.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__izmeni_button.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__ukloni_button.grid(row=red, column=kolona, sticky=W)
        red += 1

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        self.__proizvod_meni = Menu(meni_bar, tearoff=0)
        self.__proizvod_meni.add_command(label="Očisti", command=self.komanda_ocisti)
        self.__proizvod_meni.add_command(label="Dodaj", command=self.komanda_dodaj)
        self.__proizvod_meni.add_command(label="Izmeni", state=DISABLED, command=self.komanda_izmeni)
        self.__proizvod_meni.add_command(label="Obriši", state=DISABLED, command=self.komanda_obrisi)
        meni_bar.add_cascade(label="Proizvod", menu=self.__proizvod_meni)

        pomoc_meni = Menu(meni_bar, tearoff=0)
        pomoc_meni.add_command(label="O aplikaciji", command=self.komanda_o_aplikaciji)
        meni_bar.add_cascade(label="Pomoć", menu=pomoc_meni)

        self.config(menu=meni_bar)

        # jedan od načina povezivanja callback funkcije sa komponentom; koristi se za ugrađenu dugmad prozora
        # 1. parametar je identifikator događaja
        # 2. parametar je callback funkcija
        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)
        self.iconbitmap("ftn.ico")  # učitavanje ikonice prozora
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


class ProizvodProzor(Toplevel):  # TopLevel je svaki prozor koji nije glavni prozor

    # metode koje validiraju unesene vrednosti u komponentama i vraćaju ih, ili vraćaju None u suprotnom
    def sifra_validacija(self):
        sifra = self.__sifra.get()  # get metoda čita vrednost StringVar, IntVar i sl. objekata, odnosno komponenata sa kojima su povezani
        if len(sifra) != 4:
            messagebox.showerror("Greška", "Šifra mora sadržati tačno 4 karaktera!")  # menja se tekst labele za ispis poruke
            return None

        return sifra

    def naziv_validacija(self):
        naziv = self.__naziv.get()
        if naziv == "":
            messagebox.showerror("Greška", "Naziv ne sme biti prazan!")
            return None

        return naziv

    def cena_validacija(self):
        try:
            cena = self.__cena.get()
            if cena <= 0:
                messagebox.showerror("Greška", "Cena mora biti broj veći od 0!")
                return None
        except TclError:
            messagebox.showerror("Greška", "Cena mora biti broj!")
            return None

        return cena

    def proizvodjac_validacija(self):
        indeks = self.__proizvodjac_combobox.current()
        if indeks < 0:
            messagebox.showerror("Greška", "Proizvođač nije odabran!")
            return None

        indeks = self.proizvodjac_combobox.current()
        proizvodjac = self.podaci.proizvodjaci[indeks]
        return proizvodjac

    def komanda_ok(self):
        self.config(cursor="wait")
        self.update()
        self.podaci.sacuvaj_se()  # čuvanje nakon dodavanja, izmene i brisanja
        self.config(cursor="")

        self.__otkazano = False  # prozor nije zatvoren klikom na [x]
        self.destroy()  # u slučaju potvrde dodavanja i izmene, dijalog se uvek zatvara

    def __init__(self, master, podaci):
        super().__init__(master)  # svaka komponenta osim root-a mora da ima roditelja

        self.__otkazano = True  # ukoliko se zatvori klikom na [x], ostaće True

        self.__podaci = podaci  # prosleđeni podaci; privatni atribut radi pristupa u ostalim metodama

        # priprema proizvođača za dodavanje u combobox (niže)
        proizvodjaci = []
        for proizvodjac in self.__podaci.proizvodjaci:
            proizvodjaci.append(proizvodjac.naziv)

        # objekti promenljivih vrednosti koji se mogu povezati sa većinom komponenata
        # njihovom promenom se automaski ažurira prikaz u povezanoj komponenti
        # njihova vrednost se automatski ažurira izmenom vrednosti povezane komponente
        self.__sifra = StringVar(master)  # svaka komponenta osim root-a mora da ima roditelja; StringVar, IntVar i sl. se povezuju direktno sa root-om
        self.__naziv = StringVar(master)
        self.__cena = DoubleVar(master)

        # pravljenje GUI-a
        # ////////////////////////////////////////////////////////////////////////////////////////
        proizvod_frame = Frame(self, padx=5, pady=5)
        proizvod_frame.pack(expand=1)

        self.__sifra_entry = Entry(proizvod_frame, width=20, textvariable=self.__sifra)  # textvariable argument povezuje StringVar, IntVar i sl. objekte sa komponentom
        self.__naziv_entry = Entry(proizvod_frame, width=20, textvariable=self.__naziv)
        self.__cena_spinbox = Spinbox(proizvod_frame, width=20, from_=0.0, increment=0.01, to=float("inf"), format="%.2f", textvariable=self.__cena)

        self.__proizvodjac_combobox = Combobox(proizvod_frame, state="readonly", values=proizvodjaci)
        # obeležavanje prvog proizvođača ako postoji
        if len(proizvodjaci) > 0:
            self.__proizvodjac_combobox.current(0)

        self.__ok_button = Button(proizvod_frame, width=10, command=self.komanda_ok)

        red = 0
        Label(proizvod_frame, text="šifra:").grid(row=red, sticky=E)
        red += 1
        Label(proizvod_frame, text="naziv:").grid(row=red, sticky=E)
        red += 1
        Label(proizvod_frame, text="cena:").grid(row=red, sticky=E)
        red += 1
        Label(proizvod_frame, text="proizvođač:").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__sifra_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__naziv_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__cena_spinbox.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__proizvodjac_combobox.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__ok_button.grid(row=red, column=kolona, sticky=W)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        self.iconbitmap("ftn.ico")
        self.transient(master)  # prozor se ne pojavljuje se u taskbar-u, već samo njegov roditelj

        # programski izazvani događaji
        # ////////////////////////////
        self.focus_force()
        self.grab_set()  # modalni

    # indikator roditelju prozora da li je prozor zatvoren klikom na [x]
    @property
    def otkazano(self):
        return self.__otkazano

    # sledeće property metode su potrebne radi pristupa ovim atributima u klasama naslednicama
    @property
    def podaci(self):
        return self.__podaci

    @property
    def sifra(self):
        return self.__sifra

    @property
    def naziv(self):
        return self.__naziv

    @property
    def cena(self):
        return self.__cena

    @property
    def sifra_entry(self):
        return self.__sifra_entry

    @property
    def proizvodjac_combobox(self):
        return self.__proizvodjac_combobox

    @property
    def ok_button(self):
        return self.__ok_button


class DodavanjeProizvodaProzor(ProizvodProzor):

    # čitaju se i validiraju svi unosi, od njih se kreira proizvod i na kraju se on dodaje u prosleđene podatke
    def komanda_ok(self):
        sifra = self.sifra_validacija()
        if not sifra:
            return
        naziv = self.naziv_validacija()
        if not naziv:
            return
        cena = self.cena_validacija()
        if not cena:
            return
        proizvodjac = self.proizvodjac_validacija()
        if not proizvodjac:
            return

        # kreiranje novog proizvoda i dodavanje u podatke
        proizvod = Proizvod(sifra, naziv, cena, proizvodjac)
        self.podaci.dodaj_proizvod(proizvod)

        super().komanda_ok()

    def __init__(self, master, podaci):
        super().__init__(master, podaci)

        # dopuna GUI-a
        # ////////////////////////////////////////////////////////////////////////////////////////
        self.ok_button['text'] = "Dodaj"

        self.title("Dodavanje proizvoda")


class IzmenaProizvodaProzor(ProizvodProzor):

    # čitaju se i validiraju svi unosi osim šifre, a zatim se na osnovu njih modifikuju atributi prosleđenog proizvoda
    def komanda_ok(self):
        naziv = self.naziv_validacija()
        if not naziv:
            return
        cena = self.cena_validacija()
        if not cena:
            return
        proizvodjac = self.proizvodjac_validacija()
        if not proizvodjac:
            return

        # izmena proizvoda
        self.__proizvod.naziv = naziv
        self.__proizvod.cena = cena
        self.__proizvod.proizvodjac = proizvodjac

        super().komanda_ok()

    def __init__(self, master, podaci, proizvod):
        super().__init__(master, podaci)

        self.__proizvod = proizvod  # prosleđen proizvod za izmenu; privatni atribut radi pristupa u ostalim metodama

        # popunjavanje komponenata na osnovu atributa prosleđenog proizvoda
        self.sifra.set(self.__proizvod.sifra)
        self.naziv.set(self.__proizvod.naziv)
        self.cena.set(self.__proizvod.cena)

        proizvodjaci = self.podaci.proizvodjaci
        # pronalaženje indeksa proizvođača koji odgovara proizvodu
        for indeks in range(len(proizvodjaci)):
            proizvodjac = proizvodjaci[indeks]
            if proizvodjac == proizvod.proizvodjac:  # ako proizvođač na tekućem indeksu odgovara proizvodu
                self.proizvodjac_combobox.current(indeks)  # obeležavanje proizvođača u combobox-u na tekućem indeksu
                break

        # dopuna GUI-a
        # ////////////////////////////////////////////////////////////////////////////////////////
        self.sifra_entry['state'] = DISABLED  # zabrana izmene šifre
        self.ok_button['text'] = "Izmeni"

        self.title("Izmena proizvoda")


def main():
    podaci = Podaci.ucitaj()  # svi podaci

    proizvodi_prozor = ProizvodiProzor(podaci)  # glavni prozor; jedini se kreira bez roditelja; klasa Tk, ili njena naslednica
    # pokreće pozadinski GUI thread
    # program se ne završava nakon poziva ove funkcije, već traje sve dok se ne zatvori glavni prozor
    proizvodi_prozor.mainloop()


main()
