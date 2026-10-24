import time
import numpy as np
from skimage.metrics import structural_similarity as ssim


class StagnationDetector:
    def __init__(self, threshold_seconds=90, ssim_threshold=0.98):
        self.threshold_seconds = threshold_seconds
        self.ssim_threshold = ssim_threshold
        self.last_frame = None
        self.last_change_time = time.time()
        self.last_intervention_time = 0
    
    def update(self, current_frame):
        """
        Update with current frame. Returns True if stuck and should intervene.
        """
        current_time = time.time()
        
        if self.last_frame is None:
            self.last_frame = current_frame
            self.last_change_time = current_time
            return False
        
        # Convert to grayscale for SSIM comparison
        if len(current_frame.shape) == 3:
            # Convert RGB to grayscale
            current_gray = np.dot(current_frame[..., :3], [0.299, 0.587, 0.114])
        else:
            current_gray = current_frame
        
        if len(self.last_frame.shape) == 3:
            last_gray = np.dot(self.last_frame[..., :3], [0.299, 0.587, 0.114])
        else:
            last_gray = self.last_frame
        
        # Calculate SSIM
        try:
            similarity = ssim(current_gray, last_gray, data_range=current_gray.max() - current_gray.min() if (current_gray.max() - current_gray.min()) > 0 else 1)
        except:
            similarity = 0.0
        
        if similarity < self.ssim_threshold:
            # Screen changed
            self.last_change_time = current_time
            self.last_frame = current_frame.copy()
            return False
        else:
            # Screen is similar - check if stuck long enough
            time_stuck = current_time - self.last_change_time
            if time_stuck >= self.threshold_seconds:
                # Check cooldown
                if current_time - self.last_intervention_time > 300:  # 5 min cooldown minimum
                    return True
        
        self.last_frame = current_frame.copy()
        return False
    
    def record_intervention(self):
        """Record that an intervention was made."""
        self.last_intervention_time = time.time()
        self.last_change_time = time.time()  # Reset so we don't intervene again immediately
