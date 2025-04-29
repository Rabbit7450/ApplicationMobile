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
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class RecursosEducativosScreen(Screen):
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
            text='Recursos Educativos',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(title)

        # Subtítulo con estilo mejorado
        subtitle = Label(
            text='Materiales y herramientas educativas en La Paz',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle)

        # ScrollView para los recursos
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Categorías de recursos
        categorias = [
            ('Material Didáctico', [
                ('Libros en Braille', 'Disponibles en la Biblioteca del IBC y bibliotecas municipales'),
                ('Material Táctil', 'Mapas, figuras geométricas y otros recursos táctiles'),
                ('Recursos Digitales', 'Aplicaciones y software educativo adaptado')
            ]),
            ('Centros de Recursos', [
                ('Biblioteca del IBC', 'Av. 6 de Agosto, La Paz\nHorario: Lunes a Viernes 8:00-16:00'),
                ('Centro de Recursos del Ministerio de Educación', 'Calle Loayza, La Paz\nHorario: Lunes a Viernes 9:00-17:00'),
                ('Bibliotecas Municipales', 'Varias ubicaciones en La Paz con secciones especializadas')
            ]),
            ('Programas Educativos', [
                ('Programa de Alfabetización', 'Cursos de lectura y escritura en braille'),
                ('Talleres de Matemáticas', 'Material adaptado para el aprendizaje de matemáticas'),
                ('Programa de Orientación y Movilidad', 'Entrenamiento en habilidades de movilidad independiente')
            ]),
            ('Recursos en Línea', [
                ('Plataforma Educativa del IBC', 'Acceso a materiales digitales y cursos en línea'),
                ('Biblioteca Digital', 'Libros y recursos en formato digital accesible'),
                ('Comunidad Virtual', 'Foros y grupos de apoyo para padres y educadores')
            ])
        ]

        for categoria, recursos in categorias:
            # Título de categoría
            cat_label = Label(
                text=categoria,
                **TEXT_STYLES['subtitle'],
                size_hint_y=None,
                height=dp(40)
            )
            grid.add_widget(cat_label)

            # Recursos de la categoría
            for titulo, descripcion in recursos:
                # Crear tarjeta para cada recurso
                card = BoxLayout(**CARD_STYLES['default'])
                
                # Agregar sombra y borde redondeado
                with card.canvas.before:
                    Color(0, 0, 0, 0.1)  # Color de sombra
                    RoundedRectangle(
                        pos=(card.x + dp(2), card.y - dp(2)),
                        size=(card.width - dp(4), card.height - dp(4)),
                        radius=[dp(10), dp(10), dp(10), dp(10)]
                    )
                    Color(*COLORS['primary'])
                    RoundedRectangle(
                        pos=card.pos,
                        size=card.size,
                        radius=[dp(10), dp(10), dp(10), dp(10)]
                    )

                # Botón para mostrar detalles
                btn = Button(
                    text=titulo,
                    size_hint_y=None,
                    height=dp(50),
                    background_normal='',
                    background_color=COLORS['primary']
                )
                btn.bind(on_press=lambda x, d=descripcion: self.mostrar_detalles(d))
                card.add_widget(btn)
                grid.add_widget(card)

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

    def mostrar_detalles(self, descripcion):
        # Crear un layout para el popup
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        # Título del popup
        popup_title = Label(
            text='Detalles del Recurso',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        popup_layout.add_widget(popup_title)
        # Separador
        separator = BoxLayout(size_hint_y=None, height=dp(2))
        with separator.canvas.before:
            Color(*COLORS['primary'])
            Rectangle(pos=separator.pos, size=separator.size)
        popup_layout.add_widget(separator)
        # Contenido en un ScrollView
        content_scroll = ScrollView(size_hint=(1, 1))
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(10))
        content_layout.bind(minimum_height=content_layout.setter('height'))
        # Dividir el contenido en párrafos
        parrafos = descripcion.split('\n\n')
        for parrafo in parrafos:
            if parrafo.strip():
                parrafo_card = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10))
                parrafo_label = Label(
                    text=parrafo,
                    size_hint_y=None,
                    halign='left',
                    valign='top',
                    color=(0, 0, 0, 1),
                    font_size=dp(16),
                    text_size=(dp(300), None)
                )
                parrafo_label.bind(texture_size=lambda instance, value: setattr(parrafo_label, 'height', value[1]))
                parrafo_card.add_widget(parrafo_label)
                with parrafo_card.canvas.before:
                    Color(0.95, 0.95, 0.95, 1)
                    RoundedRectangle(pos=parrafo_card.pos, size=parrafo_card.size, radius=[dp(10)]*4)
                content_layout.add_widget(parrafo_card)
        content_scroll.add_widget(content_layout)
        popup_layout.add_widget(content_scroll)
        # Botón para cerrar
        close_button = Button(
            text='Cerrar',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['error']
        )
        popup_layout.add_widget(close_button)
        # Crear el popup
        popup = Popup(
            title='',
            content=popup_layout,
            size_hint=(0.9, 0.9),
            background='',
            background_color=(1, 1, 1, 0.95),
            separator_height=0
        )
        with popup.canvas.before:
            Color(0, 0, 0, 0.1)
            RoundedRectangle(pos=(popup.x + dp(2), popup.y - dp(2)), size=(popup.width - dp(4), popup.height - dp(4)), radius=[dp(20)]*4)
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(20)]*4)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_screen(self, screen_name):
        self.manager.current = screen_name 