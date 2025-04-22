import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
from tkinter import messagebox


def _format_duration(seconds):
    try:
        minutes = int(seconds) // 60
        remaining_seconds = int(seconds) % 60
        return f"{minutes:02d}:{remaining_seconds:02d}"
    except FileNotFoundError:
        return "N/A"

def _parse_song_data(data):
    """Parse song data from API response"""
    return {
        "title": data.get("title", "N/A"),
        "artist": {
            "name": data.get("artist", {}).get("name", "N/A")
        },
        "album": {
            "title": data.get("album", {}).get("title", "N/A"),
            "cover": data.get("album", {}).get("cover_big", "")
        },
        "duration": data.get("duration", "N/A"),
        "release_date": data.get("release_date", "N/A"),
        "link": data.get("link", "N/A")
    }

class SongDetailsPanel(ttk.Frame):
    """
    Panel for displaying detailed information about a selected song.
    Shows album cover, song details, and provides update functionality.
    """
    def __init__(self, parent, api_key=None):
        """
        Initialize the song details panel
        
        Args:
            parent: Parent widget
            api_key: API key for Deezer service
        """
        super().__init__(parent)
        self.api_key = api_key
        self.api_host = "deezerdevs-deezer.p.rapidapi.com"
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface components"""
        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create and configure frames
        self._setup_cover_frame()
        self._setup_details_frame()

    def _setup_cover_frame(self):
        """Set up the frame for album cover display"""
        # Create frame for album cover
        self.cover_frame = ttk.Frame(self)
        self.cover_frame.grid(row=0, column=0, sticky="ns", pady=5)
        self.cover_frame.columnconfigure(0, weight=1)

        # Create label for album cover
        self.cover_label = ttk.Label(self.cover_frame)
        self.cover_label.grid(row=0, column=0, sticky="nsew")

    def _setup_details_frame(self):
        """Set up the frame for song details"""
        # Create frame for song details
        self.details_frame = ttk.Frame(self)
        self.details_frame.grid(row=1, column=0, sticky="s")
        self.details_frame.columnconfigure(0, weight=1)

        # Create text widget for details - reduce height
        self.details_text = tk.Text(
            self.details_frame,
            wrap=tk.WORD,
            height=8,
            width=25,
            state=tk.DISABLED,
            font=("Arial", 9)  # Smaller font
        )
        self.details_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def update_song(self, song_id):
        """
        Update the panel with details for a specific song
        
        Args:
            song_id: ID of the song to display
        """
        # Clear current details
        self._clear_details()
        
        # Fetch song details from API by song_id was saved in Media table
        song_data = self._fetch_song_details(song_id)
        if song_data:
            # Update UI with song details
            self._update_cover(song_data.get('cover_url'))
            self._update_details(song_data)

    def _clear_details(self):
        """Clear the current song details from the panel"""
        # Clear cover image
        self.cover_label.configure(image='')
        # Clear details text
        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.configure(state=tk.DISABLED)

    def _fetch_song_details(self, song_id):
        """
        Fetch song details from the Deezer API
        
        Args:
            song_id: ID of the song to fetch
            
        Returns:
            dict: Song details or None if fetch failed
        """
        if not self.api_key:
            return None

        try:
            # Set up API request
            url = f"https://deezerdevs-deezer.p.rapidapi.com/track/{song_id}"
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            # Make API request
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return _parse_song_data(response.json())
            else:
                messagebox.showerror("API Error", f"Failed to fetch song details. Status code: {response.status_code}")
                return None
        except Exception:
            messagebox.showerror("Connection Error", f"Failed to connect to API")
            return None

    def _update_cover(self, cover_url):
        """
        Update the album cover image

        Args:
            cover_url: URL of the album cover image
        """
        if not cover_url:
            return

        try:
            # Fetch and process cover image
            response = requests.get(cover_url)
            # Send an HTTP GET request to the cover URL and store the server's response

            image_data = response.content
            # Get the raw binary content (image data) from the HTTP response

            image = Image.open(io.BytesIO(image_data))
            # Convert the binary image data into a file-like object and open it using PIL

            # Resize image while maintaining aspect ratio - smaller size
            max_size = (200, 200)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Convert to PhotoImage and update label
            photo = ImageTk.PhotoImage(image)
            self.cover_label.configure(image=photo)
            self.cover_label.image = photo
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load album cover: {str(e)}")
            self.cover_label.configure(image="")

    def _update_details(self, song_data):
        """
        Update the song details text

        Args:
            song_data: Dictionary containing song details
        """
        # Enable text widget for editing
        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)

        # Format and insert song details - simplified to essential info only
        details = [
            f"Title: {song_data.get('title', 'N/A')}",
            f"Artist: {song_data.get('artist', {}).get('name', 'N/A')}",
            f"Album: {song_data.get('album', {}).get('title', 'N/A')}",
            f"Duration: {_format_duration(song_data.get('duration', 'N/A'))}"

        ]

        self.details_text.insert(tk.END, "\n".join(details))
        self.details_text.configure(state=tk.DISABLED)

        if 'album' in song_data and 'cover' in song_data['album']:
            self._update_cover(song_data['album']['cover'])
        else:
            self.cover_label.configure(image="")

    def clear_details(self):
        """Clear the details text area without removing the panel"""
        if hasattr(self, 'details_text'):
            self.details_text.delete('1.0', tk.END)
            self.details_text.insert('1.0', "No song selected") 