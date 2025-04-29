from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class JuegosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Juegos Educativos',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Selecciona un juego para comenzar',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # ScrollView para la lista de juegos
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Lista de juegos de ejemplo
        juegos = [
            'Memoria Auditiva',
            'Adivina el Sonido',
            'Sigue el Ritmo',
            'Palabras en Braille',
            'Orientación Espacial'
        ]

        for juego in juegos:
            btn = Button(
                text=juego,
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=lambda x, j=juego: self.iniciar_juego(j))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        # Botón para volver a la pantalla principal
        back_button = Button(
            text='Volver al Inicio',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.switch_to_home())
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def iniciar_juego(self, nombre_juego):
        # Aquí se implementará la lógica de inicio del juego
        print(f"Iniciando juego: {nombre_juego}")

    def switch_to_home(self):
        self.manager.current = 'home'
