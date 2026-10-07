import csv

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome=nome
        self.__responsabile=responsabile

        self.__strumenti=[]

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, new_responsabile):
        self.__responsabile=new_responsabile


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:

            with open(file_path, 'r', encoding='utf8') as f:
                f.readline()
                reader = csv.reader(f)

                for row in reader:
                    codice = row[0]
                    tipo = row[1]
                    marca = row[2]
                    anno_acquisto = row[3]
                    valore = row[4]
                    nuovi_strumenti=([codice, tipo, marca, anno_acquisto, valore])
                    self.__strumenti.append(nuovi_strumenti)


        except FileNotFoundError:
            return 'File non trovato'

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # TODO

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # TODO

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # TODO

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
