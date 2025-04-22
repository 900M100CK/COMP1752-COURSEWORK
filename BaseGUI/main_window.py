import tkinter as tk
from tkinter import ttk
from config_database import API_KEY
from BaseGUI import RightFrame
from BaseGUI import PlaylistPanel



class BaseWindow:
    """
    Main window class for the Jukebox application.
    Handles the main application window, layout, and view management.
    """
    def __init__(self):
        """Initialize the main window and its components"""
        # Create the main window
        self.window = tk.Tk()
        # API key for Deezer service
        self.api_key = API_KEY

        # Configure styles and setup layout
        self._configure_styles()
        self._setup_layout()
        self._setup_components()

        # Configure window properties and show default view
        self.configure_window("Media Player")
        self.window.mainloop()

    def _configure_styles(self):
        """Configure the visual styles for the application"""
        # Create a style object
        style = ttk.Style()
        # Configure modern button style with custom font and padding
        style.configure('Modern.TButton', font=('Segoe UI', 10), padding=6)
        # Configure frame styles
        style.configure('MainFrame.TFrame', borderwidth=1, relief='solid')
        style.configure('Heading.TLabel', font=('Segoe UI', 11, 'bold'))


    def _setup_layout(self):
        """Set up the main window layout with proper grid configuration"""
     # Configure grid weights for responsive layout
        self.window.rowconfigure(0, weight=1)  # Main content row (expands)
        self.window.columnconfigure(0, weight=1)  # Single column (expands)

        # Configure window background
        self.window.configure(bg='#f0f0f0')


    def _setup_components(self):
        """Initialize and set up all UI components"""
        # Create main content frame with fixed size and padding
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure content frame grid weights
        # Configure content frame grid weights for balanced layout
        self.content_frame.columnconfigure(0, weight=3, minsize=900)  # Left (song table) - reduced width
        self.content_frame.columnconfigure(1, weight=0)  # Separator column
        self.content_frame.columnconfigure(2, weight=2, minsize=400)  # Right (playlist panel) - increased width
        self.content_frame.rowconfigure(0, weight=0)  # Title row
        self.content_frame.rowconfigure(1, weight=1)  # Content row
        
        # Add section titles
        ttk.Label(self.content_frame, text="Music Library", style='Heading.TLabel').grid(
            row=0, column=0, sticky="w", padx=5, pady=(0, 5))
        ttk.Label(self.content_frame, text="Playlists", style='Heading.TLabel').grid(
            row=0, column=2, sticky="w", padx=5, pady=(0, 5))
        
        # Create playlist panel frame with fixed size
        self.playlist_frame = ttk.Frame(self.content_frame, style='MainFrame.TFrame')
        self.playlist_frame.grid(row=1, column=2, sticky="nsew", padx=(10, 0), pady=(0, 10))
        self.playlist_frame.columnconfigure(0, weight=1)
        self.playlist_frame.rowconfigure(0, weight=1)
        
        # Create playlist panel with API key
        self.playlist_panel = PlaylistPanel(self.playlist_frame, self.api_key)
        self.playlist_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create song table frame with fixed size
        self.song_table_frame = ttk.Frame(self.content_frame, style='MainFrame.TFrame')
        self.song_table_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        self.song_table_frame.columnconfigure(0, weight=1)
        self.song_table_frame.rowconfigure(0, weight=1)
        
        # Create RightFrame component with playlist panel reference and API key
        self.right_frame = RightFrame(self.song_table_frame, self.playlist_panel, self.api_key)
        self.right_frame.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add vertical separator
        separator = ttk.Separator(self.content_frame, orient="vertical")
        separator.grid(row=1, column=1, sticky="ns")
        
        # Configure minimum window size
        self.window.minsize(1200, 768)  # Set minimum window size
        
        # Configure window resize behavior
        self.window.bind('<Configure>', self._on_window_resize)

    def _on_window_resize(self, event):
        """Handle window resize events"""
        # Update content frame size based on window size
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Calculate new sizes for components with 3:2 ratio
        # Accounting for separator and padding
        separator_width = 2
        padding_width = 40  # Total padding (left + right + between columns)
        usable_width = width - separator_width - padding_width
        
        table_width = max(900, int(usable_width * 0.70))  # Table takes 60% of usable width
        playlist_width = max(400, usable_width - table_width)  # Playlist takes remaining width
        
        # Update column weights
        self.content_frame.columnconfigure(0, weight=3, minsize=table_width)  # 60% weight
        self.content_frame.columnconfigure(1, weight=0)  # Separator column (no weight)
        self.content_frame.columnconfigure(2, weight=2, minsize=playlist_width)  # 40% weight

    def configure_window(self, title):
        """
        Configure the main window properties
        
        Args:
            title (str): Window title
        """
        # Set window title
        self.window.title(title)
        try:
            # Try to set window icon
            self.window.iconbitmap("Icon/media_player.ico")
        except:
            pass
        # Maximize the window
        self.window.state('zoomed')

