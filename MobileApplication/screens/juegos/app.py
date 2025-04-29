from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from pathlib import Path
import os

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / 'assets' / 'juegos' / 'dependencias'

# Crear directorio de dependencias si no existe
os.makedirs(ASSETS_DIR, exist_ok=True)

# Configuración de la ventana para móvil
Window.size = (360, 640)  # Tamaño típico de móvil

class CustomButton(ButtonBehavior, BoxLayout):
    text = StringProperty('')
    icon = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Color de fondo
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        icon = Label(text=self.icon, font_size=dp(30))
        text = Label(text=self.text, font_size=dp(16))
        
        self.add_widget(icon)
        self.add_widget(text)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Encabezado
        header = BoxLayout(size_hint_y=None, height=dp(60))
        title = Label(text='Mi App Móvil', font_size=dp(24), bold=True)
        header.add_widget(title)
        
        # Contenido scrollable
        scroll = ScrollView()
        content = GridLayout(cols=1, spacing=dp(20), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Tarjetas de características
        features = [
            ('📱', 'Diseño Responsivo', 'Se adapta a cualquier dispositivo'),
            ('⚡', 'Rápido y Eficiente', 'Optimizado para rendimiento'),
            ('🎨', 'Diseño Moderno', 'Interfaz atractiva y fácil de usar')
        ]
        
        for icon, title, desc in features:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120),
                           padding=dp(15), spacing=dp(10))
            
            with card.canvas.before:
                Color(1, 1, 1, 1)
                Rectangle(size=card.size, pos=card.pos)
            
            card.add_widget(Label(text=icon, font_size=dp(30)))
            card.add_widget(Label(text=title, font_size=dp(18), bold=True))
            card.add_widget(Label(text=desc, font_size=dp(14)))
            
            content.add_widget(card)
        
        scroll.add_widget(content)
        
        # Botón de acción
        action_btn = Button(text='Comenzar Ahora', size_hint_y=None, height=dp(50),
                          background_color=(0.2, 0.6, 0.8, 1))
        
        # Agregar widgets al layout principal
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        main_layout.add_widget(action_btn)
        
        self.add_widget(main_layout)

class MyMobileApp(App):
    def build(self):
        # Configurar el tema
        self.title = 'Mi App Móvil'
        
        # Crear el gestor de pantallas
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        
        return sm

if __name__ == '__main__':
    MyMobileApp().run() 