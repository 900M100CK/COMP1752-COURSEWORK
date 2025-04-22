from Model.media_item import MediaItem


class SongItem(MediaItem):
    """
    Represents a song in the jukebox application.
    Extends MediaItem with song-specific attributes and methods.
    """
    def __init__(self, song_id, media_id=None, title="", artist="", rating=0, album="", count_play=0, duration=0, genre="", year="", cover_url=""):
        """
        Initialize a song item with detailed information
        
        Args:
            song_id (int): Unique identifier for the song
            media_id (int): ID of the related media item
            title (str): Title of the song
            artist (str): Artist who created the song
            rating (int): User rating of the song (1-5)
            album (str): Album the song belongs to
            count_play (int): Number of times the song has been played
            duration (int): Duration of the song in seconds
            genre (str): Genre of the song
            year (str): Year the song was released
            cover_url (str): URL to the album cover image
        """
        # Initialize base class with common attributes
        super().__init__(title, rating)
        
        # Song-specific attributes
        self.song_id = song_id
        self.media_id = media_id if media_id is not None else song_id
        self.artist = artist
        self.album = album
        self.count_play = count_play
        self.duration = duration
        self.genre = genre
        self.year = year
        self.cover_url = cover_url

    def get_duration_formatted(self):
        """
        Get the song duration in a formatted string (MM:SS)
        
        Returns:
            str: Formatted duration string
        """
        # Calculate minutes and seconds
        minutes = self.duration // 60
        seconds = self.duration % 60
        # Return formatted string
        return f"{minutes:02d}:{seconds:02d}"

    def info(self):
        """
        Get a string representation of the song
        
        Returns:
            str: Formatted string with song details
        """
        # Return formatted string with song details
        return f"{self.title} by {self.artist} ({self.album})"

    def to_dict(self):
        return {
            "song_id": self.song_id,
            "media_id": self.media_id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "rating": self.rating,
            "count_play": self.count_play
        }

    def info(self):
        return f"{self.album} {self.title} {self.artist} {self.stars()}"

    def stars(self):
        # Handle potential non-integer ratings gracefully
        try:
            stars = self.rating *"🥰"
            empty_stars = (5-self.rating) *"🫥"
        except (ValueError, TypeError):
            stars,empty_stars = "?" # Or some other indicator
        return f"{stars}{empty_stars}"

