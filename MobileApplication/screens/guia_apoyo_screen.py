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
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class GuiaApoyoScreen(Screen):
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
            text='Guía de Apoyo',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(title)

        # Subtítulo con estilo mejorado
        subtitle = Label(
            text='Consejos y recursos para padres en La Paz',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle)

        # ScrollView para las secciones
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Secciones de la guía
        secciones = [
            ('Desarrollo del Niño', [
                ('Desarrollo Cognitivo', 'Consejos para estimular el desarrollo cognitivo:\n\n'
                 '1. Fomentar la exploración táctil\n'
                 '2. Desarrollar la memoria auditiva\n'
                 '3. Practicar la orientación espacial\n'
                 '4. Estimular la imaginación y creatividad'),
                ('Desarrollo Social', 'Estrategias para el desarrollo social:\n\n'
                 '1. Fomentar la interacción con otros niños\n'
                 '2. Desarrollar habilidades de comunicación\n'
                 '3. Practicar la empatía y el respeto\n'
                 '4. Participar en actividades grupales'),
                ('Desarrollo Físico', 'Actividades para el desarrollo físico:\n\n'
                 '1. Ejercicios de coordinación\n'
                 '2. Juegos de equilibrio\n'
                 '3. Actividades de motricidad fina\n'
                 '4. Deportes adaptados')
            ]),
            ('Apoyo Emocional', [
                ('Manejo de Emociones', 'Estrategias para el manejo emocional:\n\n'
                 '1. Identificar y expresar emociones\n'
                 '2. Técnicas de relajación\n'
                 '3. Desarrollo de la autoestima\n'
                 '4. Manejo de la frustración'),
                ('Comunicación Familiar', 'Mejores prácticas de comunicación:\n\n'
                 '1. Escucha activa\n'
                 '2. Expresión clara de sentimientos\n'
                 '3. Resolución de conflictos\n'
                 '4. Tiempo de calidad en familia')
            ]),
            ('Recursos Locales', [
                ('Centros de Apoyo', 'Centros disponibles en La Paz:\n\n'
                 '1. Centro de Apoyo Familiar del IBC\n'
                 '2. Programas del Ministerio de Educación\n'
                 '3. Grupos de apoyo en centros comunitarios'),
                ('Profesionales', 'Especialistas disponibles:\n\n'
                 '1. Psicólogos especializados\n'
                 '2. Terapeutas ocupacionales\n'
                 '3. Educadores especiales\n'
                 '4. Orientadores familiares')
            ]),
            ('Actividades Diarias', [
                ('Rutinas', 'Sugerencias para rutinas diarias:\n\n'
                 '1. Establecer horarios consistentes\n'
                 '2. Crear rutinas predecibles\n'
                 '3. Fomentar la independencia\n'
                 '4. Incluir momentos de juego y aprendizaje'),
                ('Actividades en Casa', 'Ideas para actividades en casa:\n\n'
                 '1. Juegos sensoriales\n'
                 '2. Lectura y narración\n'
                 '3. Música y ritmo\n'
                 '4. Actividades prácticas')
            ])
        ]

        for seccion, temas in secciones:
            # Título de sección
            sec_label = Label(
                text=seccion,
                **TEXT_STYLES['subtitle'],
                size_hint_y=None,
                height=dp(40)
            )
            grid.add_widget(sec_label)

            # Temas de la sección
            for titulo, contenido in temas:
                # Crear tarjeta para cada tema
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

                # Botón para mostrar contenido
                btn = Button(
                    text=titulo,
                    size_hint_y=None,
                    height=dp(50),
                    background_normal='',
                    background_color=COLORS['primary']
                )
                btn.bind(on_press=lambda x, c=contenido, t=titulo: self.mostrar_contenido(c, t))
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

    def mostrar_contenido(self, contenido, titulo):
        # Crear un layout para el popup
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título del popup con estilo mejorado
        popup_title = Label(
            text=titulo,
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
        parrafos = contenido.split('\n\n')
        for parrafo in parrafos:
            if parrafo.strip():
                # Crear una tarjeta para cada párrafo
                parrafo_card = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10))
                # Label con ajuste automático de alto y salto de línea
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
                # Fondo y borde redondeado
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
        # Agregar borde redondeado al popup
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