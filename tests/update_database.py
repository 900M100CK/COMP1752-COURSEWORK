import sqlite3 as sql
import os
from config_database import DB_PATH

def update_database():
    """
    Update the database schema by dropping all existing tables
    and recreating them with new columns.
    """
    print(f"Updating database at {DB_PATH}")
    
    # Remove the initialization flag if it exists
    flag_path = os.path.join(os.path.dirname(DB_PATH), "db_initialized.flag")
    if os.path.exists(flag_path):
        os.remove(flag_path)
        print("Removed initialization flag.")
    
    # Delete the database file if it exists
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Removed existing database file.")
        except Exception as e:
            print(f"Error removing database file: {e}")
            return
    
    # Create a new database with updated schema
    try:
        conn = sql.connect(DB_PATH)
        c = conn.cursor()
        
        # Create Media table with additional columns
        c.execute('''
            CREATE TABLE IF NOT EXISTS Media (
                media_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                rating INTEGER NOT NULL,
                duration INTEGER DEFAULT 0,
                genre TEXT DEFAULT 'Unknown',
                year TEXT DEFAULT 'Unknown',
                cover_url TEXT DEFAULT ''
            )
        ''')
        
        # Create Songs table with foreign key to Media
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
        
        # Create Playlists table
        c.execute('''
            CREATE TABLE IF NOT EXISTS Playlists (
                playlist_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                count_play INTEGER DEFAULT 0
            )
        ''')
        
        # Create PlaylistSongs junction table
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
        conn.close()
        
        print("Database schema updated successfully.")
        
        # Create initialization flag
        with open(flag_path, 'w') as f:
            f.write("initialized")
        print("Created new initialization flag.")
        
    except Exception as e:
        print(f"Error creating new database: {e}")
        
if __name__ == "__main__":
    # Ask for confirmation
    confirm = input("This will delete your existing database and create a new one. All data will be lost. Continue? (y/n): ")
    if confirm.lower() == 'y':
        update_database()
    else:
        print("Operation cancelled.") 