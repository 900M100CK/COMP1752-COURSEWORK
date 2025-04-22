import sqlite3 as sql
from Model import Playlist
from config_database import DB_PATH
from tkinter import messagebox

class PlaylistAccess:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.initialize_database()

    def _get_connection(self):
        try:
            return sql.connect(self.db_path)
        except sql.Error:
            print(f"Error connecting to database")
            raise

    def initialize_database(self):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                
                # Create Playlists table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS Playlists (
                        playlist_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        count_play INTEGER DEFAULT 0
                    )
                ''')

                # Create PlaylistSongs table (junction table)
                c.execute('''
                    CREATE TABLE IF NOT EXISTS PlaylistSongs (
                        playlist_id INTEGER,
                        song_id INTEGER,
                        FOREIGN KEY (playlist_id) REFERENCES Playlists (playlist_id),
                        FOREIGN KEY (song_id) REFERENCES Songs (song_id),
                        PRIMARY KEY (playlist_id, song_id)
                    )
                ''')
                conn.commit()

        except sql.Error:
            print(f"Error initializing database")

    def create_playlist(self, name, description=""):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO Playlists (name, description)
                    VALUES (?, ?)
                ''', (name, description))
                playlist_id = c.lastrowid
                conn.commit()
                return playlist_id
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to create playlist")
            return None

    def get_playlist(self, playlist_id):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    SELECT name, description, count_play
                    FROM Playlists
                    WHERE playlist_id = ?
                ''', (playlist_id,))
                result = c.fetchone()
                if result:
                    playlist = Playlist(playlist_id, result[0], result[1], result[2])
                    # Get songs in playlist
                    c.execute('''
                        SELECT song_id
                        FROM PlaylistSongs
                        WHERE playlist_id = ?
                    ''', (playlist_id,))
                    for song_id in c.fetchall():
                        playlist.add_song(song_id[0])
                    return playlist
                return None
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to get playlist")
            return None

    def get_all_playlists(self):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('SELECT playlist_id FROM Playlists')
                return [self.get_playlist(row[0]) for row in c.fetchall()]
        except sql.Error:
            messagebox.showerror("Database Error", f"Don't have any playlist")
            return []

    def add_song_to_playlist(self, playlist_id, song_id):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO PlaylistSongs (playlist_id, song_id)
                    VALUES (?, ?)
                ''', (playlist_id, song_id))
                conn.commit()
                return True
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to add song to playlist")
            return False

    def remove_song_from_playlist(self, playlist_id, song_id):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    DELETE FROM PlaylistSongs
                    WHERE playlist_id = ? AND song_id = ?
                ''', (playlist_id, song_id))
                conn.commit()
                return True
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to remove song from playlist")
            return False

    def play_playlist(self, playlist_id):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                
                # Update playlist play count
                c.execute('''
                    UPDATE Playlists
                    SET count_play = count_play + 1
                    WHERE playlist_id = ?
                ''', (playlist_id,))
                
                # Get songs in the playlist
                c.execute('''
                    SELECT song_id 
                    FROM PlaylistSongs 
                    WHERE playlist_id = ?
                ''', (playlist_id,))
                song_ids = [row[0] for row in c.fetchall()]
                
                # Update song play counts
                for song_id in song_ids:
                    c.execute('''
                        UPDATE Songs
                        SET count_play = count_play + 1
                        WHERE song_id = ?
                    ''', (song_id,))
                
                conn.commit()
                return True
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to update play counts")
            return False

    def update_playlist(self, playlist: Playlist):
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                # Update playlist details
                c.execute('''
                    UPDATE Playlists 
                    SET name = ?, description = ?
                    WHERE playlist_id = ?
                ''', (playlist.name, playlist.description, playlist.playlist_id))

                # Update playlist songs
                # First delete existing songs
                c.execute("DELETE FROM PlaylistSongs WHERE playlist_id = ?", (playlist.playlist_id,))
                
                # Then insert current songs
                for song_id in playlist.songs:
                    c.execute('''
                        INSERT INTO PlaylistSongs (playlist_id, song_id)
                        VALUES (?, ?)
                    ''', (playlist.playlist_id, song_id))
                
                conn.commit()
                return True
        except sql.Error:
            messagebox.showerror("Database Error", f"Failed to update playlist")
            return False

    def delete_playlist(self, playlist_id):
        """
        Delete a playlist from the database
        
        Args:
            playlist_id: ID of the playlist to delete
            
        Returns:
            bool: True if playlist was deleted successfully, False otherwise
        """
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                
                # First delete all playlist songs
                c.execute('''
                    DELETE FROM PlaylistSongs
                    WHERE playlist_id = ?
                ''', (playlist_id,))
                
                # Then delete the playlist itself
                c.execute('''
                    DELETE FROM Playlists
                    WHERE playlist_id = ?
                ''', (playlist_id,))
                
                conn.commit()
                return True
        except sql.Error :
            messagebox.showerror("Database Error", f"Failed to delete playlist")
            return False

   
