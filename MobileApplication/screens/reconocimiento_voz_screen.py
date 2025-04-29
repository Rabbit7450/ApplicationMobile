from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from utils.styles import COLORS, TEXT_STYLES, BUTTON_STYLES
from utils.microphone import MicrophoneManager
from utils.base_screen import BaseScreen

class ReconocimientoVozScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mic_manager = MicrophoneManager()
        self.setup_ui()

    def setup_ui(self):
        # Configurar el fondo
        with self.canvas.before:
            Color(*COLORS['background'])
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título
        title = Label(
            text='Reconocimiento de Voz',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)

        # Estado del micrófono
        self.status_label = Label(
            text='Micrófono listo',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.status_label)

        # Botón de grabación
        self.record_button = Button(
            text='Iniciar Grabación',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['primary']
        )
        self.record_button.bind(on_press=lambda x: self.handle_button_press(
            'record',
            lambda: self.toggle_recording(None),
            'Toque dos veces para iniciar/detener la grabación'
        ))
        layout.add_widget(self.record_button)

        # Botón de reproducción
        self.play_button = Button(
            text='Reproducir Grabación',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['accent']
        )
        self.play_button.bind(on_press=lambda x: self.handle_button_press(
            'play',
            lambda: self.play_recording(None),
            'Toque dos veces para reproducir la grabación'
        ))
        layout.add_widget(self.play_button)

        # Botón de regreso
        back_button = Button(
            text='Volver',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['primary_dark']
        )
        back_button.bind(on_press=lambda x: self.handle_button_press(
            'back',
            self.go_back,
            'Toque dos veces para volver al inicio'
        ))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def toggle_recording(self, instance):
        if not self.mic_manager.is_recording:
            # Iniciar grabación
            if self.mic_manager.start_recording(self.on_recording_started):
                self.record_button.text = 'Detener Grabación'
                self.status_label.text = 'Grabando...'
        else:
            # Detener grabación
            if self.mic_manager.stop_recording(self.on_recording_stopped):
                self.record_button.text = 'Iniciar Grabación'
                self.status_label.text = 'Grabación completada'

    def on_recording_started(self, success):
        if success:
            self.status_label.text = 'Grabando...'
        else:
            self.status_label.text = 'Error al iniciar la grabación'

    def on_recording_stopped(self, audio_file):
        if audio_file:
            self.status_label.text = 'Grabación guardada'
        else:
            self.status_label.text = 'Error al guardar la grabación'

    def play_recording(self, instance):
        if self.mic_manager.play_recording():
            self.status_label.text = 'Reproduciendo grabación...'
        else:
            self.status_label.text = 'No hay grabación para reproducir'

    def go_back(self):
        self.manager.current = 'home'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
