#!/usr/bin/env python3
import time
import random
import yaml
import os
import sys
from pathlib import Path

from capture.screen import ScreenCapture
from detectors.stagnation import StagnationDetector
from brain.ollama_client import OllamaClient
from voice.piper_speak import PiperSpeaker

try:
    from overlay import show_tip_overlay
    OVERLAY_AVAILABLE = True
except Exception as e:
    print(f"Overlay not available: {e}")
    OVERLAY_AVAILABLE = False


class SlothMascot:
    """Simple calming mascot display."""
    def __init__(self, enabled=True):
        self.enabled = enabled
    
    def show_tip(self, tip):
        if not self.enabled:
            return
        print("\n" + "="*50)
        print("  SLOTHGUARD")
        print("="*50)
        print(f"\n  {tip}\n")
        print("="*50 + "\n")
        # Also show on-screen overlay
        if OVERLAY_AVAILABLE:
            try:
                show_tip_overlay(tip, duration=8)
            except Exception as e:
                print(f"Failed to show overlay: {e}")


def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    print("[SLOTH] SlothGuard Starting...")
    
    # Load config
    config_path = Path(__file__).parent / "config.yaml"
    config = load_config(config_path)
    
    # Initialize components
    capture = ScreenCapture(downscale_factor=config['capture'].get('downscale_factor', 4))
    detector = StagnationDetector(
        threshold_seconds=config['stagnation']['threshold_seconds'],
        ssim_threshold=config['stagnation']['ssim_threshold']
    )
    ollama = OllamaClient(
        base_url=config['ollama']['base_url'],
        model=config['ollama']['model'],
        timeout=config['ollama']['timeout']
    )
    speaker = PiperSpeaker(
        model_path=config['piper']['model_path'],
        config_path=config['piper']['config_path']
    )
    mascot = SlothMascot(enabled=config['intervention']['show_mascot'])
    
    prompt_path = Path(__file__).parent / "prompts" / "intervention.txt"
    
    interval = config['capture']['interval_seconds']
    cooldown_min = config['cooldown']['min_minutes'] * 60
    cooldown_max = config['cooldown']['max_minutes'] * 60
    
    print(f"Monitoring every {interval}s, intervening after {config['stagnation']['threshold_seconds']}s of stagnation")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Capture screen
            frame = capture.to_array()
            
            # Check for stagnation
            if detector.update(frame):
                print(f"\n[{time.strftime('%H:%M:%S')}] Stagnation detected! Generating tip...")
                
                # Capture a fresh screenshot for vision model
                screenshot = capture.capture()
                
                # Generate tip
                tip = ollama.generate_tip(str(prompt_path), screenshot)
                print(f"Tip: {tip}")
                
                # Show mascot
                mascot.show_tip(tip)
                
                # Speak the tip
                speaker.speak(tip)
                
                # Record intervention
                detector.record_intervention()
                
                # Cooldown period
                cooldown = random.uniform(cooldown_min, cooldown_max)
                print(f"Cooling down for {cooldown/60:.1f} minutes...\n")
                time.sleep(cooldown)
            else:
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print("\n\nSlothGuard stopped. Take care!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
