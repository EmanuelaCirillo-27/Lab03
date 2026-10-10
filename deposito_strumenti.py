import csv
from strumento import Strumento
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome=nome
        self.__responsabile=responsabile

        self.strumenti=[]

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, new_responsabile):
        self.__responsabile=new_responsabile

    def __str__(self):
        return f' {self.__responsabile}'


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:

            with open(file_path, 'r', encoding='utf8') as f:
                reader = csv.reader(f)


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

        codici=[]

        for row in strumenti:
            codici.append(row.codice)

        ultimo=codici[-1]
        ultimo_num=ultimo[1:]

        nuovo_num=int(ultimo_num)+1
        nuovo_codice='S'+str(nuovo_num)

        return nuovo_codice



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        codice=self.crea_codice(self.strumenti)

        nuovo_strumento=Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter('marca'))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # TODO

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
