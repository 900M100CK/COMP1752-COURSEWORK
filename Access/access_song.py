import sqlite3 as sql
from Model import SongItem
from config_database import DB_PATH
from tkinter import messagebox

class SongAccess:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path


    def _get_connection(self):
        """Get a connection to the database

        Returns:
            sqlite3.Connection: Database connection object
        """
        try:
            return sql.connect(self.db_path)
        except sql.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def check_exist(self, song_id):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM Songs WHERE song_id = ?", (song_id,))
            return c.fetchone()[0] > 0

    def insert(self, s: SongItem):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO Songs (song_id, media_id, album, artist, count_play)
                VALUES (?, ?, ?, ?, ?)
            ''', (s.song_id, s.media_id, s.album, s.artist, s.count_play))
            conn.commit()

    def update(self, s: SongItem):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE Songs
                SET album = ?, artist = ?, count_play = ?, media_id = ?
                WHERE song_id = ?
            ''', (s.album, s.artist, s.count_play, s.media_id, s.song_id))
            conn.commit()

    def save(self, s: SongItem):
        try:
            if self.check_exist(s.song_id):
                self.update(s)
            else:
                self.insert(s)
            print(f"Song '{s.title}' saved successfully.")
            return s.song_id  # Return the song_id on success
        except sql.Error as e:
            messagebox.showerror("Database Error", f"Failed to save song {s.song_id}: {str(e)}")
            raise
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error saving song {s.song_id}: {str(e)}")
            raise

    def update_song(self, song_id, title, artist, album, rating):
        """Update song details in both Media and Songs tables"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Update Media table
                cursor.execute("""
                    UPDATE Media 
                    SET title = ?, rating = ?
                    WHERE media_id = ?
                """, (title, rating, song_id))
                
                # Update Songs table
                cursor.execute("""
                    UPDATE Songs
                    SET artist = ?, album = ?
                    WHERE song_id = ?
                """, (artist, album, song_id))
                
                conn.commit()
                return True
        except sql.Error as e:
            messagebox.showerror("Database Error", f"Failed to update song: {str(e)}")
            return False

    def delete_song(self, song_id):
        """Delete a song from both Media and Songs tables"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Delete from Songs table first (due to foreign key constraint)
                cursor.execute("DELETE FROM Songs WHERE song_id = ?", (song_id,))
                
                # Delete from Media table
                cursor.execute("DELETE FROM Media WHERE media_id = ?", (song_id,))
                
                conn.commit()
                return True
        except sql.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete song: {str(e)}")
            return False
