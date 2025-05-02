import tkinter as tk
from tkinter import ttk, filedialog
import os

class AudioDropArea(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        
        # Store callback function
        self.callback = callback
        
        # Configure frame appearance
        self.configure(style="DropArea.TFrame")
        
        # Create a custom style for the frame
        style = ttk.Style()
        style.configure("DropArea.TFrame", 
                      background="#2a2a2a")
        
        # Create label
        self.label = ttk.Label(
            self, 
            text="Ses dosyasını buraya sürükleyip bırakın\nveya tıklayarak seçin",
            font=("Arial", 14),
            foreground="#888888",
            background="#2a2a2a",
            anchor="center"
        )
        self.label.pack(expand=True, fill="both")
        
        # Set up drag and drop for macOS
        # Note: Tkinter doesn't have built-in drag and drop on all platforms
        # So we'll make the area clickable as an alternative
        self.label.bind("<Button-1>", self.on_click)
        
        # Add a border
        self.configure(borderwidth=2, relief="groove")
        
    def on_click(self, event):
        """Handle click event to open file dialog"""
        file_path = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[
                ("Ses Dosyaları", "*.mp3 *.wav *.ogg *.flac *.m4a"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            self.callback(file_path)
    
    def set_file_loaded(self, loaded, filename=None):
        """Update appearance when a file is loaded"""
        if loaded:
            # Change appearance for loaded state
            self.configure(style="LoadedDropArea.TFrame")
            style = ttk.Style()
            style.configure("LoadedDropArea.TFrame", 
                          background="#2a3a2a")
            
            # Update label
            if filename:
                self.label.configure(
                    text=f"Yüklendi: {filename}",
                    foreground="#aaffaa",
                    background="#2a3a2a"
                )
        else:
            # Reset to default style
            self.configure(style="DropArea.TFrame")
            self.label.configure(
                text="Ses dosyasını buraya sürükleyip bırakın\nveya tıklayarak seçin",
                foreground="#888888",
                background="#2a2a2a"
            )
