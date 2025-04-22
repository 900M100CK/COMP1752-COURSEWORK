class Playlist:
    """
    Represents a playlist in the jukebox application.
    Contains a collection of media items and provides methods to manage them.
    """
    def __init__(self, playlist_id, name, description="", count_play=0):
        """
        Initialize a new playlist
        
        Args:
            playlist_id (int): Unique identifier for the playlist
            name (str): Name of the playlist
        """
        self.playlist_id = playlist_id
        self.name = name
        self.description = description
        self.count_play = count_play
        self.songs = []  # List of song IDs in this playlist

    def add_song(self, song_id):
        if song_id not in self.songs:
            self.songs.append(song_id)

    def remove_song(self, song_id):
        if song_id in self.songs:
            self.songs.remove(song_id)

    def play(self):
        self.count_play += 1
        return self.songs  # Return list of song IDs to play

    def info(self):
        return f"Playlist: {self.name} ({len(self.songs)} songs)"

    def delete(self):
        """
        Mark the playlist for deletion
        
        This method prepares the playlist for deletion by clearing its songs list
        to avoid any references and indicates it should be deleted.
        
        Returns:
            int: The ID of the playlist to delete
        """
        # Clear the songs list to avoid any reference issues
        self.songs.clear()
        return self.playlist_id

