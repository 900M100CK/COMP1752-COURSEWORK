import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from Access import PlaylistAccess
from Fetcher import SongPlaylistFetcher
from BaseGUI import SongDetailsPanel

class PlaylistPanel(ttk.Frame):
    def __init__(self, parent, api_key, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.playlist_access = PlaylistAccess()
        self.song_playlist_fetcher = SongPlaylistFetcher()
        self.current_playlist = None
        self.sort_state = {}
        self.api_key = api_key
        self.setup_ui()

    def setup_ui(self):
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Configure styles for buttons
        style = ttk.Style()
        style.configure("Refresh.TButton", font=("Segoe UI", 10))

        # Top controls
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        # New playlist button
        ttk.Button(top_frame, text="New Playlist", command=self.create_playlist).grid(row=0, column=0, padx=5)


        # Playlist selector
        self.playlist_var = tk.StringVar()
        self.playlist_dropdown = ttk.Combobox(top_frame, textvariable=self.playlist_var, state="readonly")
        self.playlist_dropdown.grid(row=0, column=1, padx=5, sticky="ew")
        self.playlist_dropdown.bind("<<ComboboxSelected>>", self.on_playlist_select)

        # Play button
        self.play_btn = ttk.Button(top_frame, text="Play", command=self.play_playlist)
        self.play_btn.grid(row=0, column=2, padx=5)
        self.play_btn.state(["disabled"])
        
        # Remove button
        self.remove_btn = ttk.Button(top_frame, text="Remove Selected", command=self.remove_selected_songs)
        self.remove_btn.grid(row=0, column=4, padx=5)
        self.remove_btn.state(["disabled"])

        #Delete button
        ttk.Button(top_frame, text="Delete", command=self.delete_playlist, width=7).grid(row=0, column=5, padx=5)

        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Playlist info
        self.info_frame = ttk.LabelFrame(content_frame, text="Playlist Info")
        self.info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.info_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.info_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.info_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.info_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(self.info_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Save button
        self.save_btn = ttk.Button(self.info_frame, text="Save Changes", command=self.save_playlist)
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Initially disable the entries and save button until a playlist is selected
        self.name_entry.state(["disabled"])
        self.desc_entry.state(["disabled"])
        self.save_btn.state(["disabled"])

        # Songs table
        self.songs_frame = ttk.LabelFrame(content_frame, text="Songs")
        self.songs_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.songs_frame.grid_columnconfigure(0, weight=1)
        self.songs_frame.grid_rowconfigure(0, weight=1)

        # Configure Treeview style
        style = ttk.Style()
        style.configure("Playlist.Treeview", rowheight=25)
        style.configure("Playlist.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        columns =["title", "artist", "album", "rating", "plays"]
        # Create Treeview with all columns
        self.tree = ttk.Treeview(self.songs_frame, style="Playlist.Treeview", 
                                columns=columns,
                                show="headings")
        for col in columns:
            self.tree.heading(col, text=col, anchor="w",command=lambda _col=col: self.sort_column_value(_col, False))
            # Adjust column widths for a more compact layout
            if col == "title":
                self.tree.column(col, width=100, stretch=True)
            elif col == "artist":
                self.tree.column(col, width=80, stretch=True)
            elif col == "album":
                self.tree.column(col, width=80, stretch=True)
            elif col == "rating":
                self.tree.column(col, width=60, stretch=False)
            elif col == "plays":
                self.tree.column(col, width=50, stretch=False)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configure columns


        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.songs_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_song_double_click)

        # Song details panel
        self.details_panel = SongDetailsPanel(self, self.api_key)
        self.details_panel.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Load playlists
        self.load_playlists()

    def load_playlists(self):
        playlists = self.playlist_access.get_all_playlists()
        self.playlist_dropdown["values"] = [p.name for p in playlists]

    def create_playlist(self):
        name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name:
            description = simpledialog.askstring("New Playlist", "Enter playlist description (optional):")
            playlist_id = self.playlist_access.create_playlist(name, description or "")
            if playlist_id:
                self.load_playlists()
                self.playlist_var.set(name)
                self.on_playlist_select(None)

    def on_playlist_select(self, event):
        name = self.playlist_var.get()
        if name:
            playlists = self.playlist_access.get_all_playlists()
            self.current_playlist = next((p for p in playlists if p.name == name), None)
            if self.current_playlist:
                self.name_var.set(self.current_playlist.name)
                self.desc_var.set(self.current_playlist.description)
                # Enable controls
                self.play_btn.state(["!disabled"])
                self.remove_btn.state(["!disabled"])
                self.name_entry.state(["!disabled"])
                self.desc_entry.state(["!disabled"])
                self.save_btn.state(["!disabled"])
                self.load_songs()
            else:
                self.clear_playlist()

    def clear_playlist(self):
        self.current_playlist = None
        self.name_var.set("")
        self.desc_var.set("")
        # Disable controls
        self.play_btn.state(["disabled"])
        self.remove_btn.state(["disabled"])
        self.name_entry.state(["disabled"])
        self.desc_entry.state(["disabled"])
        self.save_btn.state(["disabled"])
        self.tree.delete(*self.tree.get_children())

    def load_songs(self):
        if not self.current_playlist:
            return

        self.tree.delete(*self.tree.get_children())
        # Get all songs in the playlist with their details
        songs = self.song_playlist_fetcher.get_playlist_songs(self.current_playlist.playlist_id)
        
        for song in songs:
            # Insert song with all details
            self.tree.insert("", "end", text=song["song_id"],
                           values=(song["title"],
                                 song["artist"],
                                 song["album"],
                                song["rating"],
                                 song["count_play"]))
        
        # Update playlist info to show play count
        if self.current_playlist:
            self.info_frame.configure(text=f"Playlist Info (Played {self.current_playlist.count_play} times)")
            
        # Force a refresh of the current playlist data
        if self.current_playlist:
            playlists = self.playlist_access.get_all_playlists()
            self.current_playlist = next((p for p in playlists if p.playlist_id == self.current_playlist.playlist_id), None)

    def save_playlist(self):
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "Please select a playlist first")
            return

        # Update playlist details
        self.current_playlist.name = self.name_var.get()
        self.current_playlist.description = self.desc_var.get()

        # Validate input
        if not self.current_playlist.name:
            messagebox.showwarning("Invalid Input", "Playlist name cannot be empty")
            return

        # Save changes
        if self.playlist_access.update_playlist(self.current_playlist):
            messagebox.showinfo("Success", "Playlist updated successfully")
            self.load_playlists()
            # Update the dropdown to show the new name
            self.playlist_var.set(self.current_playlist.name)
        else:
            messagebox.showerror("Error", "Failed to update playlist")

    def play_playlist(self):
        if not self.current_playlist:
            return

        if self.playlist_access.play_playlist(self.current_playlist.playlist_id):
            messagebox.showinfo("Success", "Playlist played successfully")
            # Increment the playlist's play count
            self.current_playlist.count_play += 1
            # Reload songs to show updated play counts
            self.load_songs()
        else:
            messagebox.showerror("Error", "Failed to play playlist")

    def on_song_double_click(self, event):
        """Handle double-click on a song in the table"""
        selected_item = self.tree.selection()
        if selected_item:
            # Get the song_id from the selected item
            song_id = self.tree.item(selected_item[0])['text']
            # Update the details panel with the selected song
            self.details_panel.update_song(song_id)

    def remove_selected_songs(self):
        """Remove selected songs from the current playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "Please select a playlist first")
            return

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select songs to remove")
            return

        # Confirm removal
        if not messagebox.askyesno("Confirm Removal", 
                                 f"Are you sure you want to remove {len(selected_items)} song(s) from the playlist?"):
            return

        # Remove each selected song
        for item in selected_items:
            song_id = self.tree.item(item)['text']
            if self.playlist_access.remove_song_from_playlist(self.current_playlist.playlist_id, song_id):
                self.tree.delete(item)
            else:
                messagebox.showerror("Error", f"Failed to remove song with ID {song_id}")

        # Update the playlist info and refresh the table
        self.load_songs()
        
        # Clear the song details panel text area instead of removing it
        if hasattr(self, 'details_panel'):
            self.details_panel.clear_details()  # This should be a method that only clears the text area

    def delete_playlist(self):
        """Delete the current playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "Please select a playlist first")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                 f"Are you sure you want to delete the playlist '{self.current_playlist.name}'?"):
            return

        # Get playlist ID before deleting
        playlist_id = self.current_playlist.delete()
        
        # Delete the playlist
        if self.playlist_access.delete_playlist(playlist_id):
            messagebox.showinfo("Success", "Playlist deleted successfully")
            # Clear current playlist
            self.clear_playlist()
            # Reload playlists
            self.load_playlists()
            # Refresh the main table if needed
            if hasattr(self.master, 'refresh_after_playlist_delete'):
                self.master.refresh_after_playlist_delete()
            elif hasattr(self.master.master, 'refresh_after_playlist_delete'):
                self.master.master.refresh_after_playlist_delete()
        else:
            messagebox.showerror("Error", "Failed to delete playlist")

    def refresh_all(self):
        """
        Comprehensive refresh method that updates both the playlist list and the current playlist data
        """
        # First refresh the playlists dropdown
        self.load_playlists()
        
        # Check if we have a current playlist
        if self.current_playlist:
            # Remember the current playlist ID
            current_id = self.current_playlist.playlist_id
            
            # Refresh the playlist data
            playlists = self.playlist_access.get_all_playlists()
            self.current_playlist = next((p for p in playlists if p.playlist_id == current_id), None)
            
            if self.current_playlist:
                # If playlist still exists, refresh its table
                self.refresh_playlist_table()
            else:
                # If playlist was deleted, clear the display
                self.clear_playlist()
                messagebox.showinfo("Refresh Complete", "Playlist list has been refreshed. The previously selected playlist is no longer available.")
        else:
            # If no playlist is selected, just show a message
            messagebox.showinfo("Refresh Complete", "Playlist list has been refreshed.")
            
    def refresh_playlist_table(self):
        """Refresh the playlist table to show updated song information"""
        if self.current_playlist:
            # Clear the current table
            self.tree.delete(*self.tree.get_children())
            
            # Get fresh song data from the database
            songs = self.song_playlist_fetcher.get_playlist_songs(self.current_playlist.playlist_id)
            
            # Insert updated songs into the table
            for song in songs:
                self.tree.insert("", "end", text=song["song_id"],
                               values=(song["title"],
                                     song["artist"],
                                     song["album"],
                                     "★" * song["rating"],
                                     song["count_play"]))
            
            # Update playlist info
            self.info_frame.configure(text=f"Playlist Info (Played {self.current_playlist.count_play} times)")
            
            # Force a refresh of the current playlist data
            playlists = self.playlist_access.get_all_playlists()
            self.current_playlist = next((p for p in playlists if p.playlist_id == self.current_playlist.playlist_id), None)
            
            # Update the playlist dropdown
            self.playlist_var.set(self.current_playlist.name if self.current_playlist else "")

    def sort_column_value(self, col, reverse):
        """
        Sorts the table by a given column in ascending or descending order.

        Args:
            col (str): The column name to sort.
            reverse (bool): True for descending order, False for ascending.
        """
        data = []
        for item in self.tree.get_children():
            value = self.tree.set(item, col)
            data.append((value, item))

        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (_, item) in enumerate(data):
            self.tree.move(item, '', index)

        self.sort_state[col] = not reverse
        self.tree.heading(col, command=lambda: self.sort_column_value(col, not reverse))
