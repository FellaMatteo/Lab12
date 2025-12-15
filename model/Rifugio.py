

class Rifugio:
    def __init__(self, id, nome, localita, altitudine, capienza, aperto):
        self.id = id
        self.nome = nome
        self.localita = localita
        self.altitudine = altitudine
        self.capienza = capienza
        self.aperto = aperto

    def __str__(self):
        return f"{self.nome} ({self.localita}, Alt: {self.altitudine}m)"

    def __repr__(self):
        return f"Rifugio(id={self.id}, nome='{self.nome}')"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Rifugio) and self.id == other.id