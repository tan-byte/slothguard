import requests
import json
import base64
from io import BytesIO
from PIL import Image


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="moondream", timeout=30):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
    
    def generate_tip(self, prompt_template, screenshot=None):
        """
        Generate a tip using local Ollama model.
        Can use vision model with screenshot or text-only.
        """
        try:
            with open(prompt_template, 'r') as f:
                system_prompt = f.read()
            
            # Try with vision if screenshot provided and model supports it
            if screenshot is not None and 'moondream' in self.model.lower():
                return self._generate_with_vision(system_prompt, screenshot)
            else:
                return self._generate_text(system_prompt)
        except Exception as e:
            print(f"Error generating tip: {e}")
            return "Take a slow breath. Try breaking the problem into a smaller step."
    
    def _generate_with_vision(self, system_prompt, screenshot):
        """Generate using vision model with screenshot."""
        # Resize screenshot to be smaller for faster inference
        img = screenshot.copy()
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=70)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": system_prompt + "\n\nGive just the tip:",
            "images": [img_str],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 40,
            }
        }
        
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        tip = result.get('response', '').strip()
        # Clean up - take first line if multiple
        tip = tip.split('\n')[0].strip('"\'')
        return tip
    
    def _generate_text(self, system_prompt):
        """Generate using text-only model."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": system_prompt + "\n\nSituation: User has been stuck staring at the same screen for a while. Give ONE short, calm tip:",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 40,
            }
        }
        
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        tip = result.get('response', '').strip()
        tip = tip.split('\n')[0].strip('"\'')
        return tip
