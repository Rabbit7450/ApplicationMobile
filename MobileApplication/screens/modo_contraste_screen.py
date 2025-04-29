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
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch

class ModoContrasteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.setup_ui()

    def setup_ui(self):
        # Configurar el fondo con gradiente
        with self.canvas.before:
            Color(*COLORS['background'])
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal con ScrollView
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título con estilo mejorado
        title = Label(
            text='Modo Contraste',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(title)

        # Subtítulo con estilo mejorado
        subtitle = Label(
            text='Ajuste la configuración de contraste:',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle)

        # ScrollView para las opciones
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Opciones de contraste
        opciones = [
            ('Alto Contraste', 'alto_contraste', COLORS['primary']),
            ('Contraste Invertido', 'contraste_invertido', COLORS['accent']),
            ('Contraste Personalizado', 'contraste_personalizado', COLORS['success'])
        ]

        for text, screen, color in opciones:
            # Crear tarjeta para cada opción
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

        # Controles adicionales
        # Brillo
        brillo_label = Label(
            text='Ajuste de Brillo',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        grid.add_widget(brillo_label)
        
        brillo_slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint_y=None,
            height=dp(40)
        )
        brillo_slider.bind(value=self.ajustar_brillo)
        grid.add_widget(brillo_slider)

        # Tamaño de texto
        texto_label = Label(
            text='Tamaño de Texto',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        grid.add_widget(texto_label)
        
        texto_slider = Slider(
            min=12,
            max=24,
            value=16,
            size_hint_y=None,
            height=dp(40)
        )
        texto_slider.bind(value=self.ajustar_texto)
        grid.add_widget(texto_slider)

        # Opciones adicionales
        opciones_adicionales = [
            ('Negrita', 'negrita'),
            ('Subrayado', 'subrayado'),
            ('Espaciado de texto', 'espaciado')
        ]

        for text, opcion in opciones_adicionales:
            opcion_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50)
            )
            
            opcion_label = Label(
                text=text,
                size_hint_x=0.7
            )
            opcion_layout.add_widget(opcion_label)
            
            opcion_switch = Switch(
                size_hint_x=0.3
            )
            opcion_switch.bind(active=lambda x, o=opcion: self.toggle_opcion(o, x))
            opcion_layout.add_widget(opcion_switch)
            
            grid.add_widget(opcion_layout)

        # Botón para volver
        back_button = Button(
            text='Volver a la Sección Padres',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['error']
        )
        back_button.bind(on_press=lambda x: self.switch_screen('padres'))
        grid.add_widget(back_button)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def handle_button_press(self, screen_name, button_text):
        current_time = Clock.get_time()
        
        if self.last_clicked_button == button_text and current_time - self.last_click_time < 0.5:
            # Doble clic detectado
            self.aplicar_contraste(screen_name)
        else:
            # Primer clic - narrar
            print(f"Narrando: {button_text}")
        
        self.last_click_time = current_time
        self.last_clicked_button = button_text

    def aplicar_contraste(self, tipo_contraste):
        if tipo_contraste == 'alto_contraste':
            # Aplicar alto contraste
            print("Aplicando alto contraste")
        elif tipo_contraste == 'contraste_invertido':
            # Aplicar contraste invertido
            print("Aplicando contraste invertido")
        elif tipo_contraste == 'contraste_personalizado':
            # Aplicar contraste personalizado
            print("Aplicando contraste personalizado")

    def ajustar_brillo(self, instance, value):
        print(f"Ajustando brillo a: {value}")

    def ajustar_texto(self, instance, value):
        print(f"Ajustando tamaño de texto a: {value}")

    def toggle_opcion(self, opcion, value):
        print(f"Cambiando {opcion} a: {value}")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
