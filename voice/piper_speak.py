import subprocess
import os
import tempfile
import platform


class PiperSpeaker:
    def __init__(self, model_path="en_US-lessac-medium.onnx", config_path="en_US-lessac-medium.onnx.json"):
        self.model_path = model_path
        self.config_path = config_path
        self.piper_available = self._check_piper()
    
    def _check_piper(self):
        """Check if piper is installed."""
        try:
            result = subprocess.run(['piper', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            return result.returncode == 0
        except:
            return False
    
    def speak(self, text):
        """Speak text using Piper TTS."""
        if not text:
            return
        
        if not self.piper_available:
            print(f"[TTS] Piper not found. Would say: {text}")
            return
        
        # Check if model files exist
        if not os.path.exists(self.model_path):
            print(f"[TTS] Model not found at {self.model_path}. Would say: {text}")
            return
        
        try:
            # Create temp wav file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_wav = f.name
            
            # Generate speech with piper
            cmd = [
                'piper',
                '--model', self.model_path,
                '--config', self.config_path,
                '--output_file', temp_wav
            ]
            
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            
            # Play the audio
            self._play_audio(temp_wav)
            
            # Clean up
            try:
                os.unlink(temp_wav)
            except:
                pass
                
        except Exception as e:
            print(f"[TTS] Error speaking: {e}")
            print(f"Would say: {text}")
    
    def _play_audio(self, wav_file):
        """Play audio file."""
        system = platform.system()
        try:
            if system == 'Windows':
                import winsound
                winsound.PlaySound(wav_file, winsound.SND_FILENAME)
            elif system == 'Darwin':  # macOS
                subprocess.run(['afplay', wav_file], timeout=30)
            else:  # Linux
                subprocess.run(['aplay', wav_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        except Exception as e:
            print(f"[Audio] Could not play audio: {e}")
            # Fallback to just printing
            pass
