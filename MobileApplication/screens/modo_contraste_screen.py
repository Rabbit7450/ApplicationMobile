from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class ModoContrasteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Modo Contraste',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Selecciona el modo de contraste que prefieras',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Opciones de contraste
        contrast_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Modo normal
        normal_btn = ToggleButton(
            text='Modo Normal',
            group='contrast',
            size_hint_y=None,
            height=50
        )
        normal_btn.bind(on_press=lambda x: self.cambiar_contraste('normal'))
        contrast_layout.add_widget(normal_btn)

        # Modo alto contraste
        high_contrast_btn = ToggleButton(
            text='Alto Contraste',
            group='contrast',
            size_hint_y=None,
            height=50
        )
        high_contrast_btn.bind(on_press=lambda x: self.cambiar_contraste('alto'))
        contrast_layout.add_widget(high_contrast_btn)

        # Modo inverso
        inverse_btn = ToggleButton(
            text='Modo Inverso',
            group='contrast',
            size_hint_y=None,
            height=50
        )
        inverse_btn.bind(on_press=lambda x: self.cambiar_contraste('inverso'))
        contrast_layout.add_widget(inverse_btn)

        main_layout.add_widget(contrast_layout)

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

    def cambiar_contraste(self, modo):
        if modo == 'normal':
            # Restaurar colores normales
            Window.clearcolor = (1, 1, 1, 1)
        elif modo == 'alto':
            # Aplicar alto contraste
            Window.clearcolor = (0, 0, 0, 1)
        elif modo == 'inverso':
            # Aplicar modo inverso
            Window.clearcolor = (0, 0, 0, 1)
        print(f"Modo de contraste cambiado a: {modo}")

    def switch_to_home(self):
        self.manager.current = 'home'
