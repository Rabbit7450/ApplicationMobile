import speech_recognition as sr
import pyttsx3
import chess
import chess.engine
import random
import time
import os
import json
from difflib import get_close_matches
from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / 'assets' / 'juegos' / 'dependencias'

# Crear directorio de dependencias si no existe
os.makedirs(ASSETS_DIR, exist_ok=True)

class AjedrezAccesible:
    def __init__(self):
        # Inicializar el reconocimiento de voz
        self.recognizer = sr.Recognizer()
        
        # Inicializar el motor de texto a voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)  # Velocidad de habla
        self.engine.setProperty('volume', 1.0)  # Volumen máximo
        
        # Configurar voces en español si están disponibles
        voices = self.engine.getProperty('voices')
        spanish_voice = None
        for voice in voices:
            if "spanish" in voice.name.lower() or "español" in voice.name.lower():
                spanish_voice = voice.id
                break
        if spanish_voice:
            self.engine.setProperty('voice', spanish_voice)
            
        # Tablero de ajedrez
        self.board = chess.Board()
        
        # Usuario actual
        self.usuario_actual = None
        
        # Base de datos de usuarios (progreso)
        self.base_usuarios = self.cargar_usuarios()
        
        # Niveles de aprendizaje
        self.niveles = {
            1: "Piezas y movimientos básicos",
            2: "Valor de las piezas y capturas",
            3: "Jaque, jaque mate y tablas",
            4: "Aperturas básicas", 
            5: "Táctica básica",
            6: "Estrategia media",
            7: "Finales básicos",
            8: "Aperturas intermedias",
            9: "Táctica avanzada",
            10: "Estrategia avanzada",
            11: "Finales avanzados",
            12: "Preparación para torneos"
        }
        
        # Comandos disponibles
        self.comandos = {
            "ayuda": "Recitar comandos disponibles",
            "salir": "Salir del programa",
            "niveles": "Listar niveles de aprendizaje",
            "nivel actual": "Indicar nivel actual",
            "iniciar nivel": "Iniciar el nivel actual",
            "repetir": "Repetir último mensaje",
            "aprender": "Iniciar módulo de aprendizaje",
            "practicar": "Iniciar módulo de práctica",
            "evaluar": "Evaluar nivel para avanzar",
            "estado tablero": "Describir estado actual del tablero",
            "mover": "Realizar movimiento (ejemplo: 'mover peón de e2 a e4')",
            "letra": "Obtener explicación de notación (ejemplo: 'letra a')",
            "posición": "Obtener explicación de casilla (ejemplo: 'posición a1')",
            "reiniciar tablero": "Reiniciar posición del tablero",
            "último movimiento": "Repetir último movimiento",
            "registrar usuario": "Crear un nuevo perfil de usuario",
            "cambiar usuario": "Seleccionar otro usuario existente",
            "progreso": "Consultar progreso del usuario actual"
        }
        
        # Último mensaje hablado (para el comando "repetir")
        self.ultimo_mensaje = ""
        
        # Diccionario de pronunciación para piezas y casillas
        self.pronunciacion = {
            "P": "peón", "N": "caballo", "B": "alfil", 
            "R": "torre", "Q": "dama", "K": "rey",
            "a": "a", "b": "b", "c": "c", "d": "d", 
            "e": "e", "f": "f", "g": "g", "h": "h",
        }
        
        # Diccionario para convertir comandos de voz a movimientos
        self.traduccion_piezas = {
            "peón": "p", "peon": "p", 
            "torre": "r", 
            "caballo": "n", 
            "alfil": "b", 
            "dama": "q", "reina": "q",
            "rey": "k"
        }
        
        # Lecciones por nivel
        self.lecciones = self.cargar_lecciones()
    
    def cargar_usuarios(self):
        """Cargar la base de datos de usuarios desde un archivo JSON"""
        try:
            usuarios_file = ASSETS_DIR / 'usuarios_ajedrez.json'
            if usuarios_file.exists():
                with open(usuarios_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.hablar(f"Error al cargar la base de datos de usuarios: {e}")
        return {}
    
    def guardar_usuarios(self):
        """Guardar la base de datos de usuarios en un archivo JSON"""
        try:
            usuarios_file = ASSETS_DIR / 'usuarios_ajedrez.json'
            with open(usuarios_file, 'w') as f:
                json.dump(self.base_usuarios, f, indent=4)
        except Exception as e:
            self.hablar(f"Error al guardar la base de datos de usuarios: {e}")
    
    def registrar_usuario(self):
        """Registrar un nuevo usuario"""
        self.hablar("Por favor, diga su nombre para registrarse")
        nombre = self.escuchar()
        
        if nombre:
            if nombre in self.base_usuarios:
                self.hablar(f"El usuario {nombre} ya existe. ¿Desea continuar con este usuario?")
                respuesta = self.escuchar()
                if "si" in respuesta.lower() or "sí" in respuesta.lower():
                    self.usuario_actual = nombre
                    self.hablar(f"Bienvenido nuevamente, {nombre}. Su nivel actual es {self.base_usuarios[nombre]['nivel']}")
                else:
                    self.hablar("Registro cancelado")
            else:
                # Nuevo usuario
                self.base_usuarios[nombre] = {
                    "nivel": 1,
                    "lecciones_completadas": [],
                    "ejercicios_completados": []
                }
                self.usuario_actual = nombre
                self.guardar_usuarios()
                self.hablar(f"Bienvenido, {nombre}. Ha sido registrado correctamente. Comenzará desde el nivel 1.")
        else:
            self.hablar("No se pudo registrar el nombre. Por favor intente nuevamente.")
    
    def cambiar_usuario(self):
        """Cambiar a un usuario existente"""
        self.hablar("Por favor, diga el nombre del usuario")
        nombre = self.escuchar()
        
        if nombre:
            if nombre in self.base_usuarios:
                self.usuario_actual = nombre
                self.hablar(f"Bienvenido, {nombre}. Su nivel actual es {self.base_usuarios[nombre]['nivel']}")
            else:
                self.hablar(f"El usuario {nombre} no existe. ¿Desea registrarse como nuevo usuario?")
                respuesta = self.escuchar()
                if "si" in respuesta.lower() or "sí" in respuesta.lower():
                    self.registrar_usuario()
                else:
                    self.hablar("Cambio de usuario cancelado")
        else:
            self.hablar("No se pudo entender el nombre. Por favor intente nuevamente.")
    
    def cargar_lecciones(self):
        """Cargar las lecciones para cada nivel"""
        lecciones = {
            # Nivel 1: Piezas y movimientos básicos
            1: [
                {
                    "titulo": "El tablero de ajedrez",
                    "contenido": "El tablero de ajedrez tiene 8 filas y 8 columnas, formando 64 casillas. "
                                "Las columnas se nombran con letras de la A a la H, y las filas con números del 1 al 8. "
                                "Cada casilla se identifica por su columna y fila, por ejemplo: A1, E5, H8."
                },
                {
                    "titulo": "El peón",
                    "contenido": "El peón es la pieza más numerosa y se mueve una casilla hacia adelante. "
                                "En su primer movimiento puede avanzar dos casillas. "
                                "Captura en diagonal hacia adelante. Si llega a la última fila, se promociona a otra pieza."
                },
                {
                    "titulo": "La torre",
                    "contenido": "La torre se mueve en línea recta horizontal o vertical, cuantas casillas desee. "
                                "No puede saltar sobre otras piezas. Captura ocupando la casilla del oponente."
                },
                {
                    "titulo": "El alfil",
                    "contenido": "El alfil se mueve en diagonal, cuantas casillas desee. "
                                "No puede saltar sobre otras piezas. Captura ocupando la casilla del oponente."
                },
                {
                    "titulo": "La dama",
                    "contenido": "La dama es la pieza más poderosa. Combina los movimientos de la torre y el alfil. "
                                "Se mueve en línea recta o diagonal, cuantas casillas desee. "
                                "No puede saltar sobre otras piezas. Captura ocupando la casilla del oponente."
                },
                {
                    "titulo": "El rey",
                    "contenido": "El rey se mueve una casilla en cualquier dirección: horizontal, vertical o diagonal. "
                                "Es la pieza más importante, si es capturado (jaque mate) se pierde la partida."
                },
                {
                    "titulo": "El caballo",
                    "contenido": "El caballo se mueve en forma de L: dos casillas en una dirección y luego una perpendicular. "
                                "Es la única pieza que puede saltar sobre otras. Captura ocupando la casilla del oponente."
                }
            ],
            
            # Nivel 2: Valor de las piezas y capturas
            2: [
                {
                    "titulo": "Valor de las piezas",
                    "contenido": "Cada pieza tiene un valor aproximado: Peón vale 1 punto, Caballo y Alfil valen 3 puntos cada uno, "
                                "Torre vale 5 puntos, Dama vale 9 puntos. El Rey tiene valor infinito ya que su captura significa perder el juego."
                },
                {
                    "titulo": "Capturas básicas",
                    "contenido": "Capturar significa tomar el lugar de una pieza enemiga, retirándola del tablero. "
                                "Es generalmente ventajoso capturar piezas de mayor valor con piezas de menor valor."
                },
                {
                    "titulo": "Intercambios favorables",
                    "contenido": "Un intercambio favorable ocurre cuando capturamos una pieza de mayor valor que la nuestra. "
                                "Por ejemplo, capturar una torre (5 puntos) con un caballo (3 puntos)."
                }
            ],
            
            # Nivel 3: Jaque, jaque mate y tablas
            3: [
                {
                    "titulo": "Jaque",
                    "contenido": "Jaque ocurre cuando el rey está amenazado por una pieza enemiga. "
                                "Cuando hay jaque, es obligatorio salir del jaque en el siguiente movimiento, "
                                "ya sea moviendo el rey, capturando la pieza atacante, o interponiendo una pieza."
                },
                {
                    "titulo": "Jaque mate",
                    "contenido": "Jaque mate ocurre cuando el rey está en jaque y no hay forma de salir del jaque. "
                                "El jaque mate significa el fin de la partida y la victoria para quien lo da."
                },
                {
                    "titulo": "Tablas por ahogado",
                    "contenido": "Se produce cuando un jugador no tiene movimientos legales y su rey NO está en jaque. "
                                "El resultado es empate."
                },
                {
                    "titulo": "Otras formas de tablas",
                    "contenido": "Las tablas o empate también pueden producirse por repetición de posición tres veces, "
                                "por la regla de 50 movimientos sin capturas ni movimientos de peón, "
                                "o cuando no hay material suficiente para dar mate (como Rey contra Rey)."
                }
            ],
            
            # Nivel 4: Aperturas básicas
            4: [
                {
                    "titulo": "Principios de apertura",
                    "contenido": "En la apertura es importante: desarrollar las piezas rápidamente, "
                                "controlar el centro del tablero, asegurar el rey mediante el enroque, "
                                "y conectar las torres."
                },
                {
                    "titulo": "Apertura española",
                    "contenido": "La apertura española comienza con los movimientos: 1.e4 e5 2.Cf3 Cc6 3.Ab5. "
                                "Es una de las aperturas más antiguas y respetadas del ajedrez."
                },
                {
                    "titulo": "Defensa siciliana",
                    "contenido": "La defensa siciliana comienza con 1.e4 c5. Es una defensa agresiva y desequilibrada, "
                                "muy popular a todos los niveles."
                }
            ],
            
            # Nivel 5: Táctica básica
            5: [
                {
                    "titulo": "Clavada",
                    "contenido": "Una clavada ocurre cuando una pieza no puede moverse porque expondría una pieza más valiosa detrás de ella, "
                                "generalmente el rey."
                },
                {
                    "titulo": "Horquilla",
                    "contenido": "Una horquilla sucede cuando una pieza ataca simultáneamente dos o más piezas del oponente."
                },
                {
                    "titulo": "Ataque doble",
                    "contenido": "Similar a la horquilla, pero realizado con dos piezas diferentes atacando un mismo objetivo."
                }
            ],
            
            # Nivel 6: Estrategia media
            6: [
                {
                    "titulo": "Peones aislados y doblados",
                    "contenido": "Los peones aislados no tienen peones amigos en columnas adyacentes. Los peones doblados son dos peones del mismo color en la misma columna. Ambas estructuras suelen representar debilidades."
                },
                {
                    "titulo": "Piezas activas vs pasivas",
                    "contenido": "Las piezas activas controlan muchas casillas y tienen buen alcance. Las piezas pasivas están bloqueadas o limitadas. Busca siempre maximizar la actividad de tus piezas."
                },
                {
                    "titulo": "Control del centro",
                    "contenido": "El control de las casillas centrales (d4, d5, e4, e5) proporciona ventajas posicionales importantes, dando más espacio y opciones de movimiento."
                }
            ],
            
            # Nivel 7: Finales básicos
            7: [
                {
                    "titulo": "Final de rey y peón contra rey",
                    "contenido": "En este final, la regla de la oposición y el conocimiento de casillas clave son fundamentales. El rey defensor debe intentar bloquear el avance del peón."
                },
                {
                    "titulo": "Final de torre",
                    "contenido": "Los finales de torre son los más comunes. La torre debe colocarse detrás del peón pasado, ya sea propio para apoyarlo o enemigo para frenarlo."
                },
                {
                    "titulo": "La regla del cuadrado",
                    "contenido": "Para saber si un rey puede alcanzar a un peón, imagina un cuadrado desde el peón hasta la casilla de promoción. Si el rey puede entrar en ese cuadrado, atrapará al peón."
                }
            ],
            
            # Nivel 8: Aperturas intermedias
            8: [
                {
                    "titulo": "Apertura inglesa",
                    "contenido": "Comienza con 1.c4. Es una apertura flexible que puede transponer a diversas estructuras."
                },
                {
                    "titulo": "Defensa francesa",
                    "contenido": "Comienza con 1.e4 e6. Es una defensa sólida donde las negras buscan contrajuego en el flanco de dama."
                },
                {
                    "titulo": "Gambito de dama",
                    "contenido": "Comienza con 1.d4 d5 2.c4. Las blancas ofrecen un peón temporalmente para acelerar su desarrollo y el control del centro."
                }
            ],
            
            # Nivel 9: Táctica avanzada
            9: [
                {
                    "titulo": "Sacrificios",
                    "contenido": "Un sacrificio es entregar material voluntariamente para obtener ventajas posicionales o iniciar un ataque decisivo."
                },
                {
                    "titulo": "Ataque descubierto",
                    "contenido": "Ocurre cuando una pieza se mueve y revela un ataque desde otra pieza que estaba detrás."
                },
                {
                    "titulo": "Desviación",
                    "contenido": "Táctica que consiste en apartar una pieza defensiva de su función, generalmente mediante un sacrificio."
                }
            ],
            
            # Nivel 10: Estrategia avanzada
            10: [
                {
                    "titulo": "Estructura de peones",
                    "contenido": "La disposición de los peones determina en gran medida el carácter de la posición y los planes estratégicos a seguir."
                },
                {
                    "titulo": "Juego en el flanco de dama",
                    "contenido": "Estrategia que busca crear debilidades y aprovecharlas en el lado de la dama (columnas a, b, c)."
                },
                {
                    "titulo": "El alfil bueno y el alfil malo",
                    "contenido": "Un alfil bueno opera en diagonales abiertas. Un alfil malo es limitado por sus propios peones. La diferencia puede ser decisiva en muchas posiciones."
                }
            ],
            
            # Nivel 11: Finales avanzados
            11: [
                {
                    "titulo": "Final de dama contra peón en séptima",
                    "contenido": "En este final, la técnica correcta depende de la posición del peón y de los reyes. Hay posiciones donde incluso la poderosa dama no puede impedir la promoción."
                },
                {
                    "titulo": "Final de alfil y caballo contra rey",
                    "contenido": "Es un mate teórico pero difícil de ejecutar. Requiere técnica precisa y conocimiento de patrones específicos para arrinconar al rey."
                },
                {
                    "titulo": "Zugzwang",
                    "contenido": "Una posición donde cualquier movimiento empeora la situación. Es particularmente importante en finales, donde a veces la obligación de mover determina la victoria o derrota."
                }
            ],
            
            # Nivel 12: Preparación para torneos
            12: [
                {
                    "titulo": "Preparación de aperturas",
                    "contenido": "En torneos es crucial preparar un repertorio sólido de aperturas, estudiando variantes específicas y comprendiendo los planes mediojuego asociados."
                },
                {
                    "titulo": "Gestión del tiempo",
                    "contenido": "El manejo adecuado del reloj es fundamental en ajedrez competitivo. Distribuye tu tiempo según la complejidad de la posición."
                },
                {
                    "titulo": "Psicología en el ajedrez",
                    "contenido": "En torneos, factores como la resistencia mental, la gestión de emociones y la capacidad para recuperarse de derrotas son tan importantes como el conocimiento técnico."
                }
            ]
        }
        return lecciones
    
    def hablar(self, texto):
        """Función para que el programa hable"""
        self.ultimo_mensaje = texto
        print(f"Programa: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()
    
    def escuchar(self):
        """Escuchar entrada de voz del usuario usando Vosk (funciona sin internet)"""
        try:
            from vosk import Model, KaldiRecognizer
            import pyaudio
            import json
            import os
            
            # Verificar si el modelo ya está descargado, si no, notificar al usuario
            modelo_path = "vosk-model-es"
            if not os.path.exists(modelo_path):
                self.hablar("No se encuentra el modelo de voz offline. Por favor, descargue el modelo español de Vosk desde https://alphacephei.com/vosk/models y extráigalo en una carpeta llamada 'vosk-model-es' en el mismo directorio que este programa.")
                return ""
            
            # Cargar el modelo de español
            model = Model(modelo_path)
            recognizer = KaldiRecognizer(model, 16000)
            
            # Configurar PyAudio
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, 
                            channels=1, 
                            rate=16000, 
                            input=True, 
                            frames_per_buffer=8000)
            
            self.hablar("Escuchando...")
            
            # Iniciar la grabación
            stream.start_stream()
            
            # Bucle de reconocimiento
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                
                # Procesar audio con Vosk
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    texto = result.get("text", "")
                    if texto:
                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        print(f"Usuario: {texto}")
                        return texto
            
            # Si llegamos aquí, finalizar la grabación y devolver texto final
            stream.stop_stream()
            stream.close()
            p.terminate()
            result = json.loads(recognizer.FinalResult())
            texto = result.get("text", "")
            print(f"Usuario: {texto}")
            return texto
            
        except Exception as e:
            print(f"Error en reconocimiento de voz: {e}")
            # Caer en modo de respaldo si Vosk falla
            self.hablar("Error en el reconocimiento de voz offline. Si el problema persiste, verifique la instalación de Vosk y el modelo de idioma.")
            return ""
    
    def comando_mas_similar(self, comando):
        """Encuentra el comando más similar al comando dado"""
        comandos = list(self.comandos.keys())
        matches = get_close_matches(comando, comandos, n=1, cutoff=0.6)
        return matches[0] if matches else None
    
    def listar_niveles(self):
        """Listar todos los niveles disponibles"""
        self.hablar("Los niveles disponibles son:")
        for num, desc in self.niveles.items():
            self.hablar(f"Nivel {num}: {desc}")
    
    def listar_comandos(self):
        """Listar todos los comandos disponibles"""
        self.hablar("Los comandos disponibles son:")
        for cmd, desc in self.comandos.items():
            self.hablar(f"{cmd}: {desc}")
    
    def describir_tablero(self):
        """Describir el estado actual del tablero de manera accesible"""
        if self.board.is_checkmate():
            self.hablar("Jaque mate. La partida ha terminado.")
            return
        
        if self.board.is_stalemate():
            self.hablar("Tablas por ahogado. La partida ha terminado.")
            return
        
        if self.board.is_check():
            self.hablar(f"{'Las blancas están' if self.board.turn else 'Las negras están'} en jaque.")
        
        self.hablar("Describiré el tablero por filas, de la 8 a la 1:")
        
        for fila in range(7, -1, -1):  # Del 7 (fila 8) al 0 (fila 1)
            contenido_fila = f"Fila {fila + 1}: "
            for columna in range(8):  # De la columna a (0) a la h (7)
                casilla = chess.square(columna, fila)
                pieza = self.board.piece_at(casilla)
                letra_columna = chr(97 + columna)  # 'a' es ASCII 97
                
                if pieza:
                    color = "blanca" if pieza.color else "negra"
                    nombre_pieza = self.pronunciacion.get(pieza.symbol().upper(), pieza.symbol().upper())
                    contenido_fila += f"{nombre_pieza} {color} en {letra_columna}{fila + 1}, "
            
            if "en" in contenido_fila:  # Solo hablar de filas con piezas
                self.hablar(contenido_fila)
    
    def explicar_notacion(self, letra):
        """Explicar la notación algebraica de una letra de columna"""
        if letra.lower() in "abcdefgh":
            self.hablar(f"La letra {letra} corresponde a la columna {letra} del tablero, contando desde la izquierda.")
        else:
            self.hablar(f"La letra {letra} no es una columna válida del tablero. Las columnas van de la A a la H.")
    
    def explicar_posicion(self, posicion):
        """Explicar una posición en el tablero"""
        if len(posicion) == 2 and posicion[0].lower() in "abcdefgh" and posicion[1] in "12345678":
            letra = posicion[0].lower()
            numero = posicion[1]
            color = "blanca" if (ord(letra) - ord('a') + int(numero)) % 2 == 0 else "negra"
            self.hablar(f"La casilla {letra}{numero} está en la columna {letra} y fila {numero}. Es una casilla {color}.")
            
            # Verificar si hay una pieza en esa posición
            try:
                columna = ord(letra) - ord('a')
                fila = int(numero) - 1
                casilla = chess.square(columna, fila)
                pieza = self.board.piece_at(casilla)
                
                if pieza:
                    color_pieza = "blanca" if pieza.color else "negra"
                    nombre_pieza = self.pronunciacion.get(pieza.symbol().upper(), pieza.symbol().upper())
                    self.hablar(f"En esta casilla hay un {nombre_pieza} {color_pieza}.")
                else:
                    self.hablar("No hay ninguna pieza en esta casilla.")
            except Exception as e:
                self.hablar(f"Error al verificar la pieza: {str(e)}")
        else:
            self.hablar(f"La posición {posicion} no es válida. Debe ser una letra de la A a la H seguida de un número del 1 al 8.")
    
    def procesar_movimiento_voz(self, comando):
        """Procesar un movimiento expresado por voz"""
        try:
            # Formato esperado: "mover [pieza] de [origen] a [destino]"
            if "mover" not in comando:
                self.hablar("Para mover una pieza, diga 'mover' seguido de la pieza y las casillas.")
                return
            
            partes = comando.split()
            if len(partes) < 6:
                self.hablar("Formato incorrecto. Diga por ejemplo: 'mover peón de e2 a e4'.")
                return
            
            # Extraer información del comando
            indice_pieza = partes.index("mover") + 1 if "mover" in partes else -1
            indice_origen = partes.index("de") + 1 if "de" in partes else -1
            indice_destino = partes.index("a") + 1 if "a" in partes else -1
            
            if indice_pieza == -1 or indice_origen == -1 or indice_destino == -1:
                self.hablar("No pude entender el movimiento. Use el formato: 'mover peón de e2 a e4'.")
                return
            
            nombre_pieza = partes[indice_pieza].lower()
            origen = partes[indice_origen].lower()
            destino = partes[indice_destino].lower()
            
            # Validar casillas
            if (len(origen) != 2 or len(destino) != 2 or 
                origen[0] not in "abcdefgh" or destino[0] not in "abcdefgh" or
                origen[1] not in "12345678" or destino[1] not in "12345678"):
                self.hablar("Casillas inválidas. Deben ser una letra a-h seguida de un número 1-8.")
                return
            
            # Construir movimiento en notación UCI (Universal Chess Interface)
            movimiento_uci = origen + destino
            
            # Verificar si es una promoción
            if "promoción" in comando or "promocion" in comando or "promover" in comando:
                for palabra in partes:
                    if palabra.lower() in self.traduccion_piezas:
                        pieza_promocion = self.traduccion_piezas[palabra.lower()]
                        movimiento_uci += pieza_promocion
                        break
            
            # Validar y ejecutar movimiento
            try:
                movimiento = chess.Move.from_uci(movimiento_uci)
                if movimiento in self.board.legal_moves:
                    # Guardar el movimiento para poder repetirlo si se pide
                    self.ultimo_movimiento = movimiento_uci
                    
                    # Ejecutar el movimiento
                    self.board.push(movimiento)
                    
                    # Informar del movimiento realizado
                    self.hablar(f"Movimiento realizado: {origen} a {destino}")
                    
                    # Verificar si hay jaque, jaque mate o tablas
                    if self.board.is_checkmate():
                        self.hablar("¡Jaque mate! La partida ha terminado.")
                    elif self.board.is_check():
                        self.hablar("¡Jaque!")
                    elif self.board.is_stalemate():
                        self.hablar("¡Tablas por ahogado! La partida ha terminado.")
                    elif self.board.is_insufficient_material():
                        self.hablar("¡Tablas por material insuficiente! La partida ha terminado.")
                else:
                    self.hablar("Movimiento no permitido. Intente otro movimiento.")
            except ValueError:
                self.hablar("Movimiento inválido. Verifique las casillas de origen y destino.")
        
        except Exception as e:
            self.hablar(f"Error general al procesar el comando: {str(e)}")
    
    def repetir_ultimo_movimiento(self):
        """Repetir el último movimiento realizado"""
        if hasattr(self, 'ultimo_movimiento') and self.ultimo_movimiento:
            origen = self.ultimo_movimiento[:2]
            destino = self.ultimo_movimiento[2:4]
            self.hablar(f"El último movimiento fue de {origen} a {destino}")
        else:
            self.hablar("No hay movimientos previos para repetir.")
    
    def iniciar_nivel(self):
        """Iniciar el nivel actual del usuario"""
        if not self.usuario_actual:
            self.hablar("Primero debe registrarse o seleccionar un usuario.")
            return
            
        nivel_actual = self.base_usuarios[self.usuario_actual]['nivel']
        if nivel_actual > len(self.niveles):
            self.hablar("¡Felicidades! Ha completado todos los niveles disponibles.")
            return
            
        self.hablar(f"Iniciando nivel {nivel_actual}: {self.niveles[nivel_actual]}")
        
        # Verificar si hay lecciones para este nivel
        if nivel_actual in self.lecciones:
            lecciones_nivel = self.lecciones[nivel_actual]
            lecciones_completadas = self.base_usuarios[self.usuario_actual]['lecciones_completadas']
            
            # Buscar la primera lección no completada
            for i, leccion in enumerate(lecciones_nivel):
                leccion_id = f"{nivel_actual}-{i+1}"
                if leccion_id not in lecciones_completadas:
                    self.impartir_leccion(nivel_actual, i+1, leccion)
                    return
                    
            # Si todas las lecciones están completadas
            self.hablar("Ha completado todas las lecciones de este nivel. ¿Desea hacer una evaluación para avanzar al siguiente nivel?")
            respuesta = self.escuchar()
            if respuesta and ("sí" in respuesta.lower() or "si" in respuesta.lower()):
                self.evaluar_nivel()
            else:
                self.hablar("Puede repasar las lecciones o practicar cuando desee.")
        else:
            self.hablar("No hay lecciones disponibles para este nivel.")
    
    def impartir_leccion(self, nivel, num_leccion, leccion):
        """Impartir una lección específica"""
        leccion_id = f"{nivel}-{num_leccion}"
        
        self.hablar(f"Lección {num_leccion}: {leccion['titulo']}")
        self.hablar(leccion['contenido'])
        
        # Marcar lección como completada
        self.hablar("¿Ha comprendido la lección? Diga 'sí' para continuar.")
        respuesta = self.escuchar()
        if respuesta and ("sí" in respuesta.lower() or "si" in respuesta.lower()):
            if self.usuario_actual:
                if leccion_id not in self.base_usuarios[self.usuario_actual]['lecciones_completadas']:
                    self.base_usuarios[self.usuario_actual]['lecciones_completadas'].append(leccion_id)
                    self.guardar_usuarios()
                    self.hablar(f"Lección {num_leccion} completada correctamente.")
                else:
                    self.hablar("Esta lección ya estaba marcada como completada.")
            else:
                self.hablar("Lección completada, pero no se registrará su progreso porque no ha iniciado sesión.")
        else:
            self.hablar("Puede repasar esta lección más tarde cuando lo desee.")
    
    def evaluar_nivel(self):
        """Evaluar al usuario para ver si puede avanzar de nivel"""
        if not self.usuario_actual:
            self.hablar("Primero debe registrarse o seleccionar un usuario.")
            return
            
        nivel_actual = self.base_usuarios[self.usuario_actual]['nivel']
        
        self.hablar(f"Iniciando evaluación para el nivel {nivel_actual}.")
        self.hablar("Responderá algunas preguntas para evaluar su comprensión.")
        
        # Aquí irían preguntas específicas para cada nivel
        # Por ahora, implementamos una versión simplificada
        
        preguntas = {
            1: [
                ("¿Cómo se mueve el peón?", ["adelante", "avanza", "frente"]),
                ("¿Cómo se mueve el caballo?", ["l", "ele", "salto"]),
                ("¿Cuántas casillas tiene el tablero?", ["64", "sesenta y cuatro"])
            ],
            2: [
                ("¿Cuánto vale un alfil?", ["3", "tres"]),
                ("¿Cuánto vale una dama?", ["9", "nueve"]),
                ("¿Es favorable capturar una torre con un peón?", ["sí", "si", "claro"])
            ],
            # Se pueden añadir más preguntas para más niveles
        }
        
        # Si no hay preguntas para este nivel, avanzar automáticamente
        if nivel_actual not in preguntas:
            self.hablar("No hay evaluación disponible para este nivel. Avanzando automáticamente.")
            self.base_usuarios[self.usuario_actual]['nivel'] += 1
            self.guardar_usuarios()
            self.hablar(f"¡Felicidades! Ha avanzado al nivel {self.base_usuarios[self.usuario_actual]['nivel']}.")
            return
            
        # Realizar evaluación
        preguntas_nivel = preguntas[nivel_actual]
        aciertos = 0
        
        for pregunta, respuestas_correctas in preguntas_nivel:
            self.hablar(pregunta)
            respuesta = self.escuchar()
            
            if respuesta:
                # Verificar si la respuesta es correcta
                es_correcta = False
                for r in respuestas_correctas:
                    if r in respuesta.lower():
                        es_correcta = True
                        break
                        
                if es_correcta:
                    self.hablar("¡Correcto!")
                    aciertos += 1
                else:
                    self.hablar("Incorrecto.")
            else:
                self.hablar("No se detectó respuesta. Pasando a la siguiente pregunta.")
        
        # Evaluar resultado
        porcentaje = (aciertos / len(preguntas_nivel)) * 100
        self.hablar(f"Ha obtenido {aciertos} de {len(preguntas_nivel)} respuestas correctas ({porcentaje:.1f}%).")
        
        if porcentaje >= 70:  # Umbral de aprobación
            self.base_usuarios[self.usuario_actual]['nivel'] += 1
            self.guardar_usuarios()
            self.hablar(f"¡Felicidades! Ha avanzado al nivel {self.base_usuarios[self.usuario_actual]['nivel']}.")
        else:
            self.hablar("Debe repasar este nivel antes de avanzar. Necesita al menos un 70% de aciertos.")
    
    def iniciar_modulo_aprendizaje(self):
        """Iniciar el módulo de aprendizaje guiado"""
        if not self.usuario_actual:
            self.hablar("Primero debe registrarse o seleccionar un usuario.")
            return
            
        self.hablar("Iniciando módulo de aprendizaje.")
        self.iniciar_nivel()
    
    def iniciar_modulo_practica(self):
        """Iniciar el módulo de práctica"""
        self.hablar("Iniciando módulo de práctica.")
        self.hablar("Se ha reiniciado el tablero. Puede jugar libremente y practicar movimientos.")
        self.board = chess.Board()  # Reiniciar tablero
        self.describir_tablero()
    
    def consultar_progreso(self):
        """Consultar el progreso del usuario actual"""
        if not self.usuario_actual:
            self.hablar("Primero debe registrarse o seleccionar un usuario.")
            return
            
        usuario = self.base_usuarios[self.usuario_actual]
        nivel = usuario['nivel']
        lecciones = len(usuario['lecciones_completadas'])
        ejercicios = len(usuario['ejercicios_completados'])
        
        self.hablar(f"Usuario: {self.usuario_actual}")
        self.hablar(f"Nivel actual: {nivel} - {self.niveles.get(nivel, 'Desconocido')}")
        self.hablar(f"Lecciones completadas: {lecciones}")
        self.hablar(f"Ejercicios completados: {ejercicios}")
        
        # Estimar progreso general
        # Asumimos que hay 12 niveles, con aproximadamente 3-7 lecciones cada uno
        total_niveles = len(self.niveles)
        progreso = ((nivel - 1) / total_niveles) * 100
        self.hablar(f"Progreso general estimado: {progreso:.1f}%")
    
    def reiniciar_tablero(self):
        """Reiniciar el tablero a la posición inicial"""
        self.board = chess.Board()
        self.hablar("Tablero reiniciado a la posición inicial.")
        self.describir_tablero()
    
    def ejecutar(self):
        """Función principal para ejecutar el programa"""
        self.hablar("Bienvenido a Ajedrez Accesible, un programa para aprender y practicar ajedrez mediante comandos de voz.")
        
        # Preguntar si ya tiene usuario
        self.hablar("¿Ya tiene un usuario registrado? Diga 'sí' o 'no'.")
        respuesta = self.escuchar()
        
        if respuesta:
            if "sí" in respuesta.lower() or "si" in respuesta.lower():
                self.cambiar_usuario()
            else:
                self.registrar_usuario()
        
        self.hablar("Para ver los comandos disponibles, diga 'ayuda' en cualquier momento.")
        
        while True:
            comando = self.escuchar()
            
            if not comando:
                continue
                
            comando = comando.lower()
            
            # Procesar comando
            if "salir" in comando:
                self.hablar("Gracias por usar Ajedrez Accesible. ¡Hasta pronto!")
                break
                
            elif "ayuda" in comando:
                self.listar_comandos()
                
            elif "niveles" in comando:
                self.listar_niveles()
                
            elif "nivel actual" in comando:
                if self.usuario_actual:
                    nivel = self.base_usuarios[self.usuario_actual]['nivel']
                    self.hablar(f"Su nivel actual es {nivel}: {self.niveles.get(nivel, 'Desconocido')}")
                else:
                    self.hablar("Primero debe registrarse o seleccionar un usuario.")
                
            elif "iniciar nivel" in comando:
                self.iniciar_nivel()
                
            elif "repetir" in comando:
                self.hablar(self.ultimo_mensaje)
                
            elif "aprender" in comando:
                self.iniciar_modulo_aprendizaje()
                
            elif "practicar" in comando:
                self.iniciar_modulo_practica()
                
            elif "evaluar" in comando:
                self.evaluar_nivel()
                
            elif "estado tablero" in comando:
                self.describir_tablero()
                
            elif "mover" in comando:
                self.procesar_movimiento_voz(comando)
                
            elif "letra" in comando:
                # Extraer la letra mencionada
                palabras = comando.split()
                for palabra in palabras:
                    if len(palabra) == 1 and palabra.lower() in "abcdefgh":
                        self.explicar_notacion(palabra)
                        break
                else:
                    self.hablar("No se encontró una letra válida en el comando.")
                
            elif "posición" in comando or "posicion" in comando:
                # Extraer la posición mencionada
                palabras = comando.split()
                for i, palabra in enumerate(palabras):
                    if i < len(palabras) - 1:
                        posible_posicion = palabra + palabras[i+1]
                        if len(posible_posicion) == 2 and posible_posicion[0].lower() in "abcdefgh" and posible_posicion[1] in "12345678":
                            self.explicar_posicion(posible_posicion)
                            break
                    if len(palabra) == 2 and palabra[0].lower() in "abcdefgh" and palabra[1] in "12345678":
                        self.explicar_posicion(palabra)
                        break
                else:
                    self.hablar("No se encontró una posición válida en el comando.")
                
            elif "reiniciar tablero" in comando:
                self.reiniciar_tablero()
                
            elif "último movimiento" in comando or "ultimo movimiento" in comando:
                self.repetir_ultimo_movimiento()
                
            elif "registrar usuario" in comando:
                self.registrar_usuario()
                
            elif "cambiar usuario" in comando:
                self.cambiar_usuario()
                
            elif "progreso" in comando:
                self.consultar_progreso()
                
            else:
                # Buscar comando similar
                similar = self.comando_mas_similar(comando)
                if similar:
                    self.hablar(f"Comando no reconocido. ¿Quiso decir '{similar}'?")
                else:
                    self.hablar("Comando no reconocido. Diga 'ayuda' para ver los comandos disponibles.")

if __name__ == "__main__":
    app = AjedrezAccesible()
    app.ejecutar()