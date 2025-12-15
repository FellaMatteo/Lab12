# UI/view.py

import flet as ft
from UI.alert import AlertManager


class View:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Lab12"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        self.alert = AlertManager(page)

        self.controller = None

        # Inizializzazione degli attributi UI
        self.txt_anno = None
        self.txt_soglia = None
        self.dd_partenza = None
        self.pulsante_cammino_minimo = None
        self.lista_visualizzazione_1 = None
        self.lista_visualizzazione_2 = None
        self.lista_visualizzazione_3 = None
        self.toggle_cambia_tema = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        self.txt_titolo = ft.Text(value="Gestione Sentieri di Montagna", size=38, weight=ft.FontWeight.BOLD)

        self.txt_anno = ft.TextField(label="Anno (1950-2024)", value="2000", width=200)
        pulsante_crea_grafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self.controller.handle_grafo if self.controller else None,
            width=200
        )
        row1 = ft.Row([self.txt_anno, pulsante_crea_grafo], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_1 = ft.ListView(expand=1, spacing=5, padding=15, auto_scroll=False, height=60)

        self.txt_soglia = ft.TextField(label="Soglia Peso", value="4", width=200)
        self.pulsante_conta_archi = ft.ElevatedButton("Conta Archi", width=200,
                                                      on_click=self.controller.handle_conta_archi if self.controller else None)
        row2 = ft.Row([self.txt_soglia, self.pulsante_conta_archi], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_2 = ft.ListView(expand=1, spacing=5, padding=15, auto_scroll=False, height=30)

        self.dd_partenza = ft.Dropdown(
            label="Rifugio di Partenza",
            width=200,
            options=[]
        )
        self.pulsante_cammino_minimo = ft.ElevatedButton(
            "Cammino Minimo",
            on_click=self.controller.handle_cammino_minimo if self.controller else None,
            width=200
        )
        row3_btn = ft.Row([self.pulsante_cammino_minimo], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_3 = ft.ListView(expand=1, spacing=5, padding=15, auto_scroll=False, height=100)

        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        self.page.add(
            ft.Row([self.toggle_cambia_tema], alignment=ft.MainAxisAlignment.START),

            self.txt_titolo,
            ft.Divider(),

            # Sezione 1: Grafo
            row1,
            self.lista_visualizzazione_1,
            ft.Divider(),

            # Sezione 2: Conteggio Archi
            row2,
            self.lista_visualizzazione_2,
            ft.Divider(),

            # Sezione 3: Cammino Minimo (Dropdown nascosta, pulsante visibile)
            ft.Container(self.dd_partenza, visible=False),
            row3_btn,
            self.lista_visualizzazione_3,
            ft.Divider(),
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()