from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from screens.home_screen import HomeScreen
from screens.no_videntes_screen import NoVidentesScreen
from screens.padres_screen import PadresScreen
from screens.audiolibros_screen import AudiolibrosScreen
from screens.juegos_screen import JuegosScreen
from screens.sugerencias_screen import SugerenciasScreen
from screens.tts_screen import TTSScreen
from screens.reconocimiento_voz_screen import ReconocimientoVozScreen
from screens.modo_contraste_screen import ModoContrasteScreen
from screens.lupa_screen import LupaScreen
from screens.emergencia_screen import EmergenciaScreen

# Configuración para dispositivos móviles
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'orientation', 'portrait')

class MyScreenManager(ScreenManager):
    pass

class MiAplicacion(App):
    def build(self):
        # Configurar el tamaño de la ventana para dispositivos móviles
        Window.size = (360, 640)
        Window.clearcolor = (1, 1, 1, 1)  # Fondo blanco
        
        sm = MyScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NoVidentesScreen(name="no_videntes"))
        sm.add_widget(PadresScreen(name="padres"))
        sm.add_widget(AudiolibrosScreen(name="audiolibros"))
        sm.add_widget(JuegosScreen(name="juegos"))
        sm.add_widget(SugerenciasScreen(name="sugerencias"))
        sm.add_widget(TTSScreen(name="tts"))
        sm.add_widget(ReconocimientoVozScreen(name="reconocimiento_voz"))
        sm.add_widget(ModoContrasteScreen(name="modo_contraste"))
        sm.add_widget(LupaScreen(name="lupa"))
        sm.add_widget(EmergenciaScreen(name="emergencia"))
        return sm

if __name__ == '__main__':
    MiAplicacion().run() 