from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.no_videntes_screen import NoVidentesScreen
from screens.padres_screen import PadresScreen
from screens.preguntas_frecuentes_screen import PreguntasFrecuentesScreen
from screens.modo_contraste_screen import ModoContrasteScreen
from screens.recursos_educativos_screen import RecursosEducativosScreen
from screens.guia_apoyo_screen import GuiaApoyoScreen
from screens.audiolibros_screen import AudiolibrosScreen
from screens.juegos_screen import JuegosScreen
from screens.tts_screen import TTSScreen
from screens.reconocimiento_voz_screen import ReconocimientoVozScreen
from screens.lupa_screen import LupaScreen
from screens.sugerencias_screen import SugerenciasScreen
from screens.emergencia_screen import EmergenciaScreen
from screens.interaccion_usuarios_screen import InteraccionUsuariosScreen

# Configuración para dispositivos móviles
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'orientation', 'portrait')

class MyScreenManager(ScreenManager):
    pass

class ApreciaPlus(App):
    def build(self):
        # Configurar el tema de la aplicación
        self.title = 'Aprecia+'
        # Configurar el tamaño de la ventana para dispositivos móviles
        Window.size = (360, 640)  # Ancho x Alto
        return self.setup_screens()

    def setup_screens(self):
        # Crear el gestor de pantallas
        sm = ScreenManager()
        
        # Agregar las pantallas
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(NoVidentesScreen(name='no_videntes'))
        sm.add_widget(PadresScreen(name='padres'))
        sm.add_widget(PreguntasFrecuentesScreen(name='preguntas_frecuentes'))
        sm.add_widget(ModoContrasteScreen(name='modo_contraste'))
        sm.add_widget(RecursosEducativosScreen(name='recursos_educativos'))
        sm.add_widget(GuiaApoyoScreen(name='guia_apoyo'))
        sm.add_widget(AudiolibrosScreen(name='audiolibros'))
        sm.add_widget(JuegosScreen(name='juegos'))
        sm.add_widget(TTSScreen(name='tts'))
        sm.add_widget(ReconocimientoVozScreen(name='reconocimiento_voz'))
        sm.add_widget(LupaScreen(name='lupa'))
        sm.add_widget(SugerenciasScreen(name='sugerencias'))
        sm.add_widget(EmergenciaScreen(name='emergencia'))
        sm.add_widget(InteraccionUsuariosScreen(name='interaccion_usuarios'))
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    ApreciaPlus().run()
