class Connessione:
    def __init__(self, id_rifugio1, id_rifugio2, distanza, difficolta, durata, anno):
        self.id_rifugio1 = id_rifugio1
        self.id_rifugio2 = id_rifugio2
        self.distanza = distanza
        self.difficolta = difficolta
        self.durata = durata
        self.anno = anno

    def get_fattore_difficolta(self):
        diff_map = {
            'facile': 1,
            'media': 1.5,
            'difficile': 2
        }
        return diff_map.get(self.difficolta.lower(), 1)

    @property
    def peso(self):
        return float(self.distanza) * self.get_fattore_difficolta()

    def __str__(self):
        return f"Sentiero tra {self.id_rifugio1} e {self.id_rifugio2} (Peso: {self.peso:.2f})"

    def __repr__(self):
        return f"Connessione(r1={self.id_rifugio1}, r2={self.id_rifugio2}, dist={self.distanza}, diff='{self.difficolta}', anno={self.anno})"