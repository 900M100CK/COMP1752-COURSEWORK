import tkinter as tk
from tkinter import ttk



class TopPanel:
    def __init__(self, parent, on_music_click, on_add_click):
        # Main frame with padding
        self.top_frame = ttk.Frame(parent, padding=[10, 10, 10, 10])
        self.top_frame.grid(row=0, column=0, sticky="nw")
        
        # Configure grid weights
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Create a style for modern buttons
        style = ttk.Style()
        style.configure('Modern.TButton', 
                       padding=6,
                       font=('Segoe UI', 10))

        # Buttons frame with a subtle background
        self.button_frame = ttk.Frame(self.top_frame)
        self.button_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Music button with icon
        self.music_btn = ttk.Button(
            self.button_frame,
            text="🎵 Music",
            command=on_music_click,
            style='Modern.TButton',
            width=15
        )
        self.music_btn.grid(row=0, column=0, padx=(0, 10))

        # Add button with icon
        self.add_btn = ttk.Button(
            self.button_frame,
            text="➕ Add New Song",
            command=on_add_click,
            style='Modern.TButton',
            width=16
        )
        self.add_btn.grid(row=0, column=1)




