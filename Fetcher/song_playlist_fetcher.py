import sqlite3 as sql
from config_database import DB_PATH
from tkinter import messagebox

class SongPlaylistFetcher:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_connection(self):
        """Get a connection to the database"""
        try:
            return sql.connect(self.db_path)
        except sql.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_playlist_songs(self, playlist_id):
        """Get all songs in a playlist with their details"""
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                # Join PlaylistSongs with Songs and Media tables to get all song details
                c.execute('''
                    SELECT 
                        s.song_id,
                        m.title,
                        s.artist,
                        s.album,
                        m.rating,
                        s.count_play,
                        m.duration,
                        m.genre,
                        m.year,
                        m.cover_url
                    FROM PlaylistSongs ps
                    JOIN Songs s ON ps.song_id = s.song_id
                    JOIN Media m ON s.media_id = m.media_id
                    WHERE ps.playlist_id = ?
                    ORDER BY m.title
                ''', (playlist_id,))
                
                rows = c.fetchall()
                if not rows:
                    return []
                
                # Format results as list of dictionaries
                results = []
                for row in rows:
                    results.append({
                        "song_id": row[0],
                        "title": row[1],
                        "artist": row[2],
                        "album": row[3],
                        "rating": (row[4]* "⭐"+(5-row[4])*" ☆"),
                        "count_play": row[5],
                        "duration": row[6] if len(row) > 6 else 0,
                        "genre": row[7] if len(row) > 7 else "Unknown",
                        "year": row[8] if len(row) > 8 else "Unknown",
                        "cover_url": row[9] if len(row) > 9 else ""
                    })
                return results
                
        except sql.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to fetch playlist songs: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return []

    def get_song_details(self, song_id):
        """Get details for a specific song"""
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                # Join Songs with Media table to get all song details
                c.execute('''
                    SELECT 
                        s.song_id,
                        m.title,
                        s.artist,
                        s.album,
                        m.rating,
                        s.count_play,
                        m.duration,
                        m.genre,
                        m.year,
                        m.cover_url
                    FROM Songs s
                    JOIN Media m ON s.media_id = m.media_id
                    WHERE s.song_id = ?
                ''', (song_id,))
                
                row = c.fetchone()
                if not row:
                    return None
                
                return {
                    "song_id": row[0],
                    "title": row[1],
                    "artist": row[2],
                    "album": row[3],
                    "rating": row[4],
                    "count_play": row[5],
                    "duration": row[6] if len(row) > 6 else 0,
                    "genre": row[7] if len(row) > 7 else "Unknown",
                    "year": row[8] if len(row) > 8 else "Unknown",
                    "cover_url": row[9] if len(row) > 9 else ""
                }
                
        except sql.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Failed to fetch song details: {str(e)}")
            return None 