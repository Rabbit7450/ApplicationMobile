import random
import time
import pyttsx3
import speech_recognition as sr
import json
import os
import winsound
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from .base_game import BaseGame

class AdivinanzasGame(BaseGame):
    def __init__(self, **kwargs):
        # Inicializar el motor de texto a voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Velocidad de la voz
        self.engine.setProperty('volume', 0.9)  # Volumen (0.0 a 1.0)

        # Inicializar el reconocedor de voz
        self.recognizer = sr.Recognizer()

        # Obtener la ruta base del proyecto
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        ASSETS_DIR = BASE_DIR / 'assets' / 'juegos' / 'dependencias'

        # Crear directorio de dependencias si no existe
        os.makedirs(ASSETS_DIR, exist_ok=True)

        # Archivo para guardar adivinanzas personalizadas y puntuación
        self.ARCHIVO_ADIVINANZAS = str(ASSETS_DIR / "adivinanzas_personalizadas.json")
        self.ARCHIVO_PUNTUACION = str(ASSETS_DIR / "puntuacion_adivinanzas.txt")

        # Lista inicial de adivinanzas
        self.adivinanzas = [
            {"pregunta": "Blanco por dentro, verde por fuera, si quieres que te lo diga, espera. Qué es?", "respuesta": "pera"},
            {"pregunta": "En un corral hay gallinas y conejos, si cuento las patas, son 10, y si cuento las cabezas, son 4. Cuántas gallinas hay?", "respuesta": "2"},
            {"pregunta": "Oro parece, plata no es, qué es?", "respuesta": "platano"},
            {"pregunta": "Qué animal tiene cuatro patas y un solo brazo?", "respuesta": "perro"},
            {"pregunta": "Qué es lo que tiene cuello pero no cabeza, cuerpo pero no piernas, brazos pero no manos?", "respuesta": "camisa"},
        ]

        # Cargar adivinanzas personalizadas
        self.adivinanzas_personalizadas = self.cargar_adivinanzas_personalizadas()
        self.todas_adivinanzas = self.adivinanzas + self.adivinanzas_personalizadas

        # Variables del juego
        self.puntuacion = self.cargar_puntuacion()
        self.adivinanza_actual = None
        self.modo = "jugar"  # "jugar" o "agregar"

        super().__init__(**kwargs)

    def get_title(self):
        return "Adivinanzas"

    def get_description(self):
        return "¡Adivina la respuesta a las adivinanzas usando tu voz!"

    def create_content(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Botones de modo
        modo_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        jugar_btn = Button(text='Jugar', on_press=lambda x: self.cambiar_modo("jugar"))
        agregar_btn = Button(text='Agregar Adivinanza', on_press=lambda x: self.cambiar_modo("agregar"))
        modo_layout.add_widget(jugar_btn)
        modo_layout.add_widget(agregar_btn)
        content.add_widget(modo_layout)

        # Área de juego
        self.game_area = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(self.game_area)

        # Iniciar el juego
        self.cambiar_modo("jugar")

        return content

    def cargar_adivinanzas_personalizadas(self):
        if os.path.exists(self.ARCHIVO_ADIVINANZAS):
            with open(self.ARCHIVO_ADIVINANZAS, "r") as f:
                return json.load(f)
        return []

    def guardar_adivinanzas_personalizadas(self):
        with open(self.ARCHIVO_ADIVINANZAS, "w") as f:
            json.dump(self.adivinanzas_personalizadas, f)

    def cargar_puntuacion(self):
        if os.path.exists(self.ARCHIVO_PUNTUACION):
            with open(self.ARCHIVO_PUNTUACION, "r") as f:
                try:
                    return int(f.read().strip())
                except:
                    return 0
        return 0

    def guardar_puntuacion(self):
        with open(self.ARCHIVO_PUNTUACION, "w") as f:
            f.write(str(self.puntuacion))

    def hablar(self, texto):
        """Función para que el programa hable"""
        print(f"🔊 Diciendo: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()

    def reproducir_sonido(self, tipo):
        """Función para reproducir sonidos de correcto o incorrecto"""
        if tipo == "correcto":
            winsound.Beep(1000, 500)  # Frecuencia 1000 Hz, duración 500 ms
        else:
            winsound.Beep(500, 500)   # Frecuencia 500 Hz, duración 500 ms

    def escuchar_respuesta(self, mensaje="Por favor, di tu respuesta."):
        """Función para escuchar la respuesta del usuario mediante voz"""
        with sr.Microphone() as source:
            self.hablar(mensaje)
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"Escuché: {texto}")
                return texto.lower()
            except sr.WaitTimeoutError:
                self.hablar("No escuché nada. Intentemos de nuevo.")
                return None
            except sr.UnknownValueError:
                self.hablar("No entendí tu respuesta. Intenta de nuevo.")
                return None
            except sr.RequestError:
                self.hablar("Hubo un error con el reconocimiento de voz. Asegúrate de estar conectado a internet.")
                return None

    def cambiar_modo(self, modo):
        self.modo = modo
        self.game_area.clear_widgets()

        if modo == "jugar":
            self.iniciar_juego()
        else:
            self.iniciar_agregar_adivinanza()

    def iniciar_juego(self):
        if not self.todas_adivinanzas:
            self.game_area.add_widget(Label(text="No hay adivinanzas disponibles. Agrega algunas primero."))
            return

        self.adivinanza_actual = random.choice(self.todas_adivinanzas)
        
        # Mostrar la adivinanza
        self.game_area.add_widget(Label(text=self.adivinanza_actual["pregunta"]))
        
        # Botón para responder
        responder_btn = Button(text="Responder", on_press=self.responder_adivinanza)
        self.game_area.add_widget(responder_btn)

    def iniciar_agregar_adivinanza(self):
        # Campos para agregar adivinanza
        self.game_area.add_widget(Label(text="Agregar nueva adivinanza"))
        
        # Campo para la pregunta
        self.pregunta_input = TextInput(multiline=True, hint_text="Escribe la adivinanza")
        self.game_area.add_widget(self.pregunta_input)
        
        # Campo para la respuesta
        self.respuesta_input = TextInput(multiline=False, hint_text="Escribe la respuesta")
        self.game_area.add_widget(self.respuesta_input)
        
        # Botón para guardar
        guardar_btn = Button(text="Guardar Adivinanza", on_press=self.guardar_adivinanza)
        self.game_area.add_widget(guardar_btn)

    def responder_adivinanza(self, instance):
        respuesta = self.escuchar_respuesta()
        if respuesta is None:
            return

        if respuesta == self.adivinanza_actual["respuesta"]:
            self.hablar("¡Correcto! Muy bien.")
            self.reproducir_sonido("correcto")
            self.puntuacion += 10
        else:
            self.hablar(f"Lo siento, eso no es correcto. La respuesta correcta era {self.adivinanza_actual['respuesta']}.")
            self.reproducir_sonido("incorrecto")
            self.puntuacion -= 5

        self.guardar_puntuacion()
        self.hablar(f"Tu puntuación ahora es {self.puntuacion}.")
        
        # Preguntar si quiere continuar
        self.hablar("¿Quieres otra adivinanza? Di 'sí' o 'no'.")
        continuar = self.escuchar_respuesta()
        
        if continuar and ("sí" in continuar or "si" in continuar):
            self.iniciar_juego()
        else:
            self.hablar(f"¡Gracias por jugar! Tu puntuación final es {self.puntuacion} puntos.")

    def guardar_adivinanza(self, instance):
        pregunta = self.pregunta_input.text.strip()
        respuesta = self.respuesta_input.text.strip()
        
        if not pregunta or not respuesta:
            self.hablar("Por favor, completa ambos campos.")
            return
        
        nueva_adivinanza = {"pregunta": pregunta, "respuesta": respuesta}
        self.adivinanzas_personalizadas.append(nueva_adivinanza)
        self.todas_adivinanzas.append(nueva_adivinanza)
        self.guardar_adivinanzas_personalizadas()
        
        self.hablar(f"Adivinanza agregada: {pregunta} Respuesta: {respuesta}")
        
        # Limpiar campos
        self.pregunta_input.text = ""
        self.respuesta_input.text = ""

if __name__ == "__main__":
    try:
        juego = AdivinanzasGame()
        juego.run()
    except KeyboardInterrupt:
        print("Programa terminado por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}. Programa terminado.")