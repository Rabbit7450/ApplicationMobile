from plyer import tts
from kivy.utils import platform
from kivy.clock import Clock

class TTSManager:
    def __init__(self):
        self.is_speaking = False
        self.is_available = False
        self.setup_tts()

    def setup_tts(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                # Obtener el contexto de Android
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                context = activity.getApplicationContext()

                # Configurar el motor TTS
                tts.speak('', language='es-ES')  # Inicializar con español
                self.is_available = True
                print("TTS configurado correctamente")
            except Exception as e:
                print(f"Error al configurar TTS: {str(e)}")
                self.is_available = False
        else:
            print("TTS solo disponible en Android")
            self.is_available = False

    def speak(self, text):
        if not self.is_available:
            print(f"Narrando: {text}")
            return False

        try:
            if self.is_speaking:
                tts.stop()
            
            # Configurar el idioma y la velocidad
            tts.speak(text, language='es-ES', pitch=1.0, rate=1.0)
            self.is_speaking = True
            print(f"Reproduciendo: {text}")
            return True
        except Exception as e:
            print(f"Error al narrar: {str(e)}")
            return False

    def stop(self):
        if self.is_available and self.is_speaking:
            try:
                tts.stop()
                self.is_speaking = False
                print("Narración detenida")
                return True
            except Exception as e:
                print(f"Error al detener narración: {str(e)}")
                return False
        return False
