import sqlite3 as sql
from config_database import DB_PATH


class SongFetcher:
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
        
    def fetch_all_songs(self):
        query = """
        SELECT 
            s.album, 
            s.song_id, 
            m.title, 
            s.artist, 
            m.rating, 
            s.count_play,
            m.duration,
            m.genre,
            m.year,
            m.cover_url
        FROM Songs s
        JOIN Media m ON s.media_id = m.media_id
        """

        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute(query)
                rows = c.fetchall()
                return self._format_results(rows)

        except sql.Error as e:
            print(f"[Database Error] {e}")
            return []
        except Exception as e:
            print(f"[Unexpected Error] {e}")
            return []

    def search_songs(self, search_term, search_field="title"):
        """
        Search for songs based on a search term and field
        Args:
            search_term (str): The term to search for
            search_field (str): The field to search in ('title', 'artist', 'album', 'all')
        Returns:
            tuple: (rows, formatted_results)
        """
        # Validate search field
        valid_fields = ['title', 'artist', 'album', 'all']
        if search_field not in valid_fields:
            raise ValueError(f"Invalid search field. Must be one of: {valid_fields}")

        # Build the query based on search field
        if search_field == 'all':
            query = """
            SELECT 
                s.album, 
                s.song_id, 
                m.title, 
                s.artist, 
                m.rating, 
                s.count_play,
                m.duration,
                m.genre,
                m.year,
                m.cover_url
            FROM Songs s
            JOIN Media m ON s.media_id = m.media_id
            WHERE (LOWER(m.title) LIKE LOWER(?) OR 
                  LOWER(s.artist) LIKE LOWER(?) OR 
                  LOWER(s.album) LIKE LOWER(?))
            """
            params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        else:
            field_map = {
                'title': 'm.title',
                'artist': 's.artist',
                'album': 's.album'
            }
            query = f"""
            SELECT 
                s.album, 
                s.song_id, 
                m.title, 
                s.artist, 
                m.rating, 
                s.count_play,
                m.duration,
                m.genre,
                m.year,
                m.cover_url
            FROM Songs s
            JOIN Media m ON s.media_id = m.media_id
            WHERE LOWER({field_map[search_field]}) LIKE LOWER(?)
            """
            params = (f'%{search_term}%',)

        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute(query, params)
                rows = c.fetchall()
                return self._format_results(rows)

        except sql.Error as e:
            print(f"[Database Error] {e}")
            return []
        except Exception as e:
            print(f"[Unexpected Error] {e}")
            return []

    def _format_results(self, rows):
        """Format the database rows into a list of dictionaries"""
        result = []
        for row in rows:
            result.append({
                "album": row[0],
                "#": row[1],
                "title": row[2],
                "artist": row[3],
                "rating": (row[4]* "⭐"+(5-row[4])*" ☆"),
                "count_play": row[5],
                "duration": row[6] if len(row) > 6 else 0,
                "genre": row[7] if len(row) > 7 else "Unknown",
                "year": row[8] if len(row) > 8 else "Unknown",
                "cover_url": row[9] if len(row) > 9 else ""
            })
        return result

    def get_song_details(self, song_id):
        """
        Get details for a specific song by ID
        Returns: tuple (id, album, title, artist, rating, count_play) or None if not found
        """
        """Get details for a specific song"""
        query = """
        SELECT 
            s.album, 
            s.song_id, 
            m.title, 
            s.artist, 
            m.rating, 
            s.count_play,
            m.duration,
            m.genre,
            m.year,
            m.cover_url
        FROM Songs s
        JOIN Media m ON s.media_id = m.media_id
        WHERE s.song_id = ?
        """
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute(query, (song_id,))
                row = c.fetchone()
                if row:
                    return {
                        "album": row[0],
                        "#": row[1],
                        "title": row[2],
                        "artist": row[3],
                        "rating": row[4],
                        "count_play": row[5],
                        "duration": row[6] if len(row) > 6 else 0,
                        "genre": row[7] if len(row) > 7 else "Unknown",
                        "year": row[8] if len(row) > 8 else "Unknown",
                        "cover_url": row[9] if len(row) > 9 else ""
                    }
                return None
        except sql.Error as e:
            print(f"[Database Error] {e}")
            return None


