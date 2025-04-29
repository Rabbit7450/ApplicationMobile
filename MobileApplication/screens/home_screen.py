from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Configurar el fondo
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Color de fondo gris claro
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Bienvenido a la Aplicación',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)

        # Subtítulo
        subtitle = Label(
            text='Seleccione una opción:',
            font_size='18sp',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(subtitle)

        # Botones de navegación
        buttons = [
            ('No Videntes', 'no_videntes'),
            ('Padres', 'padres'),
            ('Audiolibros', 'audiolibros'),
            ('Juegos', 'juegos'),
            ('Sugerencias', 'sugerencias'),
            ('TTS', 'tts'),
            ('Reconocimiento de Voz', 'reconocimiento_voz'),
            ('Modo Contraste', 'modo_contraste'),
            ('Lupa', 'lupa'),
            ('Emergencia', 'emergencia')
        ]

        for text, screen in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=lambda x, s=screen: self.switch_screen(s))
            layout.add_widget(btn)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
