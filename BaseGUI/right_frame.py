import tkinter as tk
from tkinter import ttk, messagebox

from BaseGUI import SongTable
from BaseGUI import SongSearchPanel
from BaseGUI import TopPanel
# from BaseGUI import SongUpdateForm
# from BaseGUI import SongDetailsPanel
from Access import PlaylistAccess
from config_database import API_KEY


class RightFrame:
    """
    Main frame component for displaying and managing songs.
    Handles switching between song table and search panel.
    """
    def __init__(self, window, playlist_panel=None, api_key=None):
        """
        Initialize the right frame component
        
        Args:
            window: Parent window
            playlist_panel: Reference to playlist panel for updates
            api_key: API key for Deezer service
        """
        # Store window reference
        self.window = window
        # Reference to current table being displayed
        self.current_table = None
        # API key for external services
        self.api_key = api_key if api_key else API_KEY
        # Reference to playlist panel for updates
        self.playlist_panel = playlist_panel
        # Setup UI components
        self._setup_layout()
        self._setup_components()
        self.click_music_btn()

    def _setup_layout(self):
        """Configure the main layout grid"""
        # Configure window grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Create and configure main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)  # Top panel row
        self.main_frame.rowconfigure(1, weight=1)  # Content row

    def _setup_components(self):
        """Initialize all UI components"""
        # Setup all UI components in order
        self._setup_top_panel()
        self._setup_content_frame()

    def _setup_top_panel(self):
        """Set up the top panel with navigation buttons"""
        # Create top panel with music and add buttons
        self.top_panel = TopPanel(self.main_frame, self.click_music_btn, self.click_add_btn)
        self.top_panel.top_frame.grid(row=0, column=0, sticky="ew")

    def _setup_content_frame(self):
        """Set up the content frame that holds the active panel"""
        # Create content frame for table or search panel
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

    def show_table(self, table_class, api_key=None):
        """
        Display a specific table type (songs or search results)
        
        Args:
            table_class: Class of table to display
            api_key: API key for external services
        """
        # Clear current table
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Clear and recreate status label
        if hasattr(self, 'status_lbl'):
            self.status_lbl.destroy()
        self.status_lbl = ttk.Label(self.main_frame, text="Ready", anchor=tk.W)
        self.status_lbl.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Create new table instance with appropriate parameters
        if table_class == SongTable:
            # Use API key from the class
            self.current_table = table_class(self.content_frame, self.playlist_panel, self.api_key)
        else:
            # Use provided API key for search panel
            api_key_to_use = api_key if api_key else self.api_key
            self.current_table = table_class(self.content_frame, api_key_to_use)
            
        # Setup UI and load data
        self.current_table.setup_ui()
        self.current_table.load_data()

        # Reference the status label if it's needed
        if hasattr(self.current_table, 'status_lbl'):
            self.current_table.status_lbl = self.status_lbl

    def click_music_btn(self):
        """Handle click on the music button"""
        # Show song table
        self.show_table(SongTable)
        self.status_lbl.configure(text="Showing music library")

    def click_add_btn(self):
        """Handle click on the add button"""
        # Show search panel
        self.show_table(SongSearchPanel, api_key=self.api_key)
        self.status_lbl.configure(text="Add new song to library")

    def refresh_table(self):
        """Refresh the current table data"""
        # Show the song table
        self.show_table(SongTable)
        # Refresh the table data
        if self.current_table:
            self.current_table.load_data()
            self.status_lbl.configure(text="Table refreshed")

    def refresh_all_tables(self):
        """
        Comprehensive method to refresh all tables in the application
        """
        # First refresh the main song table
        self.refresh_table()
        
        # Then refresh the playlist panel if available
        if self.playlist_panel and hasattr(self.playlist_panel, 'refresh_playlist_table'):
            self.playlist_panel.refresh_playlist_table()
            
        # Log the refresh operation
        self.status_lbl.configure(text="All tables refreshed")





