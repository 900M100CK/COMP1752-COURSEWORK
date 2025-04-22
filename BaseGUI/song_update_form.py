import tkinter as tk
from tkinter import ttk, messagebox
from Access import SongAccess
from Model import SongItem

class SongUpdateForm(ttk.Frame):
    """
    Form for updating song details.
    Allows users to modify song information and save changes.
    """
    def __init__(self, parent, playlist_panel=None, table_frame=None):
        super().__init__(parent)
        self.parent_widget = parent  # Store parent reference
        self.playlist_panel = playlist_panel
        self.table_frame = table_frame  # Store table frame reference
        self.song_access = SongAccess()
        self.current_song_id = None
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface components"""
        # Configure grid layout
        self.columnconfigure(1, weight=1)
        
        # Create form fields
        self._setup_title_field()
        self._setup_artist_field()
        self._setup_album_field()
        self._setup_rating_field()
        self._setup_buttons()

    def _setup_title_field(self):
        """Set up the title input field"""
        # Create label
        ttk.Label(self, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        # Create entry
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self, textvariable=self.title_var, state="disabled")
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def _setup_artist_field(self):
        """Set up the artist input field"""
        # Create label
        ttk.Label(self, text="Artist:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        # Create entry
        self.artist_var = tk.StringVar()
        self.artist_entry = ttk.Entry(self, textvariable=self.artist_var, state="disabled")
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def _setup_album_field(self):
        """Set up the album input field"""
        # Create label
        ttk.Label(self, text="Album:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        # Create entry
        self.album_var = tk.StringVar()
        self.album_entry = ttk.Entry(self, textvariable=self.album_var, state="disabled")
        self.album_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def _setup_rating_field(self):
        """Set up the rating input field"""
        # Create label
        ttk.Label(self, text="Rating:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        # Create combobox
        self.rating_var = tk.StringVar()
        self.rating_combo = ttk.Combobox(
            self,
            textvariable=self.rating_var,
            values=[(i * "⭐"+(5-i)*" ☆")  for i in range((0), 6)],
            state="readonly"
        )
        self.rating_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    def _setup_buttons(self):
        """Set up the action buttons"""
        # Create button frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Create update button
        self.update_btn = ttk.Button(
            button_frame,
            text="Update",
            command=self._on_update
        )
        self.update_btn.grid(row=0, column=0, padx=5)
        
        # Create clear button
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self._on_clear
        )
        self.clear_btn.grid(row=0, column=1, padx=5)

    def load_song(self, song_id, title, artist, album, rating):
        """
        Load song details into the form
        
        Args:
            song_id: ID of the song
            title: Song title
            artist: Song artist
            album: Song album
            rating: Song rating
        """
        # Store current song ID
        self.current_song_id = song_id
        
        # Set form values
        self.title_var.set(title)
        self.artist_var.set(artist)
        self.album_var.set(album)
        self.rating_var.set(str(rating))

    def _on_update(self):
        """Handle update button click"""
        # Validate form
        if not self._validate_form():
            return
        if not self.load_song:
            return

        try:
            # Get form values
            title = self.title_var.get().strip()
            artist = self.artist_var.get().strip()
            album = self.album_var.get().strip()
            rating = int(self.rating_var.get())

            # Validate artist name
            if not artist or len(artist) > 100:  # Assuming a reasonable max length
                messagebox.showerror("Validation Error", "Artist name is required and must be less than 100 characters")
                return

            # Create updated song object with the right parameter order
            updated_song = SongItem(
                song_id=self.current_song_id,
                media_id=self.current_song_id,
                title=title,
                artist=artist,
                rating=rating,
                album=album,
                count_play=0
            )

            # Update song in database
            success = self.song_access.update_song(self.current_song_id, title, artist, album, rating)
            if success:
                messagebox.showinfo("Success", "Song updated successfully. All tables will be refreshed.")
                
                # Store current song ID before clearing the form
                song_id = self.current_song_id
                
                # Clear the form
                self._on_clear()

                # Refresh all tables and views to reflect the changes
                self._refresh_all_views()
            else:
                messagebox.showerror("Error", "Failed to update song. Please check the database connection.")
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Invalid rating value: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the song:\n{str(e)}")

    def _refresh_all_views(self):
        """Refresh all related views to reflect changes"""
        # Use the new comprehensive refresh method if available
        if self.table_frame and hasattr(self.table_frame, 'refresh_all_tables'):
            self.table_frame.refresh_all_tables(self.current_song_id)
            return
            
        # Fallback to existing refresh methods if comprehensive method is not available
        # Direct refresh of table frame if available
        if self.table_frame and hasattr(self.table_frame, 'refresh_table'):
            try:
                self.table_frame.refresh_table()
                print("Directly refreshed table frame")
            except Exception as e:
                print(f"Error refreshing table frame: {e}")
        
        # Refresh the parent widget (song table)
        if hasattr(self.parent_widget, 'refresh_table'):
            self.parent_widget.refresh_table()
        
        # Try additional refresh methods that might exist
        for method_name in ['refresh', 'update_display', 'load_data', 'reload']:
            if hasattr(self.parent_widget, method_name):
                try:
                    getattr(self.parent_widget, method_name)()
                    print(f"Called {method_name} on parent widget")
                except Exception as e:
                    print(f"Error calling {method_name}: {e}")
        
        # Refresh playlist panel if provided
        if self.playlist_panel:
            if hasattr(self.playlist_panel, 'refresh_playlist_table'):
                try:
                    self.playlist_panel.refresh_playlist_table()
                    print("Refreshed playlist table")
                except Exception as e:
                    print(f"Error refreshing playlist table: {e}")
            else:
                # Try multiple possible refresh methods
                for method_name in ['load_songs', 'refresh', 'update', 'reload']:
                    if hasattr(self.playlist_panel, method_name):
                        try:
                            getattr(self.playlist_panel, method_name)()
                            print(f"Called {method_name} on playlist panel")
                        except Exception as e:
                            print(f"Error calling {method_name} on playlist: {e}")

    def _on_clear(self):
        """Handle clear button click"""
        # Clear form fields
        self.current_song_id = None
        self.title_var.set("")
        self.artist_var.set("")
        self.album_var.set("")
        self.rating_var.set("")
        self.title_entry.state(["disabled"])
        self.artist_entry.state(["disabled"])
        self.album_entry.state(["disabled"])
        self.rating_combo.state(["disabled"])

    def _validate_form(self):
        """
        Validate form input
        
        Returns:
            bool: True if form is valid, False otherwise
        """
        # Check required fields
        if not self.title_var.get().strip():
            messagebox.showwarning("Validation Error", "Title is required")
            return False
            
        if not self.artist_var.get().strip():
            messagebox.showwarning("Validation Error", "Artist is required")
            return False
            
        if not self.album_var.get().strip():
            messagebox.showwarning("Validation Error", "Album is required")
            return False
            
        if not self.rating_var.get():
            messagebox.showwarning("Validation Error", "Rating is required")
            return False

        return True

    def set_table_frame(self, table_frame):
        """
        Set the reference to the table frame for direct updates
        
        Args:
            table_frame: Reference to the main table frame
        """
        self.table_frame = table_frame

