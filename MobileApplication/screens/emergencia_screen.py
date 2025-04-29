from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
import time
from kivy.clock import Clock

class EmergenciaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.contact_numbers = {
            'Médico de cabecera': '',
            'Familiar cercano': '',
            'Vecino de confianza': ''
        }
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título
        title = Label(
            text='Modo Emergencia',
            font_size='24sp',
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='En caso de emergencia, presiona el botón de SOS',
            font_size='16sp',
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(description)

        # Botón de SOS con doble clic
        sos_button = Button(
            text='SOS',
            size_hint_y=None,
            height=dp(100),
            background_color=(1, 0, 0, 1)  # Rojo
        )
        sos_button.bind(on_press=lambda x: self.handle_double_click('sos', self.activar_sos, 'Presiona dos veces para activar SOS'))
        main_layout.add_widget(sos_button)

        # Campo para número de emergencia general
        emergency_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
        emergency_label = Label(
            text='Número de emergencia:',
            size_hint_y=None,
            height=dp(30)
        )
        self.emergency_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            hint_text='Ingresa el número de emergencia'
        )
        emergency_layout.add_widget(emergency_label)
        emergency_layout.add_widget(self.emergency_input)
        main_layout.add_widget(emergency_layout)

        # Botones de contacto rápido con edición de número
        contact_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        contact_label = Label(
            text='Contactos de emergencia:',
            size_hint_y=None,
            height=dp(30)
        )
        contact_layout.add_widget(contact_label)

        self.contact_inputs = {}
        contactos = [
            'Médico de cabecera',
            'Familiar cercano',
            'Vecino de confianza'
        ]
        for contacto in contactos:
            row = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(50))
            btn = Button(
                text=contacto,
                size_hint_x=0.4,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=lambda x, c=contacto: self.handle_double_click(c, lambda: self.llamar_contacto(c), f'Doble clic para llamar a {c}'))
            input_num = TextInput(
                text=self.contact_numbers[contacto],
                hint_text='Número',
                size_hint_x=0.4,
                multiline=False
            )
            self.contact_inputs[contacto] = input_num
            save_btn = Button(
                text='Guardar',
                size_hint_x=0.2,
                background_color=(0.7, 0.7, 0.7, 1)
            )
            save_btn.bind(on_press=lambda x, c=contacto: self.guardar_numero_contacto(c))
            row.add_widget(btn)
            row.add_widget(input_num)
            row.add_widget(save_btn)
            contact_layout.add_widget(row)
        main_layout.add_widget(contact_layout)

        # Mensaje de estado
        self.status_label = Label(text='', font_size=dp(14), size_hint_y=None, height=dp(30), color=(0,0.5,0,1))
        main_layout.add_widget(self.status_label)

        # Botón para volver a la pantalla principal con doble clic
        back_button = Button(
            text='Volver al Inicio',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.handle_double_click('back', self.switch_to_home, 'Doble clic para volver al inicio'))
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def handle_double_click(self, button_id, action, narracion):
        current_time = time.time()
        if self.last_clicked_button == button_id and current_time - self.last_click_time < 0.5:
            action()
        else:
            print(f'Narrando: {narracion}')
        self.last_click_time = current_time
        self.last_clicked_button = button_id

    def activar_sos(self):
        print('¡SOS ACTIVADO!')
        print('Llamando a emergencias...')
        print(f'Número de emergencia: {self.emergency_input.text}')

    def llamar_contacto(self, contacto):
        numero = self.contact_inputs[contacto].text
        print(f'Llamando a: {contacto} ({numero})')
        self.mostrar_mensaje(f'Llamando a: {contacto} ({numero})')

    def guardar_numero_contacto(self, contacto):
        self.contact_numbers[contacto] = self.contact_inputs[contacto].text
        print(f'Número de {contacto} guardado: {self.contact_numbers[contacto]}')
        self.mostrar_mensaje(f'Número de {contacto} guardado')

    def mostrar_mensaje(self, mensaje):
        self.status_label.text = mensaje
        Clock.schedule_once(lambda dt: self.limpiar_mensaje(), 2)

    def limpiar_mensaje(self):
        self.status_label.text = ''

    def switch_to_home(self):
        self.manager.current = 'home'
