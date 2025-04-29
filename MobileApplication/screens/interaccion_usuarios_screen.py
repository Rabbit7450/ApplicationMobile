from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.metrics import dp
from utils.styles import COLORS, TEXT_STYLES

class InteraccionUsuariosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.amigos = []
        self.mensajes = []
        self.setup_ui()

    def setup_ui(self):
        # Fondo con imagen
        with self.canvas.before:
            self.bg_rect = Rectangle(source='assets/imagenes/fondo1.jpg', size=Window.size, pos=self.pos)
            self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        title = Label(text='Interacción con otros usuarios', **TEXT_STYLES['title'], size_hint_y=None, height=dp(50))
        layout.add_widget(title)

        # Sección agregar amigos
        amigos_box = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(120))
        amigos_label = Label(text='Agregar amigo:', **TEXT_STYLES['subtitle'], size_hint_y=None, height=dp(30))
        amigos_box.add_widget(amigos_label)
        add_box = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(40))
        self.amigo_input = TextInput(hint_text='Nombre de usuario', size_hint_x=0.7, height=dp(40))
        add_btn = Button(text='Agregar', size_hint_x=0.3, height=dp(40), background_normal='', background_color=COLORS['accent'])
        add_btn.bind(on_press=self.agregar_amigo)
        add_box.add_widget(self.amigo_input)
        add_box.add_widget(add_btn)
        amigos_box.add_widget(add_box)
        self.amigos_list_label = Label(text='Amigos: Ninguno', font_size=dp(14), size_hint_y=None, height=dp(30))
        amigos_box.add_widget(self.amigos_list_label)
        layout.add_widget(amigos_box)

        # Sección eliminar amigos
        eliminar_box = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(40))
        self.eliminar_input = TextInput(hint_text='Nombre de amigo a eliminar', size_hint_x=0.7, height=dp(40))
        eliminar_btn = Button(text='Eliminar', size_hint_x=0.3, height=dp(40), background_normal='', background_color=COLORS['secondary'])
        eliminar_btn.bind(on_press=self.eliminar_amigo)
        eliminar_box.add_widget(self.eliminar_input)
        eliminar_box.add_widget(eliminar_btn)
        layout.add_widget(eliminar_box)
        self.eliminar_status = Label(text='', font_size=dp(13), size_hint_y=None, height=dp(20), color=(1,0,0,1))
        layout.add_widget(self.eliminar_status)

        # Sección foro
        foro_label = Label(text='Foro con amigos:', **TEXT_STYLES['subtitle'], size_hint_y=None, height=dp(30))
        layout.add_widget(foro_label)
        self.foro_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=[dp(5),0,dp(5),0])
        self.foro_mensajes = Label(text='No hay mensajes aún.', font_size=dp(14), halign='left', valign='top', size_hint_y=None, height=dp(100), text_size=(Window.width-dp(60), None))
        self.foro_box.add_widget(self.foro_mensajes)
        layout.add_widget(self.foro_box)
        foro_input_box = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(40))
        self.foro_input = TextInput(hint_text='Escribe un mensaje...', size_hint_x=0.7, height=dp(40))
        foro_send_btn = Button(text='Enviar', size_hint_x=0.3, height=dp(40), background_normal='', background_color=COLORS['highlight'])
        foro_send_btn.bind(on_press=self.enviar_mensaje)
        foro_input_box.add_widget(self.foro_input)
        foro_input_box.add_widget(foro_send_btn)
        layout.add_widget(foro_input_box)

        self.add_widget(layout)

    def agregar_amigo(self, instance):
        nombre = self.amigo_input.text.strip()
        if nombre and nombre not in self.amigos:
            self.amigos.append(nombre)
            self.amigos_list_label.text = 'Amigos: ' + ', '.join(self.amigos)
            self.amigo_input.text = ''
        elif nombre:
            self.amigos_list_label.text = f'{nombre} ya está en tu lista.'

    def eliminar_amigo(self, instance):
        nombre = self.eliminar_input.text.strip()
        if nombre in self.amigos:
            self.amigos.remove(nombre)
            self.amigos_list_label.text = 'Amigos: ' + (', '.join(self.amigos) if self.amigos else 'Ninguno')
            self.eliminar_status.text = f'{nombre} eliminado.'
            self.eliminar_input.text = ''
        else:
            self.eliminar_status.text = f'{nombre} no está en tu lista.'

    def enviar_mensaje(self, instance):
        mensaje = self.foro_input.text.strip()
        if mensaje:
            self.mensajes.append(mensaje)
            self.foro_mensajes.text = '\n'.join(self.mensajes[-5:])
            self.foro_input.text = ''

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos 