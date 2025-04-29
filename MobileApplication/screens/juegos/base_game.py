from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

class BaseGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título
        title = Label(
            text=self.get_title(),
            font_size='24sp',
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text=self.get_description(),
            font_size='16sp',
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(description)

        # Contenido del juego
        content = self.create_content()
        main_layout.add_widget(content)

        # Botón para volver
        back_button = Button(
            text='Volver a Juegos',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1)
        )
        back_button.bind(on_press=self.switch_to_games)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def get_title(self):
        """Método que debe ser sobrescrito por las clases hijas"""
        return "Juego Base"

    def get_description(self):
        """Método que debe ser sobrescrito por las clases hijas"""
        return "Descripción del juego"

    def create_content(self):
        """Método que debe ser sobrescrito por las clases hijas"""
        return BoxLayout()

    def switch_to_games(self, instance):
        """Volver a la pantalla de juegos"""
        self.manager.current = 'juegos' 