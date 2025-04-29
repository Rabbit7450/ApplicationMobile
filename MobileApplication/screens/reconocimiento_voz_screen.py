from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class ReconocimientoVozScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Reconocimiento de Voz',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Presiona el botón y habla para convertir tu voz en texto',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Campo de texto para mostrar el resultado
        self.resultado_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=200,
            hint_text='El texto reconocido aparecerá aquí...',
            readonly=True
        )
        main_layout.add_widget(self.resultado_input)

        # Botones de control
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Botón para iniciar grabación
        record_button = Button(
            text='Iniciar Grabación',
            background_color=(0.2, 0.6, 1, 1)
        )
        record_button.bind(on_press=self.iniciar_grabacion)
        control_layout.add_widget(record_button)

        # Botón para detener grabación
        stop_button = Button(
            text='Detener Grabación',
            background_color=(0.2, 0.6, 1, 1)
        )
        stop_button.bind(on_press=self.detener_grabacion)
        control_layout.add_widget(stop_button)

        main_layout.add_widget(control_layout)

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

    def iniciar_grabacion(self, instance):
        # Aquí se implementará la lógica de inicio de grabación
        print("Iniciando grabación de voz...")
        self.resultado_input.text = "Grabando..."

    def detener_grabacion(self, instance):
        # Aquí se implementará la lógica de detención de grabación
        print("Deteniendo grabación...")
        self.resultado_input.text = "Texto reconocido: Hola, este es un ejemplo de reconocimiento de voz."

    def switch_to_home(self):
        self.manager.current = 'home'
