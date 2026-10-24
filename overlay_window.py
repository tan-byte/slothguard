import tkinter as tk
import sys

def main():
    if len(sys.argv) < 2:
        return
    tip_text = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    
    root = tk.Tk()
    root.title("SlothGuard")
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.attributes('-alpha', 0.95)
    root.configure(bg='#1e272e')
    
    # Make it appear on top of everything
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', True)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    main_frame = tk.Frame(root, bg='#1e272e', padx=40, pady=25, highlightbackground='#00b894', highlightthickness=2)
    main_frame.pack()
    
    mascot_label = tk.Label(
        main_frame, 
        text="SLOTHGUARD", 
        font=('Arial', 16, 'bold'),
        bg='#1e272e',
        fg='#00b894'
    )
    mascot_label.pack(pady=(0, 12))
    
    tip_label = tk.Label(
        main_frame,
        text=tip_text,
        font=('Arial', 12),
        bg='#1e272e',
        fg='#ffffff',
        wraplength=450,
        justify='center'
    )
    tip_label.pack()
    
    hint_label = tk.Label(
        main_frame,
        text="(click to dismiss)",
        font=('Arial', 8),
        bg='#1e272e',
        fg='#808e9b'
    )
    hint_label.pack(pady=(10, 0))
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (screen_width // 2) - (width // 2)
    y = screen_height - height - 80
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.after(duration * 1000, root.destroy)
    root.bind('<Button-1>', lambda e: root.destroy())
    root.bind('<Escape>', lambda e: root.destroy())
    
    root.mainloop()

if __name__ == '__main__':
    main()
