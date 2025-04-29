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
from kivy.uix.image import Image
from utils.styles import COLORS, TEXT_STYLES, BUTTON_STYLES, CARD_STYLES

class HomeScreen(Screen):
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
        main_layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15))
        
        # Layout para el logo
        logo_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )
        
        # Logo de la aplicación
        logo = Image(
            source='assets/imagenes/IconoApp.jpg',
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={'center_x': 0.5}
        )
        logo_layout.add_widget(logo)
        
        # Título con estilo mejorado
        title = Label(
            text='Aprecia+',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle'
        )
        logo_layout.add_widget(title)
        
        main_layout.add_widget(logo_layout)

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
            ('Modo No Videntes', 'no_videntes', BUTTON_STYLES['primary']),
            ('Sección Padres', 'padres', BUTTON_STYLES['accent']),
            ('Sugerencias', 'sugerencias', BUTTON_STYLES['secondary']),
            ('Emergencia', 'emergencia', BUTTON_STYLES['highlight'])
        ]

        for text, screen, style in buttons:
            # Crear tarjeta para cada botón
            card = BoxLayout(**CARD_STYLES['default'])
            
            # Agregar sombra y borde redondeado
            with card.canvas.before:
                # Sombra principal
                Color(0, 0, 0, 0.2)  # Color de sombra más oscuro
                RoundedRectangle(
                    pos=(card.x + dp(3), card.y - dp(3)),
                    size=(card.width - dp(6), card.height - dp(6)),
                    radius=[dp(12), dp(12), dp(12), dp(12)]
                )
                # Sombra secundaria
                Color(0, 0, 0, 0.1)
                RoundedRectangle(
                    pos=(card.x + dp(1), card.y - dp(1)),
                    size=(card.width - dp(2), card.height - dp(2)),
                    radius=[dp(12), dp(12), dp(12), dp(12)]
                )
                # Fondo del botón
                Color(*style['background_color'])
                RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(12), dp(12), dp(12), dp(12)]
                )

            # Botón dentro de la tarjeta
            btn = Button(
                text=text,
                **style
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
