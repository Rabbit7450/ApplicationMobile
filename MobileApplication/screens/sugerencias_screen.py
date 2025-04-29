from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class SugerenciasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Sugerencias y Comentarios',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Envía tus sugerencias para mejorar la aplicación',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Campo de texto para sugerencias
        self.sugerencia_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=200,
            hint_text='Escribe tu sugerencia aquí...'
        )
        main_layout.add_widget(self.sugerencia_input)

        # Botón para enviar sugerencia
        enviar_button = Button(
            text='Enviar Sugerencia',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        enviar_button.bind(on_press=self.enviar_sugerencia)
        main_layout.add_widget(enviar_button)

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

    def enviar_sugerencia(self, instance):
        sugerencia = self.sugerencia_input.text
        if sugerencia.strip():
            # Aquí se implementará la lógica para guardar la sugerencia
            print(f"Sugerencia enviada: {sugerencia}")
            self.sugerencia_input.text = ''
        else:
            print("Por favor, escribe una sugerencia")

    def switch_to_home(self):
        self.manager.current = 'home'
