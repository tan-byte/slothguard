import ctypes
import sys

def show_message_box(title, message, timeout_ms=8000):
    try:
        # MB_OK | MB_TOPMOST | MB_ICONINFORMATION
        ctypes.windll.user32.MessageBoxTimeoutW(None, message, title, 0x40 | 0x40000, 0, timeout_ms)
    except Exception as e:
        print(f"Error showing message box: {e}")
        print(f"{title}: {message}")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        show_message_box(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8000)
    elif len(sys.argv) == 2:
        show_message_box("SlothGuard", sys.argv[1], 8000)
