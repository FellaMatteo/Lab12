# model/model.py

import networkx as nx
from database.dao import DAO
from model.Rifugio import Rifugio
from model.Connessione import Connessione


class Model:
    def __init__(self):
        self._rifugi = None
        self._grafo = nx.Graph()
        self._idMap = {}
        self._pesoMinimo = float('inf')
        self._pesoMassimo = float('-inf')

        self._bestPath = []
        self._bestPathWeight = float('inf')
        self._sogliaS = 0

    def get_rifugi_da_db(self):
        if self._rifugi is None:
            self._rifugi = DAO.get_rifugi()
            self._idMap = {r.id: r for r in self._rifugi}
        return self._rifugi

    def build_weighted_graph(self, year: int):
        self.get_rifugi_da_db()
        self._grafo.clear()

        connessioni = DAO.get_connessioni_fino_a_anno(year)

        rifugi_coinvolti_id = set()
        for conn in connessioni:
            rifugi_coinvolti_id.add(conn.id_rifugio1)
            rifugi_coinvolti_id.add(conn.id_rifugio2)

        nodi_da_aggiungere = [self._idMap[id_r] for id_r in rifugi_coinvolti_id if id_r in self._idMap]
        self._grafo.add_nodes_from(nodi_da_aggiungere)

        self._pesoMinimo = float('inf')
        self._pesoMassimo = float('-inf')

        for conn in connessioni:
            u = self._idMap.get(conn.id_rifugio1)
            v = self._idMap.get(conn.id_rifugio2)

            if u is not None and v is not None:
                peso = conn.peso

                self._grafo.add_edge(u, v, weight=peso)

                if peso < self._pesoMinimo:
                    self._pesoMinimo = peso
                if peso > self._pesoMassimo:
                    self._pesoMassimo = peso

        if self._grafo.number_of_edges() == 0:
            self._pesoMinimo = 0
            self._pesoMassimo = 0

    def get_edges_weight_min_max(self):
        return self._pesoMinimo, self._pesoMassimo

    def count_edges_by_threshold(self, soglia):
        archi_minori_s = 0
        archi_maggiori_s = 0

        for u, v, data in self._grafo.edges(data=True):
            peso = data['weight']
            if peso < soglia:
                archi_minori_s += 1
            elif peso > soglia:
                archi_maggiori_s += 1

        return archi_minori_s, archi_maggiori_s

    def get_nodi_partenza(self):
        return list(self._grafo.nodes())

    def trova_cammino_minimo_networkx(self, nodo_partenza: Rifugio, soglia_s: float):
        if self._grafo.number_of_nodes() < 3:
            return []

        subgraph_nodes = list(self._grafo.nodes())
        subgraph_edges = [
            (u, v, d['weight'])
            for u, v, d in self._grafo.edges(data=True)
            if d['weight'] > soglia_s
        ]

        G_filtrato = nx.Graph()
        G_filtrato.add_nodes_from(subgraph_nodes)
        G_filtrato.add_weighted_edges_from(subgraph_edges)

        self._sogliaS = soglia_s
        self._bestPath = []
        self._bestPathWeight = float('inf')

        try:
            shortest_paths = nx.shortest_path(G_filtrato, source=nodo_partenza, weight='weight')
            shortest_weights = nx.shortest_path_length(G_filtrato, source=nodo_partenza, weight='weight')

            for nodo_fine, peso in shortest_weights.items():
                if nodo_fine == nodo_partenza:
                    continue

                path = shortest_paths[nodo_fine]

                if len(path) >= 3:
                    if peso < self._bestPathWeight:
                        self._bestPathWeight = peso
                        self._bestPath = path

        except Exception:
            pass

        return self._bestPath

    def trova_cammino_minimo_ricorsivo(self, nodo_partenza: Rifugio, soglia_s: float):
        if self._grafo.number_of_nodes() < 3:
            return []

        self._sogliaS = soglia_s
        self._bestPath = []
        self._bestPathWeight = float('inf')

        self._ricerca_ricorsiva(nodo_corrente=nodo_partenza,
                                cammino_corrente=[nodo_partenza],
                                peso_corrente=0)

        return self._bestPath

    def _ricerca_ricorsiva(self, nodo_corrente: Rifugio, cammino_corrente: list, peso_corrente: float):

        if len(cammino_corrente) >= 3:
            if peso_corrente < self._bestPathWeight:
                self._bestPathWeight = peso_corrente
                self._bestPath = list(cammino_corrente)

        if peso_corrente >= self._bestPathWeight:
            return

        for vicino in self._grafo.neighbors(nodo_corrente):

            if vicino in cammino_corrente:
                continue

            peso_arco = self._grafo[nodo_corrente][vicino]['weight']

            if peso_arco > self._sogliaS:
                self._ricerca_ricorsiva(nodo_corrente=vicino,
                                        cammino_corrente=cammino_corrente + [vicino],
                                        peso_corrente=peso_corrente + peso_arco)