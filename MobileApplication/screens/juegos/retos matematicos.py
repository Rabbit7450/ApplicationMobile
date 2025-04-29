import random
import time
import pyttsx3
import speech_recognition as sr
import json
import os
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from .base_game import BaseGame

class RetosMatematicosGame(BaseGame):
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

        # Archivo para guardar problemas personalizados y puntuación
        self.ARCHIVO_PROBLEMAS = str(ASSETS_DIR / "problemas_personalizados.json")
        self.ARCHIVO_PUNTUACION = str(ASSETS_DIR / "puntuacion.txt")

        # Lista inicial de problemas matemáticos por nivel
        self.problemas_inicial = [
            {"pregunta": "Cuántos dedos hay en una mano?", "respuesta": 5},
            {"pregunta": "Cuántas patas tiene un perro?", "respuesta": 4},
            {"pregunta": "Si tienes 3 manzanas y comes 1, cuántas te quedan?", "respuesta": 2},
            {"pregunta": "Cuántos colores tiene un arcoíris?", "respuesta": 7},
            {"pregunta": "Cuántos lados tiene un triángulo?", "respuesta": 3},
        ]

        self.problemas_primaria = [
            {"pregunta": "Cuánto es 5 más 3?", "respuesta": 8},
            {"pregunta": "Cuánto es 10 menos 4?", "respuesta": 6},
            {"pregunta": "Cuánto es 6 por 2?", "respuesta": 12},
            {"pregunta": "Cuánto es 15 dividido por 3?", "respuesta": 5},
            {"pregunta": "Cuánto es 8 más 7?", "respuesta": 15},
        ]

        self.problemas_secundaria = [
            {"pregunta": "Si x más 5 es igual a 12, cuánto es x?", "respuesta": 7},
            {"pregunta": "Cuál es el 20% de 50?", "respuesta": 10},
            {"pregunta": "Cuánto es 2 a la potencia 3?", "respuesta": 8},
            {"pregunta": "Si 3x es igual a 9, cuánto es x?", "respuesta": 3},
            {"pregunta": "Cuál es la raíz cuadrada de 16?", "respuesta": 4},
        ]

        # Cargar problemas personalizados
        self.problemas_personalizados = self.cargar_problemas_personalizados()
        self.todos_problemas = {
            "inicial": self.problemas_inicial + self.problemas_personalizados["inicial"],
            "primaria": self.problemas_primaria + self.problemas_personalizados["primaria"],
            "secundaria": self.problemas_secundaria + self.problemas_personalizados["secundaria"]
        }

        # Variables del juego
        self.puntuacion = self.cargar_puntuacion()
        self.problema_actual = None
        self.nivel_actual = "inicial"
        self.modo = "jugar"  # "jugar" o "agregar"

        super().__init__(**kwargs)

    def get_title(self):
        return "Retos Matemáticos"

    def get_description(self):
        return "¡Resuelve problemas matemáticos usando tu voz!"

    def create_content(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Botones de modo
        modo_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        jugar_btn = Button(text='Jugar', on_press=lambda x: self.cambiar_modo("jugar"))
        agregar_btn = Button(text='Agregar Problema', on_press=lambda x: self.cambiar_modo("agregar"))
        modo_layout.add_widget(jugar_btn)
        modo_layout.add_widget(agregar_btn)
        content.add_widget(modo_layout)

        # Área de juego
        self.game_area = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(self.game_area)

        # Iniciar el juego
        self.cambiar_modo("jugar")

        return content

    def cargar_problemas_personalizados(self):
        if os.path.exists(self.ARCHIVO_PROBLEMAS):
            with open(self.ARCHIVO_PROBLEMAS, "r") as f:
                return json.load(f)
        return {"inicial": [], "primaria": [], "secundaria": []}

    def guardar_problemas_personalizados(self):
        with open(self.ARCHIVO_PROBLEMAS, "w") as f:
            json.dump(self.problemas_personalizados, f)

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

    def escuchar_respuesta(self, mensaje="Por favor, di tu respuesta."):
        """Función para escuchar la respuesta del usuario mediante voz"""
        with sr.Microphone() as source:
            self.hablar(mensaje)
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"Escuché: {texto}")
                # Convertir la respuesta a número si es posible
                try:
                    return int(texto)
                except ValueError:
                    # Si el usuario dice "cinco" en lugar de "5", intentamos mapear palabras a números
                    numero_dict = {
                        "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
                        "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
                        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
                        "quince": 15
                    }
                    texto = texto.lower()
                    return numero_dict.get(texto, None)
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
            self.iniciar_agregar_problema()

    def iniciar_juego(self):
        # Seleccionar nivel
        nivel_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        for nivel in ["inicial", "primaria", "secundaria"]:
            btn = Button(text=nivel.title(), on_press=lambda x, n=nivel: self.seleccionar_nivel(n))
            nivel_layout.add_widget(btn)
        self.game_area.add_widget(nivel_layout)

        if not self.todos_problemas[self.nivel_actual]:
            self.game_area.add_widget(Label(text=f"No hay problemas disponibles para el nivel {self.nivel_actual}. Agrega algunos primero."))
            return

        self.problema_actual = random.choice(self.todos_problemas[self.nivel_actual])
        
        # Mostrar el problema
        self.game_area.add_widget(Label(text=self.problema_actual["pregunta"]))
        
        # Botón para responder
        responder_btn = Button(text="Responder", on_press=self.responder_problema)
        self.game_area.add_widget(responder_btn)

    def iniciar_agregar_problema(self):
        # Campos para agregar problema
        self.game_area.add_widget(Label(text="Agregar nuevo problema"))
        
        # Selección de nivel
        nivel_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        for nivel in ["inicial", "primaria", "secundaria"]:
            btn = Button(text=nivel.title(), on_press=lambda x, n=nivel: self.seleccionar_nivel_agregar(n))
            nivel_layout.add_widget(btn)
        self.game_area.add_widget(nivel_layout)
        
        # Campo para la pregunta
        self.pregunta_input = TextInput(multiline=True, hint_text="Escribe el problema")
        self.game_area.add_widget(self.pregunta_input)
        
        # Campo para la respuesta
        self.respuesta_input = TextInput(multiline=False, hint_text="Escribe la respuesta (número)")
        self.game_area.add_widget(self.respuesta_input)
        
        # Botón para guardar
        guardar_btn = Button(text="Guardar Problema", on_press=self.guardar_problema)
        self.game_area.add_widget(guardar_btn)

    def seleccionar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.iniciar_juego()

    def seleccionar_nivel_agregar(self, nivel):
        self.nivel_actual = nivel
        self.hablar(f"Nivel seleccionado: {nivel}")

    def responder_problema(self, instance):
        respuesta = self.escuchar_respuesta()
        if respuesta is None:
            return

        if respuesta == self.problema_actual["respuesta"]:
            self.hablar("¡Correcto! Muy bien.")
            self.puntuacion += 10
        else:
            self.hablar(f"Lo siento, eso no es correcto. La respuesta correcta era {self.problema_actual['respuesta']}.")
            self.puntuacion -= 5

        self.guardar_puntuacion()
        self.hablar(f"Tu puntuación ahora es {self.puntuacion}.")
        
        # Preguntar si quiere continuar
        self.hablar("¿Quieres otro problema? Di 'sí' o 'no'.")
        continuar = self.escuchar_respuesta()
        
        if continuar and ("sí" in str(continuar) or "si" in str(continuar)):
            self.iniciar_juego()
        else:
            self.hablar(f"¡Gracias por jugar! Tu puntuación final es {self.puntuacion} puntos.")

    def guardar_problema(self, instance):
        pregunta = self.pregunta_input.text.strip()
        respuesta = self.respuesta_input.text.strip()
        
        if not pregunta or not respuesta:
            self.hablar("Por favor, completa ambos campos.")
            return
        
        try:
            respuesta = int(respuesta)
        except ValueError:
            self.hablar("La respuesta debe ser un número.")
            return
        
        nuevo_problema = {"pregunta": pregunta, "respuesta": respuesta}
        self.problemas_personalizados[self.nivel_actual].append(nuevo_problema)
        self.todos_problemas[self.nivel_actual].append(nuevo_problema)
        self.guardar_problemas_personalizados()
        
        self.hablar(f"Problema agregado al nivel {self.nivel_actual}: {pregunta} Respuesta: {respuesta}")
        
        # Limpiar campos
        self.pregunta_input.text = ""
        self.respuesta_input.text = ""

if __name__ == "__main__":
    try:
        juego = RetosMatematicosGame()
        juego.run()
    except KeyboardInterrupt:
        print("Programa terminado por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}. Programa terminado.")