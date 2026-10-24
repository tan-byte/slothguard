import mss
import mss.tools
from PIL import Image
import numpy as np
import io


class ScreenCapture:
    def __init__(self, downscale_factor=4):
        self.downscale_factor = downscale_factor
        self.sct = mss.mss()
    
    def capture(self):
        """Capture the primary monitor and return as PIL Image."""
        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        return img
    
    def capture_downscaled(self):
        """Capture and downscale for faster comparison."""
        img = self.capture()
        if self.downscale_factor > 1:
            new_size = (img.width // self.downscale_factor, img.height // self.downscale_factor)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        return img
    
    def to_array(self):
        """Capture downscaled as numpy array."""
        img = self.capture_downscaled()
        return np.array(img)
    
    def __del__(self):
        if hasattr(self, 'sct'):
            self.sct.close()
