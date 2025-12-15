# UI/controller.py

import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)

        num_nodi = self._model._grafo.number_of_nodes()
        num_archi = self._model._grafo.number_of_edges()

        if num_nodi == 0:
            self._view.show_alert("Nessun rifugio o sentiero trovato per l'anno specificato.")
            self._view.lista_visualizzazione_1.controls.clear()
            self._view.page.update()
            return

        min_p, max_p = self._model.get_edges_weight_min_max()

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {num_nodi} nodi, {num_archi} archi")
        )
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))

        rifugi_options = [ft.dropdown.Option(str(rifugio.id), rifugio.nome)
                          for rifugio in self._model.get_nodi_partenza()]
        self._view.dd_partenza.options = rifugi_options
        self._view.dd_partenza.value = None

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_3.controls.clear()

        self._view.page.update()

    def handle_conta_archi(self, e):
        if self._model._grafo.number_of_nodes() == 0:
            self._view.show_alert("Devi prima creare il grafo (Crea Grafo).")
            return

        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()

        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range. Deve essere tra {min_p:.2f} e {max_p:.2f}.")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Archi < {soglia:.1f}: {minori}, Archi > {soglia:.1f}: {maggiori}")
        )

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.page.update()

    def handle_cammino_minimo(self, e):
        if self._model._grafo.number_of_nodes() == 0:
            self._view.show_alert("Devi prima creare il grafo (Crea Grafo).")
            return

        id_partenza_str = self._view.dd_partenza.value
        if id_partenza_str is None and self._model.get_nodi_partenza():
            id_partenza_str = str(self._model.get_nodi_partenza()[0].id)

        if id_partenza_str is None:
            self._view.show_alert("Errore: Impossibile determinare il rifugio di partenza.")
            return

        try:
            soglia_s = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia 'S'.")
            return

        try:
            id_partenza = int(id_partenza_str)
            nodo_partenza = self._model._idMap.get(id_partenza)
        except ValueError:
            self._view.show_alert("Errore nella selezione del rifugio.")
            return

        if nodo_partenza is None:
            self._view.show_alert("Rifugio selezionato non trovato nel grafo.")
            return

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text("Cammino minimo:", weight=ft.FontWeight.BOLD))

        path_nx = self._model.trova_cammino_minimo_networkx(nodo_partenza, soglia_s)

        if not path_nx:
            self._model._bestPath = []
            self._model._bestPathWeight = float('inf')
            path_finale = self._model.trova_cammino_minimo_ricorsivo(nodo_partenza, soglia_s)
        else:
            path_finale = path_nx

        self._stampa_risultato_cammino(path_finale)

        self._view.page.update()

    def _stampa_risultato_cammino(self, path: list):

        if not path:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Nessun cammino valido (almeno 2 archi) trovato."))
        else:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                peso = self._model._grafo[u][v]['weight']
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f"[{u.id}] {u.nome} --> [{v.id}] {v.nome} [peso: {peso:.1f}]")
                )