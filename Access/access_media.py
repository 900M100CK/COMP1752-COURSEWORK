import sqlite3 as sql
from Model import MediaItem, SongItem
from access_song import SongAccess
from config_database import DB_PATH
import os
from tkinter import messagebox

class MediaItemAccess:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        # Initialize database if it doesn't exist
        self.initialize_database()
        
        # Create SongAccess with the same database path
        self.song_access = SongAccess(self.db_path)
        
    def _get_connection(self):
        """Get a connection to the database

        Returns:
            sqlite3.Connection: Database connection object
        """
        try:
            return sql.connect(self.db_path)
        except sql.Error:
            print(f"Error connecting to database")
            raise

    def initialize_database(self):
        try:
            flag_path = os.path.join(os.path.dirname(self.db_path), "db_initialized.flag")
            if os.path.exists(flag_path):
                return  # Already initialized, no need to recreate

            with self._get_connection() as conn:
                c = conn.cursor()
                # Create Media table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS Media (
                        media_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                        duration INTEGER DEFAULT 0,
                        genre TEXT DEFAULT 'Unknown',
                        year TEXT DEFAULT 'Unknown',
                        cover_url TEXT DEFAULT ''
                    )
                ''')

                # Create Songs table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS Songs (
                        song_id INTEGER PRIMARY KEY,
                        media_id INTEGER,
                        album TEXT,
                        artist TEXT NOT NULL,
                        count_play INTEGER DEFAULT 0,
                        FOREIGN KEY (media_id) REFERENCES Media (media_id)
                    )
                ''')
                conn.commit()
                print("Database tables created successfully.")
                with open(flag_path, 'w') as f:
                    f.write("initialized")

        except sql.Error:
            print(f"Error initializing database")
        except Exception:
            print(f"An unexpected error occurred during database initialization")

    def insert(self, media_id, title, rating, duration=0, genre="Unknown", year="Unknown", cover_url=""):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO Media (media_id, title, rating, duration, genre, year, cover_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (media_id, title, rating, duration, genre, year, cover_url))
            conn.commit()
            return media_id

    def update(self, media_id, title, rating, duration=0, genre="Unknown", year="Unknown", cover_url=""):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE Media
                SET title = ?, rating = ?, duration = ?, genre = ?, year = ?, cover_url = ?
                WHERE media_id = ?
            ''', (title, rating, duration, genre, year, cover_url, media_id))
            conn.commit()
            return media_id

    def check_exist(self, media_id):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM Media WHERE media_id = ?", (media_id,))
            exists = c.fetchone()[0] > 0
            return exists

    def save(self, media):
        """Save media item and if it's a song, also save the song details"""
        try:
            # Handle case where we're passing a SongItem object
            if isinstance(media, SongItem):
                media_id = media.song_id  # Use song_id as media_id
                title = media.title
                rating = media.rating
                duration = getattr(media, 'duration', 0)
                genre = getattr(media, 'genre', 'Unknown')
                year = getattr(media, 'year', 'Unknown')
                cover_url = getattr(media, 'cover_url', '')
                
                # First save the media
                if self.check_exist(media_id):
                    self.update(media_id, title, rating, duration, genre, year, cover_url)
                else:
                    self.insert(media_id, title, rating, duration, genre, year, cover_url)
                
                # Then save the song details
                try:
                    self.song_access.save(media)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save song details: {str(e)}")
                    raise
                
                messagebox.showinfo("Success", f"Successfully saved song: {media.title}")
                return media_id
            
            # Handle normal MediaItem
            elif isinstance(media, MediaItem):
                media_id = getattr(media, 'media_id', None)
                if not media_id:
                    messagebox.showerror("Error", "Media item has no media_id")
                    return None
                    
                title = media.title
                rating = media.rating
                duration = getattr(media, 'duration', 0)
                genre = getattr(media, 'genre', 'Unknown')
                year = getattr(media, 'year', 'Unknown')
                cover_url = getattr(media, 'cover_url', '')
                
                if self.check_exist(media_id):
                    return self.update(media_id, title, rating, duration, genre, year, cover_url)
                else:
                    return self.insert(media_id, title, rating, duration, genre, year, cover_url)
            
            # Handle case where we're passing raw parameters
            else:
                if "media_id" in media and "title" in media:
                    media_id = media["media_id"]
                    title = media["title"]
                    rating = media.get("rating", 0)
                    duration = media.get("duration", 0)
                    genre = media.get("genre", "Unknown")
                    year = media.get("year", "Unknown")
                    cover_url = media.get("cover_url", "")
                    
                    if self.check_exist(media_id):
                        return self.update(media_id, title, rating, duration, genre, year, cover_url)
                    else:
                        return self.insert(media_id, title, rating, duration, genre, year, cover_url)
                else:
                    messagebox.showerror("Error", "Invalid media data format")
                    return None

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save media: {str(e)}")
            raise

