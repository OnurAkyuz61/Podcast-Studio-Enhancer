#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk
from src.ui.main_window import MainWindow

def main():
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Create root window
    root = tk.Tk()
    root.title("Podcast Studio Enhancer")
    
    # Set window size and position
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Configure style for a modern look
    style = ttk.Style()
    style.theme_use('clam')  # Use the 'clam' theme which looks modern
    
    # Configure colors for dark theme
    root.configure(bg='#2e2e2e')
    style.configure('TFrame', background='#2e2e2e')
    style.configure('TButton', background='#3e3e3e', foreground='white')
    style.configure('TLabel', background='#2e2e2e', foreground='white')
    style.configure('TProgressbar', background='#4e4e4e', troughcolor='#2e2e2e')
    
    # Create main window
    app = MainWindow(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
