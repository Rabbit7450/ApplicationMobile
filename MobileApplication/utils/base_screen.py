from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from utils.accessibility_manager import AccessibilityManager

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0
        self.last_clicked_button = None
        self.accessibility = AccessibilityManager()

    def handle_button_press(self, button_id, action, button_text=None, priority='normal'):
        """
        Maneja el doble clic en botones con feedback táctil y auditivo.
        
        Args:
            button_id: Identificador único del botón
            action: Función a ejecutar en doble clic
            button_text: Texto a narrar en primer clic (opcional)
            priority: Prioridad de la narración ('low', 'normal', 'high')
        """
        current_time = Clock.get_time()
        
        if self.last_clicked_button == button_id and current_time - self.last_click_time < 0.5:
            # Doble clic detectado
            self.accessibility.stop_speech()  # Detener cualquier narración en curso
            self.accessibility.vibrate([0, 50, 50, 50])  # Vibración de confirmación
            action()
        else:
            # Primer clic - narrar y dar feedback táctil
            if button_text:
                self.accessibility.speak(button_text, priority)
                self.accessibility.vibrate([0, 30, 30, 30])  # Vibración suave
        
        self.last_click_time = current_time
        self.last_clicked_button = button_id

    def announce_screen(self, screen_name):
        """Anuncia el nombre de la pantalla al entrar"""
        self.accessibility.speak(f"Pantalla {screen_name}", priority='high')
        self.accessibility.vibrate([0, 100, 100, 100])

    def on_enter(self):
        """Se llama cuando la pantalla se activa"""
        super().on_enter()
        self.announce_screen(self.name)

    def on_leave(self):
        """Se llama cuando la pantalla se desactiva"""
        super().on_leave()
        self.accessibility.stop_speech()
        self.accessibility.stop_vibration() 