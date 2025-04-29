from kivy.utils import platform
from kivy.clock import Clock
from plyer import tts
import os

class AccessibilityManager:
    def __init__(self):
        self.is_speaking = False
        self.is_vibrating = False
        self.setup_accessibility()

    def setup_accessibility(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                # Obtener el contexto de Android
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self.activity = PythonActivity.mActivity
                self.context = self.activity.getApplicationContext()

                # Configurar el motor TTS
                tts.speak('', language='es-ES')
                self.is_tts_available = True

                # Configurar el vibrador
                self.Vibrator = autoclass('android.os.Vibrator')
                self.vibrator = self.context.getSystemService(self.context.VIBRATOR_SERVICE)
                self.is_vibrator_available = True

                # Configurar el gestor de accesibilidad
                self.AccessibilityManager = autoclass('android.view.accessibility.AccessibilityManager')
                self.accessibility_manager = self.context.getSystemService(self.context.ACCESSIBILITY_SERVICE)
                self.is_accessibility_available = True

                print("Accesibilidad configurada correctamente")
            except Exception as e:
                print(f"Error al configurar accesibilidad: {str(e)}")
                self.is_tts_available = False
                self.is_vibrator_available = False
                self.is_accessibility_available = False
        else:
            print("Accesibilidad solo disponible en Android")
            self.is_tts_available = False
            self.is_vibrator_available = False
            self.is_accessibility_available = False

    def speak(self, text, priority='normal'):
        """
        Narra el texto con diferentes prioridades.
        Prioridades: 'low', 'normal', 'high'
        """
        if not self.is_tts_available:
            print(f"Narrando: {text}")
            return False

        try:
            if self.is_speaking:
                tts.stop()
            
            # Configurar el idioma y la velocidad según la prioridad
            rate = 1.0
            if priority == 'high':
                rate = 1.2
            elif priority == 'low':
                rate = 0.8
            
            tts.speak(text, language='es-ES', pitch=1.0, rate=rate)
            self.is_speaking = True
            print(f"Reproduciendo: {text}")
            return True
        except Exception as e:
            print(f"Error al narrar: {str(e)}")
            return False

    def vibrate(self, pattern=None, repeat=-1):
        """
        Hace vibrar el dispositivo con un patrón específico.
        pattern: lista de duraciones en milisegundos
        repeat: número de repeticiones (-1 para infinito)
        """
        if not self.is_vibrator_available:
            return False

        try:
            if pattern is None:
                # Patrón por defecto: vibración corta
                pattern = [0, 100, 100, 100]
            
            # Convertir el patrón a un array de long
            pattern_array = [long(x) for x in pattern]
            
            # Aplicar el patrón de vibración
            self.vibrator.vibrate(pattern_array, repeat)
            self.is_vibrating = True
            return True
        except Exception as e:
            print(f"Error al vibrar: {str(e)}")
            return False

    def stop_vibration(self):
        """Detiene la vibración actual"""
        if self.is_vibrator_available and self.is_vibrating:
            try:
                self.vibrator.cancel()
                self.is_vibrating = False
                return True
            except:
                return False
        return False

    def stop_speech(self):
        """Detiene la narración actual"""
        if self.is_tts_available and self.is_speaking:
            try:
                tts.stop()
                self.is_speaking = False
                return True
            except:
                return False
        return False

    def get_screen_reader_status(self):
        """Verifica si el lector de pantalla está activo"""
        if platform == 'android' and self.is_accessibility_available:
            try:
                return self.accessibility_manager.isEnabled()
            except:
                return False
        return False

    def announce_for_accessibility(self, text, event_type='TYPE_VIEW_CLICKED'):
        """
        Anuncia el texto usando el servicio de accesibilidad de Android.
        Útil cuando el lector de pantalla está activo.
        """
        if platform == 'android' and self.is_accessibility_available:
            try:
                from jnius import autoclass
                AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')
                event = AccessibilityEvent.obtain()
                event.setEventType(getattr(AccessibilityEvent, event_type))
                event.setClassName(self.activity.getClass().getName())
                event.setPackageName(self.context.getPackageName())
                event.getText().add(text)
                self.accessibility_manager.sendAccessibilityEvent(event)
                return True
            except Exception as e:
                print(f"Error al anunciar para accesibilidad: {str(e)}")
                return False
        return False 