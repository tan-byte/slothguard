import subprocess
import sys
import os


def show_tip_overlay(tip_text, duration=8):
    """Show tip overlay in a separate process."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Try Windows Forms MessageBox via PowerShell - most reliable on Windows
    try:
        ps_cmd = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{tip_text}", "SlothGuard")'
        if sys.platform == 'win32':
            subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd], 
                            creationflags=0)
            return
    except Exception as e:
        pass
    
    # Try tkinter overlay
    try:
        overlay_script = os.path.join(script_dir, 'overlay_window.py')
        subprocess.Popen([sys.executable, overlay_script, tip_text, str(duration)], 
                        creationflags=0)
        return
    except Exception as e:
        pass
    
    print(f"\n{'='*60}")
    print(f"*** SLOTHGUARD TIP ***")
    print(f"{tip_text}")
    print(f"{'='*60}\n")
