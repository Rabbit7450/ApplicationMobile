from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class LupaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Lupa Digital',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Ajusta el nivel de zoom con el control deslizante',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # Control deslizante para el zoom
        zoom_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        zoom_label = Label(text='Nivel de Zoom:', size_hint_y=None, height=30)
        self.zoom_slider = Slider(
            min=1,
            max=5,
            value=1,
            size_hint_y=None,
            height=50
        )
        self.zoom_slider.bind(value=self.ajustar_zoom)
        zoom_layout.add_widget(zoom_label)
        zoom_layout.add_widget(self.zoom_slider)
        main_layout.add_widget(zoom_layout)

        # Área de visualización
        self.view_area = BoxLayout(size_hint_y=None, height=300)
        with self.view_area.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.view_area.size, pos=self.view_area.pos)
        self.view_area.bind(size=self._update_rect, pos=self._update_rect)
        main_layout.add_widget(self.view_area)

        # Botones de control
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Botón para activar/desactivar lupa
        self.toggle_button = Button(
            text='Activar Lupa',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.toggle_button.bind(on_press=self.toggle_lupa)
        control_layout.add_widget(self.toggle_button)

        main_layout.add_widget(control_layout)

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

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def ajustar_zoom(self, instance, value):
        # Aquí se implementará la lógica de zoom
        print(f"Nivel de zoom ajustado a: {value}x")

    def toggle_lupa(self, instance):
        if self.toggle_button.text == 'Activar Lupa':
            self.toggle_button.text = 'Desactivar Lupa'
            # Aquí se implementará la lógica de activación
            print("Lupa activada")
        else:
            self.toggle_button.text = 'Activar Lupa'
            # Aquí se implementará la lógica de desactivación
            print("Lupa desactivada")

    def switch_to_home(self):
        self.manager.current = 'home'
