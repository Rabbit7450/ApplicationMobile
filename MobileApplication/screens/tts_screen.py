from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

class TTSScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Text-to-Speech',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Escribe el texto que deseas convertir a voz',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Campo de texto para entrada
        self.text_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=200,
            hint_text='Escribe el texto aquí...'
        )
        main_layout.add_widget(self.text_input)

        # Selector de voz
        voice_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        voice_label = Label(text='Seleccionar voz:', size_hint_x=0.4)
        self.voice_spinner = Spinner(
            text='Voz 1',
            values=('Voz 1', 'Voz 2', 'Voz 3', 'Voz 4'),
            size_hint_x=0.6
        )
        voice_layout.add_widget(voice_label)
        voice_layout.add_widget(self.voice_spinner)
        main_layout.add_widget(voice_layout)

        # Botones de control
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Botón para reproducir
        play_button = Button(
            text='Reproducir',
            background_color=(0.2, 0.6, 1, 1)
        )
        play_button.bind(on_press=self.reproducir_texto)
        control_layout.add_widget(play_button)

        # Botón para pausar
        pause_button = Button(
            text='Pausar',
            background_color=(0.2, 0.6, 1, 1)
        )
        pause_button.bind(on_press=self.pausar_texto)
        control_layout.add_widget(pause_button)

        # Botón para detener
        stop_button = Button(
            text='Detener',
            background_color=(0.2, 0.6, 1, 1)
        )
        stop_button.bind(on_press=self.detener_texto)
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

    def reproducir_texto(self, instance):
        texto = self.text_input.text
        voz = self.voice_spinner.text
        if texto.strip():
            # Aquí se implementará la lógica de reproducción
            print(f"Reproduciendo texto con {voz}: {texto}")
        else:
            print("Por favor, escribe algún texto")

    def pausar_texto(self, instance):
        # Aquí se implementará la lógica de pausa
        print("Reproducción pausada")

    def detener_texto(self, instance):
        # Aquí se implementará la lógica de detención
        print("Reproducción detenida")

    def switch_to_home(self):
        self.manager.current = 'home'
