from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from utils.styles import COLORS, TEXT_STYLES, BUTTON_STYLES
from utils.text_to_audio import TextToAudioConverter
from utils.base_screen import BaseScreen

class ConversionAudioScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.converter = TextToAudioConverter()
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
            text='Conversión de Texto a Audio',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)

        # Instrucciones
        instructions = Label(
            text='Pega el texto que deseas convertir a audio:',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(instructions)

        # Campo de texto para el contenido
        self.text_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=dp(200),
            hint_text='Pega aquí el texto del libro...',
            background_color=COLORS['white'],
            foreground_color=COLORS['text_primary'],
            font_size='16sp'
        )
        layout.add_widget(self.text_input)

        # Nombre del archivo
        self.filename_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            hint_text='Nombre del archivo de audio (sin extensión)',
            background_color=COLORS['white'],
            foreground_color=COLORS['text_primary'],
            font_size='16sp'
        )
        layout.add_widget(self.filename_input)

        # Barra de progreso
        self.progress_bar = ProgressBar(
            max=100,
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.progress_bar)

        # Estado de la conversión
        self.status_label = Label(
            text='Listo para convertir',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.status_label)

        # Botón de conversión
        self.convert_button = Button(
            text='Convertir a Audio',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['primary']
        )
        self.convert_button.bind(on_press=lambda x: self.handle_button_press(
            'convert',
            self.start_conversion,
            'Toque dos veces para iniciar la conversión',
            priority='high'
        ))
        layout.add_widget(self.convert_button)

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

    def start_conversion(self):
        text = self.text_input.text
        filename = self.filename_input.text

        if not text or not filename:
            self.status_label.text = 'Por favor, ingresa el texto y el nombre del archivo'
            return

        self.status_label.text = 'Iniciando conversión...'
        self.progress_bar.value = 0
        self.convert_button.disabled = True

        def update_progress(current, total):
            progress = (current / total) * 100
            self.progress_bar.value = progress
            self.status_label.text = f'Procesando capítulo {current} de {total}'

        def conversion_complete(success):
            self.convert_button.disabled = False
            if success:
                self.status_label.text = 'Conversión completada'
                self.accessibility.speak('Conversión completada exitosamente', priority='high')
            else:
                self.status_label.text = 'Error en la conversión'
                self.accessibility.speak('Hubo un error en la conversión', priority='high')

        # Iniciar la conversión en un hilo separado
        Clock.schedule_once(lambda dt: self.converter.convert_text_to_audio(
            text,
            filename,
            update_progress
        ))

    def go_back(self):
        self.manager.current = 'home'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size 