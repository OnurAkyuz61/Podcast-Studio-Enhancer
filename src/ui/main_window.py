import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from src.ui.drag_drop_area import AudioDropArea
from src.audio_processing.processor import AudioProcessor

class ProcessingThread(threading.Thread):
    def __init__(self, audio_file, settings, progress_callback, complete_callback, error_callback):
        super().__init__()
        self.audio_file = audio_file
        self.settings = settings
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.error_callback = error_callback
        self.daemon = True  # Thread will exit when main program exits
        
    def run(self):
        try:
            processor = AudioProcessor()
            output_file = processor.process_audio(
                self.audio_file, 
                self.settings,
                progress_callback=self.progress_callback
            )
            self.complete_callback(output_file)
        except Exception as e:
            self.error_callback(str(e))

class MainWindow:
    def __init__(self, root):
        self.root = root
        
        # Initialize variables
        self.audio_file = None
        self.processing_thread = None
        self.file_selected = False  # Track if a file has been selected
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Ses Dosyası Seç", command=self.browse_file)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                    'assets', 'logo', 'podcast-studio-enhencer-logo.png')
            logo_image = Image.open(logo_path)
            # Resize the logo to an appropriate size
            logo_image = logo_image.resize((150, 150), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Create a label for the logo
            logo_label = ttk.Label(main_frame, image=logo_photo, background='#2e2e2e')
            logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Add title
        title_label = ttk.Label(
            main_frame, 
            text="Podcast Studio Enhancer", 
            font=("Arial", 24, "bold"),
            foreground="white"
        )
        title_label.pack(pady=(0, 5))
        
        # Add subtitle
        subtitle_label = ttk.Label(
            main_frame, 
            text="Ses kayıtlarınızı profesyonel stüdyo kalitesine dönüştürün",
            font=("Arial", 12),
            foreground="white"
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Add developer credit
        credit_label = ttk.Label(
            main_frame,
            text="Developed by Onur Akyüz",
            font=("Arial", 10, "italic"),
            foreground="#aaaaaa"
        )
        credit_label.pack(pady=(0, 15))
        
        # Add separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", pady=10)
        
        # Create drag and drop area
        self.drop_area = AudioDropArea(main_frame, self.set_audio_file)
        self.drop_area.pack(fill="x", pady=10, ipady=50)
        
        # Add file info label
        self.file_info_label = ttk.Label(
            main_frame, 
            text="Henüz bir ses dosyası seçilmedi",
            foreground="white"
        )
        self.file_info_label.pack(pady=5)
        
        # Add start button (initially disabled)
        self.start_button = ttk.Button(
            main_frame, 
            text="İyileştirmeyi Başlat",
            command=self.process_audio,
            state="disabled",
            style="TButton"
        )
        self.start_button.pack(pady=10, ipady=10, fill="x")
        
        # Add settings frame
        settings_frame = ttk.LabelFrame(
            main_frame, 
            text="İyileştirme Ayarları",
            padding=10,
            style="TLabelframe"
        )
        settings_frame.pack(fill="x", pady=10)
        
        # Configure label frame style
        style = ttk.Style()
        style.configure("TLabelframe", background="#2e2e2e", foreground="white")
        style.configure("TLabelframe.Label", background="#2e2e2e", foreground="white", font=("Arial", 12, "bold"))
        
        # Add noise reduction settings
        noise_frame = ttk.Frame(settings_frame)
        noise_frame.pack(fill="x", pady=5)
        
        noise_label = ttk.Label(noise_frame, text="Gürültü Azaltma:", foreground="white")
        noise_label.pack(side="left")
        
        self.noise_value_label = ttk.Label(noise_frame, text="50%", foreground="white")
        self.noise_value_label.pack(side="right")
        
        self.noise_slider = ttk.Scale(
            noise_frame, 
            from_=0, 
            to=100, 
            orient="horizontal",
            command=lambda v: self.noise_value_label.config(text=f"{int(float(v))}%")
        )
        self.noise_slider.set(50)
        self.noise_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Add compression settings
        comp_frame = ttk.Frame(settings_frame)
        comp_frame.pack(fill="x", pady=5)
        
        comp_label = ttk.Label(comp_frame, text="Kompresyon:", foreground="white")
        comp_label.pack(side="left")
        
        self.comp_value_label = ttk.Label(comp_frame, text="50%", foreground="white")
        self.comp_value_label.pack(side="right")
        
        self.comp_slider = ttk.Scale(
            comp_frame, 
            from_=0, 
            to=100, 
            orient="horizontal",
            command=lambda v: self.comp_value_label.config(text=f"{int(float(v))}%")
        )
        self.comp_slider.set(50)
        self.comp_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Add EQ preset settings
        eq_frame = ttk.Frame(settings_frame)
        eq_frame.pack(fill="x", pady=5)
        
        eq_label = ttk.Label(eq_frame, text="EQ Önayarı:", foreground="white")
        eq_label.pack(side="left")
        
        self.eq_combo = ttk.Combobox(
            eq_frame,
            values=["Stüdyo", "Doğal", "Sıcak", "Parlak", "Derin", "Özel"],
            width=15,
            state="readonly"
        )
        self.eq_combo.current(0)  # Set default to "Stüdyo"
        self.eq_combo.pack(side="left", padx=10, fill="x", expand=True)
        
        # Progress variable (will be used in popup)
        self.progress_var = tk.IntVar()
        
        # Process button is now the start button defined above
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[
                ("Ses Dosyaları", "*.mp3 *.wav *.ogg *.flac *.m4a"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            self.set_audio_file(file_path)
    
    def set_audio_file(self, file_path):
        if os.path.exists(file_path):  # Verify the file exists
            self.audio_file = file_path
            self.file_selected = True  # Mark that a file has been selected
            file_name = os.path.basename(file_path)
            self.file_info_label.config(text=f"Seçilen dosya: {file_name}")
            self.start_button.config(state="normal")
            self.drop_area.set_file_loaded(True, file_name)
        else:
            messagebox.showerror("Hata", "Seçilen dosya bulunamadı.")
            self.file_selected = False
            self.audio_file = None
            self.file_info_label.config(text="Henüz bir ses dosyası seçilmedi")
            self.start_button.config(state="disabled")
            self.drop_area.set_file_loaded(False)
    
    def process_audio(self):
        # Double check that we have a valid file
        if not self.file_selected or not self.audio_file or not os.path.exists(self.audio_file):
            messagebox.showwarning("Uyarı", "Lütfen önce bir ses dosyası seçin.")
            # Reset file selection state
            self.file_selected = False
            self.audio_file = None
            self.file_info_label.config(text="Henüz bir ses dosyası seçilmedi")
            self.start_button.config(state="disabled")
            self.drop_area.set_file_loaded(False)
            return
        
        # Disable UI elements during processing
        self.start_button.config(state="disabled")
        self.progress_var.set(0)
        
        # Create progress dialog
        self.progress_dialog = tk.Toplevel(self.root)
        self.progress_dialog.title("İşlem Sürüyor")
        self.progress_dialog.geometry("400x150")
        self.progress_dialog.resizable(False, False)
        self.progress_dialog.transient(self.root)  # Set as transient to main window
        self.progress_dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        window_width = 400
        window_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.progress_dialog.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Configure dialog style
        self.progress_dialog.configure(bg="#2e2e2e")
        
        # Add processing message
        message_label = ttk.Label(
            self.progress_dialog,
            text="Ses dosyası işleniyor...",
            font=("Arial", 12, "bold"),
            foreground="white",
            background="#2e2e2e"
        )
        message_label.pack(pady=(20, 10))
        
        # Add file name
        file_name = os.path.basename(self.audio_file)
        file_label = ttk.Label(
            self.progress_dialog,
            text=f"Dosya: {file_name}",
            foreground="#aaaaaa",
            background="#2e2e2e"
        )
        file_label.pack(pady=(0, 10))
        
        # Add progress bar to dialog
        self.progress_bar = ttk.Progressbar(
            self.progress_dialog,
            orient="horizontal",
            length=350,
            mode="determinate",
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=10, padx=25)
        
        # Add percentage label
        self.percentage_label = ttk.Label(
            self.progress_dialog,
            text="0%",
            foreground="white",
            background="#2e2e2e"
        )
        self.percentage_label.pack()
        
        # Get settings
        settings = {
            'noise_reduction': self.noise_slider.get() / 100.0,
            'compression': self.comp_slider.get() / 100.0,
            'eq_preset': self.eq_combo.get()
        }
        
        # Start processing thread
        self.processing_thread = ProcessingThread(
            self.audio_file, 
            settings,
            self.update_progress,
            self.processing_complete,
            self.processing_error
        )
        self.processing_thread.start()
    
    def update_progress(self, value):
        self.progress_var.set(value)
        # Update percentage label
        if hasattr(self, 'percentage_label'):
            self.percentage_label.config(text=f"{value}%")
        self.root.update_idletasks()  # Update UI
    
    def processing_complete(self, output_file):
        self.progress_var.set(100)
        
        # Close progress dialog if it exists
        if hasattr(self, 'progress_dialog') and self.progress_dialog.winfo_exists():
            self.progress_dialog.destroy()
        
        # Re-enable start button
        self.start_button.config(state="normal")
        
        # Create a custom completion dialog
        completion_dialog = tk.Toplevel(self.root)
        completion_dialog.title("İşlem Tamamlandı")
        completion_dialog.geometry("500x250")
        completion_dialog.resizable(False, False)
        completion_dialog.transient(self.root)  # Set as transient to main window
        completion_dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        window_width = 500
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        completion_dialog.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Configure dialog style
        completion_dialog.configure(bg="#2e2e2e")
        
        # Add success message
        success_label = ttk.Label(
            completion_dialog,
            text="İşlem Başarıyla Tamamlandı!",
            font=("Arial", 16, "bold"),
            foreground="#aaffaa",
            background="#2e2e2e"
        )
        success_label.pack(pady=(20, 10))
        
        # Add file info
        file_name = os.path.basename(output_file)
        file_info_label = ttk.Label(
            completion_dialog,
            text=f"Dosya kaydedildi:\n{file_name}",
            font=("Arial", 12),
            foreground="white",
            background="#2e2e2e",
            justify="center"
        )
        file_info_label.pack(pady=(0, 20))
        
        # Add buttons frame
        buttons_frame = ttk.Frame(completion_dialog, style="TFrame")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        # Add open folder button
        open_folder_button = ttk.Button(
            buttons_frame,
            text="Klasörü Aç",
            command=lambda: os.system(f'open -R "{output_file}"') or completion_dialog.destroy()
        )
        open_folder_button.pack(side="left", padx=10, fill="x", expand=True)
        
        # Add close button
        close_button = ttk.Button(
            buttons_frame,
            text="Kapat",
            command=completion_dialog.destroy
        )
        close_button.pack(side="right", padx=10, fill="x", expand=True)
    
    def processing_error(self, error_message):
        # Close progress dialog if it exists
        if hasattr(self, 'progress_dialog') and self.progress_dialog.winfo_exists():
            self.progress_dialog.destroy()
            
        # Re-enable start button
        self.start_button.config(state="normal")
        
        messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu:\n{error_message}")

