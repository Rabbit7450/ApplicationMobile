from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from utils.tts_manager import TTSManager

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.tts_manager = TTSManager()

    def handle_button_press(self, button_id, action, button_text=None):
        """
        Maneja el doble clic en botones.
        
        Args:
            button_id: Identificador único del botón
            action: Función a ejecutar en doble clic
            button_text: Texto a narrar en primer clic (opcional)
        """
        current_time = Clock.get_time()
        
        if self.last_clicked_button == button_id and current_time - self.last_click_time < 0.5:
            # Doble clic detectado
            self.tts_manager.stop()  # Detener cualquier narración en curso
            action()
        else:
            # Primer clic - narrar
            if button_text:
                self.tts_manager.speak(button_text)
        
        self.last_click_time = current_time
        self.last_clicked_button = button_id 