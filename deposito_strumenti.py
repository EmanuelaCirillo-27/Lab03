import csv

from prestito import Prestito
from strumento import Strumento
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome=nome # Inizializzo il nome del deposito
        self.__responsabile=responsabile # Inizializzo il nome del responsabile

        self.strumenti=[] # Lista per tener traccia di tutti gli strumenti letti dal file/aggiunti da tastiera
        self.prestito=[] # Lista per tener traccia dei prestiti effettuati

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, new_responsabile):
        self.__responsabile=new_responsabile

    def __str__(self):
        return f' {self.__responsabile}'

    # Avendo definito il nome del responsabile con __, cioè come attributo privato, utilizzo i metodi getter e
    # setter per permettere all'utente di modificarlo

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:

            with open(file_path, 'r', encoding='utf8') as f:
                reader = csv.reader(f)

                # Una volta aperto il file in lettura, scandisco riga per riga e assegno ad ogni elemento di essa
                # un nominativo per poi andare a caratterizzare il singolo strumento grazie alla classe Strumento,
                # la quale è costituita dagli attributi codice, tipo, marca, anno_acquisto e valore.
                # Dopo aver definito lo strumento lo inserisco all'interno della lista strumenti che definirà così
                # un sistema con all'interno tutti gli strumenti

                for row in reader:
                    codice = row[0]
                    tipo = row[1]
                    marca = row[2]
                    anno_acquisto = int(row[3])
                    valore = float(row[4])
                    strumento=Strumento(codice, tipo, marca, anno_acquisto, valore)
                    self.strumenti.append(strumento)

            return self.strumenti


        except FileNotFoundError:
            return 'File non trovato'


    def crea_codice(self, strumenti):
        # Questa funzione prende tutti i codici presenti all'interno del file csv e li mette dentro una lista
        codici=[]

        for row in strumenti:
            codici.append(row.codice)

        # Mi interessa prendere l'ultimo codice di questa lista in quanto devo creare un nuovo codice che si incrementa
        # a partire dall'ultimo presente, e in particolare vado a prendere solo la parte numerica
        ultimo=codici[-1]
        ultimo_num=ultimo[1:]

        # Incremento la parte numerica del codice e poi creo il nuovo codice definendolo come stringa
        nuovo_num=int(ultimo_num)+1
        nuovo_codice='S'+str(nuovo_num)

        return nuovo_codice



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        # La funzione aggiungi_strumento non riceveva in input il codice, perciò creo una funzione crea_codice
        # che mi restituisce il codice da assegnare allo strumento inserito da tastiera

        codice=self.crea_codice(self.strumenti)

        # Utilizzo la classe Strumento per definire il nuovo strumento e poi lo aggiungo nel sistema
        nuovo_strumento=Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # Utilizzo la funzione sorted per poter ordinare per marca gli strumenti
        return sorted(self.strumenti, key=attrgetter('marca'))


    def crea_id(self,prestito):

        # La funzione controlla se ci siano mai stati dei prestiti, in caso negativo definisce l'id del primo prestito
        if not prestito:
            return 'P1'

        # Se già sono stati fatti dei prestiti, allora prendo l'ultimo prestito fatto e in particolare la parte
        # numerica del suo id, andandolo ad incrementare in seguito al nuovo prestito e creare così l'id del nuovo
        # prestito
        ultimo=prestito[-1]
        ultimo_id=ultimo.id_prestito
        ultimo_prestito_num=ultimo_id[1:]

        nuovo_num_prestito=int(ultimo_prestito_num)+1
        nuovo_prestito='P'+str(nuovo_num_prestito)

        return nuovo_prestito

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""

        # Definisco id_prestito tramite una funzione creata precedentemente crea_id

        id_prestito=self.crea_id(self.prestito)

        # Creo la lista strumenti_già_in_prestito per mettere al suo interno tutti quegli strumenti che sono
        # ancora in prestito, poi tramite un if si controlla se l'id_strumento è già presente in questa lista e in caso
        # positivo scatena l'eccezione
        # Un procedimento simile avviene con la lista strumenti_tot, che al suo interno contiene tutti i codici degli
        # strumenti presenti proprio nel sistema, per poi tramite un if scatenare un'eccezione se l'id_strumento dato
        # non esista nel sistema
        strumenti_già_in_prestito=[]
        strumenti_tot=[]

        for el in self.prestito:
            strumenti_già_in_prestito.append(el.id_strumento)

        for elemento in self.strumenti:
            strumenti_tot.append(elemento.codice)


        if id_strumento in strumenti_già_in_prestito or id_strumento not in strumenti_tot:
            raise Exception("Strumento non trovato o già in prestito")

        # Utilizzo la classe Prestito per definire il nuovo prestito, per poi aggiungerlo nella lista dei prestiti
        # definita sopra
        prestato=Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestito.append(prestato)

        return prestato

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""

        # Creo una lista che al suo interno contiene tutti gli id_prestito dei prestiti effettuati
        strumenti_prestati=[]

        for el in self.prestito:
            strumenti_prestati.append(el.id_prestito)

        # Controlla se l'id dato in input sia all'interno della lista, se non è così scatena un'eccezione
        if id_prestito not in strumenti_prestati:
            raise Exception("Prestito non trovato")

        # Prendo riga per riga i prestiti dalla mia lista di tutti i prestiti effettuati, vedo se, per ogni riga,
        # l'id di essa corrisponde con quello dato da tastiera, in caso affermativo definisco prestito_da_togliere
        # la riga che contiene l'id_prestito di cui si vuole terminare il prestito
        for elemento in self.prestito:
            if elemento.id_prestito==id_prestito:
                prestito_da_togliere=elemento

                self.prestito.remove(prestito_da_togliere) # Elimino la riga che contiene l'id_prestito
                                                           # di cui voglio terminare il prestito
