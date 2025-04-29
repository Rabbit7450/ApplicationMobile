from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os
import importlib.util
from pathlib import Path

class JuegosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='Juegos Educativos',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)

        # Descripción
        description = Label(
            text='Selecciona un juego para comenzar',
            font_size='16sp',
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(description)

        # ScrollView para la lista de juegos
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Obtener la lista de juegos del directorio
        juegos_dir = Path(__file__).parent / 'juegos'
        juegos = []
        
        if juegos_dir.exists():
            for archivo in juegos_dir.glob('*.py'):
                if archivo.name != '__init__.py':
                    # Convertir el nombre del archivo a un nombre más amigable
                    nombre_juego = archivo.stem.replace('_', ' ').title()
                    juegos.append((nombre_juego, str(archivo)))

        # Si no hay juegos, mostrar un mensaje
        if not juegos:
            no_juegos = Label(
                text='No hay juegos disponibles',
                font_size='16sp',
                size_hint_y=None,
                height=50
            )
            grid.add_widget(no_juegos)
        else:
            # Agregar botones para cada juego
            for nombre_juego, ruta_juego in juegos:
                btn = Button(
                    text=nombre_juego,
                    size_hint_y=None,
                    height=50,
                    background_color=(0.2, 0.6, 1, 1)
                )
                btn.bind(on_press=lambda x, j=nombre_juego, r=ruta_juego: self.iniciar_juego(j, r))
                grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

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

    def iniciar_juego(self, nombre_juego, ruta_juego):
        try:
            # Cargar el módulo dinámicamente
            spec = importlib.util.spec_from_file_location(nombre_juego, ruta_juego)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            # Buscar la clase principal del juego
            for nombre_clase in dir(modulo):
                if nombre_clase.endswith('Screen') or nombre_clase.endswith('Game'):
                    clase_juego = getattr(modulo, nombre_clase)
                    # Crear una instancia del juego
                    juego = clase_juego()
                    # Agregar el juego a la pantalla actual
                    self.add_widget(juego)
                    # Cambiar a la pantalla del juego
                    self.manager.current = nombre_juego
                    return

            print(f"No se encontró una clase principal en el juego {nombre_juego}")
        except Exception as e:
            print(f"Error al cargar el juego {nombre_juego}: {str(e)}")

    def switch_to_home(self):
        self.manager.current = 'home'
