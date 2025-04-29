from kivy.utils import platform
from kivy.clock import Clock
from plyer import tts
import os
import json
from datetime import datetime

class TextToAudioConverter:
    def __init__(self):
        self.is_processing = False
        self.current_chapter = 0
        self.total_chapters = 0
        self.setup_converter()

    def setup_converter(self):
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

                # Configurar el directorio para los archivos de audio
                self.audio_dir = os.path.join(self.context.getFilesDir().getAbsolutePath(), 'audiolibros')
                if not os.path.exists(self.audio_dir):
                    os.makedirs(self.audio_dir)

                print("Conversor de texto a audio configurado correctamente")
            except Exception as e:
                print(f"Error al configurar el conversor: {str(e)}")
                self.is_tts_available = False
        else:
            print("Conversor solo disponible en Android")
            self.is_tts_available = False

    def convert_text_to_audio(self, text, output_file, callback=None):
        """
        Convierte texto a audio y lo guarda en un archivo.
        
        Args:
            text: Texto a convertir
            output_file: Nombre del archivo de salida
            callback: Función a llamar cuando termine la conversión
        """
        if not self.is_tts_available:
            print("El conversor no está disponible")
            return False

        try:
            # Dividir el texto en capítulos o secciones
            chapters = self._split_into_chapters(text)
            self.total_chapters = len(chapters)
            self.current_chapter = 0

            # Crear archivo de metadatos
            metadata = {
                'titulo': os.path.splitext(output_file)[0],
                'fecha_creacion': datetime.now().isoformat(),
                'total_capitulos': self.total_chapters,
                'duracion_total': 0,
                'capitulos': []
            }

            # Procesar cada capítulo
            for i, chapter in enumerate(chapters):
                chapter_file = f"{output_file}_capitulo_{i+1}.mp3"
                chapter_path = os.path.join(self.audio_dir, chapter_file)
                
                # Convertir capítulo a audio
                self._convert_chapter(chapter, chapter_path)
                
                # Actualizar metadatos
                chapter_metadata = {
                    'numero': i + 1,
                    'archivo': chapter_file,
                    'duracion': self._get_audio_duration(chapter_path)
                }
                metadata['capitulos'].append(chapter_metadata)
                metadata['duracion_total'] += chapter_metadata['duracion']

                self.current_chapter = i + 1
                if callback:
                    callback(self.current_chapter, self.total_chapters)

            # Guardar metadatos
            metadata_path = os.path.join(self.audio_dir, f"{output_file}_metadata.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)

            return True
        except Exception as e:
            print(f"Error al convertir texto a audio: {str(e)}")
            return False

    def _split_into_chapters(self, text):
        """
        Divide el texto en capítulos o secciones manejables.
        """
        # Aquí puedes implementar la lógica para dividir el texto
        # Por ejemplo, por párrafos, capítulos, etc.
        paragraphs = text.split('\n\n')
        chapters = []
        current_chapter = []
        current_length = 0

        for paragraph in paragraphs:
            if current_length + len(paragraph) > 1000:  # Límite de caracteres por capítulo
                chapters.append('\n'.join(current_chapter))
                current_chapter = [paragraph]
                current_length = len(paragraph)
            else:
                current_chapter.append(paragraph)
                current_length += len(paragraph)

        if current_chapter:
            chapters.append('\n'.join(current_chapter))

        return chapters

    def _convert_chapter(self, text, output_path):
        """
        Convierte un capítulo de texto a audio.
        """
        try:
            # Configurar el motor TTS para la conversión
            tts.speak(text, language='es-ES', rate=1.0)
            
            # Aquí deberías implementar la lógica para guardar el audio
            # Esto dependerá de la API específica de Android que uses
            
            return True
        except Exception as e:
            print(f"Error al convertir capítulo: {str(e)}")
            return False

    def _get_audio_duration(self, audio_path):
        """
        Obtiene la duración de un archivo de audio.
        """
        try:
            # Implementar la lógica para obtener la duración
            # Esto dependerá de la API específica de Android que uses
            return 0
        except:
            return 0

    def get_progress(self):
        """
        Obtiene el progreso actual de la conversión.
        """
        if self.total_chapters == 0:
            return 0
        return (self.current_chapter / self.total_chapters) * 100 