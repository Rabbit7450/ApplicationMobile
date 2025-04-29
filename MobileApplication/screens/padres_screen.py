from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class PadresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Sección para Padres',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)

        # Descripción
        description = Label(
            text='Esta sección contiene información y recursos para padres',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(description)

        # Botón para volver a la pantalla principal
        back_button = Button(
            text='Volver al Inicio',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.switch_to_home())
        layout.add_widget(back_button)

        self.add_widget(layout)

    def switch_to_home(self):
        self.manager.current = 'home'
