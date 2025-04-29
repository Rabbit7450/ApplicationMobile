import random
import time
import os
import sys
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from .base_game import BaseGame

# Dependencias para Vosk y PyAudio
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    import json
except ImportError:
    print("Faltan dependencias. Asegúrate de instalar 'vosk' y 'pyaudio' con:")
    print("pip install vosk pyaudio")
    sys.exit(1)

class ProyectoSocialGame(BaseGame):
    def __init__(self, **kwargs):
        # Obtener la ruta base del proyecto
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        ASSETS_DIR = BASE_DIR / 'assets' / 'juegos' / 'dependencias'

        # Crear directorio de dependencias si no existe
        os.makedirs(ASSETS_DIR, exist_ok=True)

        # Verificar si el modelo ya está descargado
        self.modelo_path = str(ASSETS_DIR / "vosk-model-es")
        if not os.path.exists(self.modelo_path):
            print(f"No se encuentra el modelo de voz offline. Por favor, descargue el modelo español de Vosk desde https://alphacephei.com/vosk/models y extráigalo en la carpeta {self.modelo_path}")

        # Diccionario de Braille
        self.braille_dict = {
            'a': [7],                  # ⠁
            'b': [7, 4],               # ⠃
            'c': [7, 8],               # ⠉
            'd': [7, 8, 5],            # ⠙
            'e': [7, 5],               # ⠑
            'f': [7, 8, 4],            # ⠋
            'g': [7, 8, 4, 5],         # ⠛
            'h': [7, 4, 5],            # ⠓
            'i': [4, 8],               # ⠊
            'j': [4, 5, 8],            # ⠚
            'k': [7, 1],               # ⠅
            'l': [7, 4, 1],            # ⠇
            'm': [7, 8, 1],            # ⠍
            'n': [7, 8, 5, 1],         # ⠝
            'o': [7, 5, 1],            # ⠕
            'p': [7, 8, 4, 1],         # ⠏
            'q': [7, 4, 1, 8, 5],      # ⠟
            'r': [7, 4, 1, 5],         # ⠗
            's': [4, 1, 8],            # ⠎
            't': [4, 1, 8, 5],         # ⠞
            'u': [7, 1, 2],            # ⠥
            'v': [7, 4, 1, 2],         # ⠧
            'w': [4, 8, 5, 2],         # ⠺
            'x': [7, 8, 1, 2],         # ⠭
            'y': [7, 1, 8, 5, 2],      # ⠽
            'z': [7, 1, 5, 2]          # ⠵
        }

        # Lista de palabras con pistas
        self.palabras_con_pistas = [
            ("python", "Lenguaje de programación nombrado como una serpiente"),
            ("braille", "Sistema de escritura táctil para personas con discapacidad visual"),
            ("teclado", "Dispositivo que usas para escribir en la computadora"),
            ("codigo", "Conjunto de instrucciones para una computadora"),
            ("juego", "Actividad recreativa con reglas"),
            ("sonido", "Lo que escuchas a través de tus oídos"),
            ("letra", "Unidad básica de la escritura"),
            ("palabra", "Conjunto de letras con significado"),
            ("audio", "Señal sonora"),
            ("acceso", "Posibilidad de entrada o paso")
        ]

        # Variables del juego
        self.palabra_actual = None
        self.pista_actual = None
        self.letras_adivinadas = set()
        self.intentos = 0

        super().__init__(**kwargs)

    def get_title(self):
        return "Crucigrama Braille"

    def get_description(self):
        return "¡Adivina palabras usando el sistema Braille!"

    def create_content(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        # Área de juego
        self.game_area = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(self.game_area)

        # Iniciar el juego
        self.iniciar_juego()

        return content

    def reproducir_sonido(self, tipo):
        if tipo == "correcto":
            print("\n🔊 SONIDO: ¡Correcto! 🎵")
            print('\a')  # Beep del sistema
        else:
            print("\n🔊 SONIDO: ¡Incorrecto! 🎵")
            print('\a')

    def hablar(self, texto):
        print(f"\n🔊 VOZ: {texto}")

    def escuchar(self):
        """Escuchar entrada de voz del usuario usando Vosk (funciona sin internet)"""
        try:
            # Verificar si el modelo ya está descargado
            if not os.path.exists(self.modelo_path):
                self.hablar("No se encuentra el modelo de voz offline. Por favor, descargue el modelo español de Vosk desde https://alphacephei.com/vosk/models y extráigalo en una carpeta llamada 'vosk-model-es' en el mismo directorio que este programa.")
                return ""

            # Cargar el modelo de español
            model = Model(self.modelo_path)
            recognizer = KaldiRecognizer(model, 16000)

            # Configurar PyAudio
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=4000)

            self.hablar("Escuchando...")
            stream.start_stream()

            # Añadir un tiempo de espera
            timeout = time.time() + 5  # 5 segundos de espera
            while True:
                if time.time() > timeout:
                    self.hablar("Tiempo de espera agotado. Intenta de nuevo.")
                    return ""

                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    texto = result.get("text", "")
                    if texto:
                        print(f"Usuario dijo: {texto}")
                        return texto

            result = json.loads(recognizer.FinalResult())
            texto = result.get("text", "")
            print(f"Usuario dijo: {texto}")
            return texto

        except Exception as e:
            print(f"Error en reconocimiento de voz: {e}")
            self.hablar("Error en el reconocimiento de voz offline. Si el problema persiste, verifique la instalación de Vosk y el modelo de idioma.")
            return ""
        finally:
            try:
                stream.stop_stream()
                stream.close()
                p.terminate()
            except:
                pass

    def verificar_braille(self, entrada, letra):
        teclas = set([int(num) for num in entrada if num in "12457" or num in "12458"])
        print(f"Verificando letra '{letra}': patrón esperado {self.braille_dict.get(letra.lower(), [])} vs. entrada {teclas}")
        return set(self.braille_dict.get(letra.lower(), [])) == teclas

    def obtener_entrada_braille(self):
        intentos = 0
        max_intentos = 3
        numero_dict = {
            "uno": "1", "dos": "2", "cuatro": "4", "cinco": "5", "siete": "7", "ocho": "8",
            "1": "1", "2": "2", "4": "4", "5": "5", "7": "7", "8": "8"
        }
        while intentos < max_intentos:
            self.hablar("Di los números para la letra en Braille usando 1, 2, 4, 5, 7, 8. Por ejemplo, di '7' para la letra 'a'. Habla despacio y claramente.")
            entrada_voz = self.escuchar()

            if not entrada_voz:
                intentos += 1
                self.hablar(f"No entendí lo que dijiste. Intenta de nuevo. Intento {intentos} de {max_intentos}.")
                continue

            # Convertir palabras a números
            entrada_voz = entrada_voz.lower()
            numeros = []
            for palabra in entrada_voz.split():
                if palabra in numero_dict:
                    numeros.append(numero_dict[palabra])
            entrada_voz = "".join(numeros)

            if all(char in "12457" for char in entrada_voz) or all(char in "12458" for char in entrada_voz):
                if entrada_voz:
                    return entrada_voz

            intentos += 1
            self.hablar(f"Entrada inválida. Solo usa los números 1, 2, 4, 5, 7, 8. Intenta de nuevo. Intento {intentos} de {max_intentos}.")

        self.hablar("Demasiados intentos fallidos. Saltando este turno.")
        return ""

    def convertir_a_letra(self, entrada):
        conjunto_entrada = set([int(num) for num in entrada if num in "12457" or num in "12458"])
        print(f"Conjunto de entrada: {conjunto_entrada}")

        for letra, puntos in self.braille_dict.items():
            if set(puntos) == conjunto_entrada:
                return letra

        print("No se encontró coincidencia exacta.")

        opciones_similares = []
        for letra, puntos in self.braille_dict.items():
            coincidencias = len(set(puntos).intersection(conjunto_entrada))
            if coincidencias > 0:
                opciones_similares.append((letra, puntos, coincidencias))

        if opciones_similares:
            print("Opciones similares:")
            for letra, puntos, coincidencias in sorted(opciones_similares, key=lambda x: x[2], reverse=True)[:5]:
                print(f"{letra}: {puntos} ({coincidencias} coincidencias)")

        return None

    def mostrar_crucigrama(self):
        resultado = ""
        for letra in self.palabra_actual:
            if letra in self.letras_adivinadas:
                resultado += letra + " "
            else:
                resultado += "_ "
        
        self.game_area.clear_widgets()
        self.game_area.add_widget(Label(text="Palabra actual:"))
        self.game_area.add_widget(Label(text=resultado))
        
        if self.letras_adivinadas:
            self.game_area.add_widget(Label(text="Letras adivinadas: " + ", ".join(sorted(self.letras_adivinadas))))
        
        return resultado

    def iniciar_juego(self):
        self.palabra_actual, self.pista_actual = random.choice(self.palabras_con_pistas)
        self.letras_adivinadas = set()
        self.intentos = 0

        self.game_area.clear_widgets()
        self.game_area.add_widget(Label(text=f"Pista: {self.pista_actual}"))
        self.game_area.add_widget(Label(text=f"La palabra tiene {len(self.palabra_actual)} letras."))

        self.mostrar_crucigrama()

        # Botón para adivinar letra
        adivinar_btn = Button(text="Adivinar Letra", on_press=self.adivinar_letra)
        self.game_area.add_widget(adivinar_btn)

    def adivinar_letra(self, instance):
        self.hablar("Di los números para una letra en Braille")

        entrada = self.obtener_entrada_braille()
        if not entrada:  # Si se agotaron los intentos
            return

        letra_ingresada = self.convertir_a_letra(entrada)

        if letra_ingresada is None:
            self.hablar("No reconozco ese patrón Braille. Intenta de nuevo.")
            return

        self.hablar(f"Has ingresado la letra: {letra_ingresada}")

        self.intentos += 1

        if letra_ingresada in self.palabra_actual:
            self.letras_adivinadas.add(letra_ingresada)
            self.hablar("¡Correcto!")
            self.reproducir_sonido("correcto")
        else:
            self.hablar("Esa letra no está en la palabra.")
            self.reproducir_sonido("incorrecto")

        progreso = self.mostrar_crucigrama()

        if "_" not in progreso:
            self.hablar(f"¡Felicidades! Has completado la palabra '{self.palabra_actual}' en {self.intentos} intentos.")
            # Preguntar si quiere jugar de nuevo
            self.hablar("¿Quieres jugar de nuevo? Di 'sí' o 'no'.")
            respuesta = self.escuchar()
            if respuesta and ("sí" in respuesta.lower() or "si" in respuesta.lower()):
                self.iniciar_juego()
            else:
                self.hablar("¡Gracias por jugar!")

if __name__ == "__main__":
    try:
        juego = ProyectoSocialGame()
        juego.run()
    except KeyboardInterrupt:
        print("Programa terminado por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}. Programa terminado.")