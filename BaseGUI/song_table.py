from Abstraction import BaseTable
from Fetcher import SongFetcher
import tkinter as tk
from tkinter import ttk, messagebox
from song_update_form import SongUpdateForm
from song_details_panel import SongDetailsPanel
from song_field import SongFields
from Access import PlaylistAccess

class SongTable(BaseTable):
    def __init__(self, frame, playlist_panel=None, api_key=None):
        """
        Initialize the song table component
        
        Args:
            frame: Parent frame
            playlist_panel: Reference to playlist panel for updates
            api_key: API key for external services
        """
        # Store the api_key before calling super().__init__ which will call setup_ui
        self.api_key = api_key
        self.playlist_panel_bridge = playlist_panel
        self.playlist_access = PlaylistAccess()
        self.search_frame = None
        
        # Initialize the base class
        super().__init__(frame)
        
    def setup_ui(self):
        """Set up the UI components - this is called from BaseTable"""
        super().setup_ui()
        
        # Setup additional UI components
        self._setup_search_form()
        self._setup_song_details_frame()
        self._setup_update_form()
        self._setup_context_menu()
        
        # Bind events
        self.table.bind('<Double-1>', self.on_double_click)
        self.table.bind('<Button-3>', self.show_context_menu)
        
    def _setup_search_form(self):
        # Set up search frame
        self.search_frame = ttk.Frame(self.frame)
        self.search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        # Search label
        self.search_label = ttk.Label(
            self.search_frame,
            text="Search:",
            font=('Segoe UI', 10)
        )
        self.search_label.grid(row=0, column=0, padx=(0, 5))

        # Search entry with placeholder
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            width=30,
            font=('Segoe UI', 10)
        )
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.insert(0, "Search songs...")
        self.search_entry.bind('<FocusIn>', self._clear_placeholder)
        self.search_entry.bind('<FocusOut>', self._add_placeholder)

        # Search field dropdown
        self.field_dropdown = SongFields(self.search_frame)
        self.field_dropdown.field_dropdown.grid(row=0, column=2, padx=5)

        # Search button
        self.search_btn = ttk.Button(
            self.search_frame,
            text="🔍 Search",
            style='Modern.TButton',
            width=10,
            command= self._on_search
        )
        self.search_btn.grid(row=0, column=3, padx=5)
        # Bind search functionality
        self.search_entry.bind('<Return>', self._on_search)

        # Configure modern style
        style = ttk.Style()
        style.configure('Treeview',
                      font=('Segoe UI', 9),
                      rowheight=25,
                      background='#ffffff',
                      fieldbackground='#ffffff',
                      foreground='#333333')
        style.configure('Treeview.Heading',
                      font=('Segoe UI', 9, 'bold'),
                      background='#f0f0f0',
                      foreground='#333333')
        style.map('Treeview',
                 background=[('selected', '#0078d7')],
                 foreground=[('selected', '#ffffff')])

    def _setup_song_details_frame(self):
        """Set up the frame for song details"""
        # Create frame for song details
        self.details_frame = ttk.LabelFrame(self.frame, text="Song Details")
        self.details_frame.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=(10,0))
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)

        # Set fixed width for details frame
        self.details_frame.configure(width=250)

        # Create song details panel with API key - use self.api_key, not self.API_key
        self.song_details = SongDetailsPanel(self.details_frame, self.api_key)
        self.song_details.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def _setup_update_form(self):
        """Set up the song update form"""
        # Create song update form with playlist panel reference and table frame reference
        self.update_form = SongUpdateForm(
            self.frame,
            self.playlist_panel_bridge,
            self  # Pass self (Table) as the table_frame reference
        )
        self.update_form.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    def _setup_context_menu(self):
        """Set up the right-click context menu"""
        # Create context menu for right-click actions
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Add to Playlist", command=self.add_to_playlist)
    def show_context_menu(self, event):
        """
        Display the context menu on right-click
        
        Args:
            event: Mouse event object
        """
        try:
            # Get clicked item and show menu
            item = self.table.identify_row(event.y)
            if item:
                self.table.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error showing context menu: {e}")
    
    def columns(self):
        return ["Album", "#", "Title", "Artist", "Rating", "Count play"]

    def load_data(self, search_term=None, search_field="title"):
        """
        Load data into the table, optionally with search filtering
        Args:
            search_term (str, optional): Term to search for
            search_field (str, optional): Field to search in ('title', 'artist', 'album', 'all')
        """
        # Clear existing items
        for item in self.table.get_children():
            self.table.delete(item)
            
        song_data = SongFetcher()
        
        if search_term:
            # Use search method
            formatted_results = song_data.search_songs(search_term, search_field)
        else:
            # Load all songs
            formatted_results = song_data.fetch_all_songs()
            
        if formatted_results:
            for song in formatted_results:
                # Store song_id in the 'text' field of the item
                self.table.insert("", "end", 
                                text=song["#"], 
                                values=(song["album"],
                                      song["#"],
                                      song["title"],
                                      song["artist"],
                                      song["rating"],
                                      song["count_play"]))
        else:
            # Insert "No songs found" message with empty values for all columns
            messagebox.showerror("404", "No Songs found")

    def refresh_table(self):
        """Refresh the table data"""
        self.load_data()

    def _clear_placeholder(self, event):
        if self.search_entry.get() == "Search songs...":
            self.search_entry.delete(0, tk.END)

    def _add_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search songs...")

    def get_search_term(self):
        term = self.search_var.get()
        return term if term != "Search songs..." else ""

    def get_search_field(self):
        return self.field_dropdown.get_value_search_field()

    def _on_search(self, event=None):
        # Get search parameters
        search_term = self.get_search_term()
        search_field = self.get_search_field()

        # Perform search or show all songs
        if search_term:
            self.load_data(search_term, search_field)
            self.status_lbl.configure(text=f"Searching for '{search_term}' in {search_field}")
        else:
            self.load_data()
            self.status_lbl.configure(text="Showing all songs")

    def on_double_click(self, event):
        # Get clicked item
        item = self.table.identify_row(event.y)
        if not item:
            return
        # Get item values
        values = self.table.item(item)['values']
        if not values:
            return

        # Extract song details
        song_id = self.table.item(item)['text']
        album = values[0]
        title = values[2]
        artist = values[3]
        rating = values[4]
        self.update_form.title_entry.state(["!disabled"])
        self.update_form.artist_entry.state(["!disabled"])
        self.update_form.album_entry.state(["!disabled"])
        self.update_form.rating_combo.state(["!disabled"])
        # Update song details and form
        self.song_details.update_song(song_id)
        self.update_form.load_song(song_id, title, artist, album, rating)
        
    def add_to_playlist(self):
        """Handle adding selected songs to a playlist"""
        # Get selected songs
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a song to add to playlist")
            return

        # Get available playlists
        playlists = self.playlist_access.get_all_playlists()
        if not playlists:
            messagebox.showinfo("No Playlists", "Please create a playlist first")
            return

        # Create playlist selection dialog
        playlist_dialog = tk.Toplevel(self.frame.winfo_toplevel())
        playlist_dialog.title("Select Playlist")
        playlist_dialog.geometry("300x150")
        playlist_dialog.transient(self.frame.winfo_toplevel())
        playlist_dialog.grab_set()

        # Create playlist dropdown
        playlist_var = tk.StringVar()
        playlist_dropdown = ttk.Combobox(
            playlist_dialog,
            textvariable=playlist_var,
            values=[p.name for p in playlists],
            state="readonly"
        )
        playlist_dropdown.pack(pady=20, padx=20, fill="x")

        def on_ok():
            """Handle OK button click in playlist selection dialog"""
            # Get selected playlist
            playlist_name = playlist_var.get()
            if not playlist_name:
                messagebox.showwarning("No Selection", "Please select a playlist")
                return

            # Find playlist object
            playlist = next((p for p in playlists if p.name == playlist_name), None)
            if not playlist:
                return

            # Add songs to playlist
            success_count = 0
            for item in selected:
                values = self.table.item(item)['values']
                song_id = self.table.item(item)['text']
                if self.playlist_access.add_song_to_playlist(playlist.playlist_id, song_id):
                    success_count += 1
                    self.status_lbl.configure(
                        text=f"Added song to playlist: {playlist.name}")
                else:
                    messagebox.showerror("Error", "Failed to add song to playlist")

            # Show success message and refresh if playlist panel exists
            if success_count > 0:
                messagebox.showinfo("Success",
                                f"Successfully added {success_count} song(s) to playlist: {playlist.name}")
                
                # Update the playlist panel if it exists
                if self.playlist_panel_bridge and hasattr(self.playlist_panel_bridge, 'refresh_playlist_table'):
                    self.playlist_panel_bridge.refresh_playlist_table()
                
            playlist_dialog.destroy()

        # Add OK button
        ttk.Button(playlist_dialog, text="OK", command=on_ok).pack(pady=10)

