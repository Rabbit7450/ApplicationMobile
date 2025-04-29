from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from utils.styles import COLORS, TEXT_STYLES, BUTTON_STYLES, CARD_STYLES

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_label = None
        self.setup_ui()

    def setup_ui(self):
        with self.canvas.before:
            Color(*COLORS['background'])
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20), size_hint=(.9, .8), pos_hint={'center_x':.5, 'center_y':.5})

        title = Label(text='Iniciar Sesión', **TEXT_STYLES['title'], size_hint_y=None, height=dp(60))
        layout.add_widget(title)

        self.user_input = TextInput(hint_text='Usuario', multiline=False, size_hint_y=None, height=dp(50), padding=[dp(10), dp(10)], background_color=(1,1,1,1), foreground_color=(0,0,0,1), font_size=dp(18), cursor_color=(0,0,0,1))
        layout.add_widget(self.user_input)

        self.pass_input = TextInput(hint_text='Contraseña', multiline=False, password=True, size_hint_y=None, height=dp(50), padding=[dp(10), dp(10)], background_color=(1,1,1,1), foreground_color=(0,0,0,1), font_size=dp(18), cursor_color=(0,0,0,1))
        layout.add_widget(self.pass_input)

        self.error_label = Label(text='', color=(1,0,0,1), size_hint_y=None, height=dp(30), font_size=dp(14))
        layout.add_widget(self.error_label)

        login_btn = Button(text='Ingresar', size_hint_y=None, height=dp(50), background_normal='', background_color=COLORS['primary'], font_size=dp(18))
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        # Fondo y borde redondeado
        with layout.canvas.before:
            Color(1, 1, 1, 0.95)
            RoundedRectangle(pos=layout.pos, size=layout.size, radius=[dp(20)]*4)

        # Fondo con imagen
        with self.canvas.before:
            self.bg_rect = Rectangle(source='assets/imagenes/fondo.jpg', size=Window.size, pos=self.pos)
            self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        self.add_widget(layout)

    def login(self, instance):
        usuario = self.user_input.text.strip()
        contrasena = self.pass_input.text.strip()
        # Validación básica (usuario: admin, contraseña: admin)
        if usuario == 'admin' and contrasena == 'admin':
            self.error_label.text = ''
            self.manager.current = 'home'
        else:
            self.error_label.text = 'Usuario o contraseña incorrectos'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos 