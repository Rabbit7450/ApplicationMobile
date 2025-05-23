from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from utils.styles import COLORS, TEXT_STYLES, BUTTON_STYLES, CARD_STYLES

class NoVidentesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.setup_ui()

    def setup_ui(self):
        # Fondo con imagen
        with self.canvas.before:
            self.bg_rect = Rectangle(source='assets/imagenes/fondo1.jpg', size=Window.size, pos=self.pos)
            self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # Layout principal con ScrollView
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título con estilo mejorado
        title = Label(
            text='Modo No Videntes',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(title)

        # Subtítulo con estilo mejorado
        subtitle = Label(
            text='Seleccione una opción:',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle)

        # ScrollView para los botones
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Botones de navegación con estilo mejorado
        buttons = [
            ('Audiolibros', 'audiolibros', COLORS['primary']),
            ('Juegos Educativos', 'juegos', COLORS['accent']),
            ('Text-to-Speech', 'tts', COLORS['highlight']),
            ('Reconocimiento de Voz', 'reconocimiento_voz', COLORS['secondary']),
            ('Interacción con otros usuarios', 'interaccion_usuarios', COLORS['accent']),
            ('Lupa Digital', 'lupa', COLORS['primary']),
            ('Volver al Menú Principal', 'home', COLORS['primary'])
        ]

        for text, screen, color in buttons:
            # Crear tarjeta para cada botón
            card = BoxLayout(**CARD_STYLES['default'])
            
            # Agregar sombra y borde redondeado
            with card.canvas.before:
                Color(0, 0, 0, 0.1)  # Color de sombra
                RoundedRectangle(
                    pos=(card.x + dp(2), card.y - dp(2)),
                    size=(card.width - dp(4), card.height - dp(4)),
                    radius=[dp(10), dp(10), dp(10), dp(10)]
                )
                Color(*color)
                RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(10), dp(10), dp(10), dp(10)]
                )

            # Botón dentro de la tarjeta
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(50),
                background_normal='',
                background_color=color
            )
            btn.bind(on_press=lambda x, s=screen, t=text: self.handle_button_press(s, t))
            card.add_widget(btn)
            grid.add_widget(card)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def handle_button_press(self, screen_name, button_text):
        current_time = Clock.get_time()
        
        if self.last_clicked_button == button_text and current_time - self.last_click_time < 0.5:
            # Doble clic detectado
            self.switch_screen(screen_name)
        else:
            # Primer clic - narrar
            print(f"Narrando: {button_text}")
        
        self.last_click_time = current_time
        self.last_clicked_button = button_text

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
