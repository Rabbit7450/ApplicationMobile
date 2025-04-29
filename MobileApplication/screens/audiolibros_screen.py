from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class AudiolibrosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Audiolibros',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # ScrollView para la lista de audiolibros
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Lista de audiolibros de ejemplo
        audiolibros = [
            'El Principito',
            'Don Quijote',
            'Cien años de soledad',
            'El señor de los anillos',
            'Harry Potter'
        ]

        for libro in audiolibros:
            btn = Button(
                text=libro,
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=lambda x, l=libro: self.reproducir_audiolibro(l))
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

    def reproducir_audiolibro(self, titulo):
        # Aquí se implementará la lógica de reproducción
        print(f"Reproduciendo: {titulo}")

    def switch_to_home(self):
        self.manager.current = 'home'
