from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class EmergenciaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Modo Emergencia',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='En caso de emergencia, presiona el botón de SOS',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Botón de SOS
        sos_button = Button(
            text='SOS',
            size_hint_y=None,
            height=100,
            background_color=(1, 0, 0, 1)  # Rojo
        )
        sos_button.bind(on_press=self.activar_sos)
        main_layout.add_widget(sos_button)

        # Campo para número de emergencia
        emergency_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        emergency_label = Label(
            text='Número de emergencia:',
            size_hint_y=None,
            height=30
        )
        self.emergency_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            hint_text='Ingresa el número de emergencia'
        )
        emergency_layout.add_widget(emergency_label)
        emergency_layout.add_widget(self.emergency_input)
        main_layout.add_widget(emergency_layout)

        # Botones de contacto rápido
        contact_layout = BoxLayout(orientation='vertical', spacing=10)
        contact_label = Label(
            text='Contactos de emergencia:',
            size_hint_y=None,
            height=30
        )
        contact_layout.add_widget(contact_label)

        # Lista de contactos de ejemplo
        contactos = [
            'Médico de cabecera',
            'Familiar cercano',
            'Vecino de confianza'
        ]

        for contacto in contactos:
            btn = Button(
                text=contacto,
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=lambda x, c=contacto: self.llamar_contacto(c))
            contact_layout.add_widget(btn)

        main_layout.add_widget(contact_layout)

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

    def activar_sos(self, instance):
        # Aquí se implementará la lógica de activación de SOS
        print("¡SOS ACTIVADO!")
        print("Llamando a emergencias...")

    def llamar_contacto(self, contacto):
        # Aquí se implementará la lógica de llamada
        print(f"Llamando a: {contacto}")

    def switch_to_home(self):
        self.manager.current = 'home'
