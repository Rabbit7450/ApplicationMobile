from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import os

class MicrophoneManager:
    def __init__(self):
        self.has_permission = False
        self.is_recording = False
        self.audio_file = None
        self.setup_permissions()

    def setup_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.RECORD_AUDIO,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            self.has_permission = True
        elif platform == 'ios':
            # En iOS, los permisos se manejan a través del archivo Info.plist
            self.has_permission = True
        else:
            # En otras plataformas, asumimos que tenemos permiso
            self.has_permission = True

    def start_recording(self, callback=None):
        if not self.has_permission:
            print("No hay permiso para acceder al micrófono")
            return False

        if platform == 'android':
            from jnius import autoclass
            MediaRecorder = autoclass('android.media.MediaRecorder')
            AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
            OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
            AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
            
            # Crear directorio para el archivo de audio si no existe
            audio_dir = os.path.join(os.path.expanduser('~'), 'audio')
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)
            
            self.audio_file = os.path.join(audio_dir, 'recording.mp3')
            
            try:
                self.recorder = MediaRecorder()
                self.recorder.setAudioSource(AudioSource.MIC)
                self.recorder.setOutputFormat(OutputFormat.MPEG_4)
                self.recorder.setAudioEncoder(AudioEncoder.AAC)
                self.recorder.setOutputFile(self.audio_file)
                self.recorder.prepare()
                self.recorder.start()
                self.is_recording = True
                
                if callback:
                    Clock.schedule_once(lambda dt: callback(True))
                return True
            except Exception as e:
                print(f"Error al iniciar la grabación: {str(e)}")
                return False
        else:
            print("La grabación de audio solo está soportada en Android")
            return False

    def stop_recording(self, callback=None):
        if not self.is_recording:
            return False

        if platform == 'android':
            try:
                self.recorder.stop()
                self.recorder.release()
                self.is_recording = False
                
                if callback:
                    Clock.schedule_once(lambda dt: callback(self.audio_file))
                return True
            except Exception as e:
                print(f"Error al detener la grabación: {str(e)}")
                return False
        return False

    def play_recording(self):
        if self.audio_file and os.path.exists(self.audio_file):
            sound = SoundLoader.load(self.audio_file)
            if sound:
                sound.play()
                return True
        return False 