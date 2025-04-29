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
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class PreguntasFrecuentesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.setup_ui()

    def setup_ui(self):
        # Fondo con imagen
        with self.canvas.before:
            self.bg_rect = Rectangle(source='assets/imagenes/fondo1.jpg', size=Window.size, pos=self.pos)
            self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # Layout principal con ScrollView
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título con estilo mejorado
        title = Label(
            text='Preguntas Frecuentes',
            **TEXT_STYLES['title'],
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(title)

        # Subtítulo con estilo mejorado
        subtitle = Label(
            text='Información para padres en La Paz, Bolivia',
            **TEXT_STYLES['subtitle'],
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle)

        # ScrollView para las preguntas
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Categorías de preguntas
        categorias = [
            ('Educación', [
                ('¿Qué escuelas en La Paz ofrecen educación especializada para niños no videntes?',
                 'En La Paz, existen varias instituciones que ofrecen educación especializada:\n\n'
                 '1. Centro de Educación Especial "San Francisco de Asís"\n'
                 '2. Escuela de Ciegos "Santa Lucía"\n'
                 '3. Instituto Boliviano de la Ceguera (IBC)\n\n'
                 'Estas instituciones cuentan con programas adaptados y personal especializado.'),
                ('¿Qué recursos educativos están disponibles en La Paz?',
                 'La Paz ofrece varios recursos educativos:\n\n'
                 '1. Biblioteca del IBC con material en braille\n'
                 '2. Centro de Recursos Educativos del Ministerio de Educación\n'
                 '3. Programas de apoyo en bibliotecas municipales\n'
                 '4. Material didáctico adaptado en centros especializados')
            ]),
            ('Salud', [
                ('¿Dónde puedo encontrar especialistas en salud visual en La Paz?',
                 'Los principales centros de atención son:\n\n'
                 '1. Hospital de Clínicas\n'
                 '2. Instituto Nacional de Oftalmología\n'
                 '3. Clínicas privadas especializadas\n\n'
                 'Se recomienda consultar con el Seguro Universal de Salud (SUS) para cobertura.'),
                ('¿Qué programas de rehabilitación existen?',
                 'Programas disponibles:\n\n'
                 '1. Centro de Rehabilitación del IBC\n'
                 '2. Programas del Ministerio de Salud\n'
                 '3. Terapias en centros especializados privados')
            ]),
            ('Apoyo y Recursos', [
                ('¿Qué organizaciones ofrecen apoyo a familias?',
                 'Organizaciones principales:\n\n'
                 '1. Asociación Boliviana de Padres de Familia de Personas con Discapacidad Visual\n'
                 '2. Fundación para el Desarrollo de la Educación Especial\n'
                 '3. Red de Apoyo a la Discapacidad Visual'),
                ('¿Qué beneficios y derechos tienen los niños no videntes?',
                 'Derechos y beneficios:\n\n'
                 '1. Educación gratuita y especializada\n'
                 '2. Acceso a programas de rehabilitación\n'
                 '3. Beneficios del Seguro Universal de Salud\n'
                 '4. Derecho a materiales educativos adaptados')
            ]),
            ('Desarrollo y Actividades', [
                ('¿Qué actividades recreativas están disponibles?',
                 'Actividades disponibles:\n\n'
                 '1. Deportes adaptados en el IBC\n'
                 '2. Talleres de música y arte\n'
                 '3. Programas de integración social\n'
                 '4. Actividades en centros culturales'),
                ('¿Cómo puedo ayudar a mi hijo a desarrollar habilidades independientes?',
                 'Recomendaciones:\n\n'
                 '1. Participar en programas de orientación y movilidad\n'
                 '2. Practicar actividades de la vida diaria\n'
                 '3. Fomentar la autonomía desde temprana edad\n'
                 '4. Buscar apoyo en grupos de padres')
            ])
        ]

        for categoria, preguntas in categorias:
            # Título de categoría
            cat_label = Label(
                text=categoria,
                **TEXT_STYLES['subtitle'],
                size_hint_y=None,
                height=dp(40)
            )
            grid.add_widget(cat_label)

            # Preguntas de la categoría
            for pregunta, respuesta in preguntas:
                # Crear tarjeta para cada pregunta
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

                # Botón para mostrar la respuesta
                btn = Button(
                    text=pregunta,
                    size_hint_y=None,
                    height=dp(50),
                    background_normal='',
                    background_color=COLORS['primary']
                )
                btn.bind(on_press=lambda x, r=respuesta: self.mostrar_respuesta(r))
                card.add_widget(btn)
                grid.add_widget(card)

        # Botón para volver
        back_button = Button(
            text='Volver a la Sección Padres',
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=COLORS['primary']
        )
        back_button.bind(on_press=lambda x: self.switch_screen('padres'))
        grid.add_widget(back_button)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def mostrar_respuesta(self, respuesta):
        # Crear un layout para el popup
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        # Título del popup
        popup_title = Label(
            text='Respuesta',
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
        parrafos = respuesta.split('\n\n')
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
            background_color=COLORS['primary']
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

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def switch_screen(self, screen_name):
        self.manager.current = screen_name 