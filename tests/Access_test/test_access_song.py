import pytest
import sqlite3
import os
from Access.access_song import SongAccess
from config_database import DB_PATH

@pytest.fixture
def test_db():
    """Create a test database"""
    test_db_path = "test_songs.db"
    yield test_db_path
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.fixture
def song_access(test_db):
    """Create a SongAccess instance with test database"""
    return SongAccess(test_db)

def test_initialize_database(song_access, test_db):
    """Test database initialization"""
    # Check if tables are created
    with sqlite3.connect(test_db) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in c.fetchall()]
        assert 'Songs' in tables
        assert 'Media' in tables

def test_save_song(song_access):
    """Test saving a song"""
    song_data = {
        'song_id': 1,
        'title': 'Test Song',
        'artist': 'Test Artist',
        'album': 'Test Album',
        'rating': 5,
        'count_play': 0
    }
    
    # Save song
    result = song_access.save(song_data)
    assert result == song_data['song_id']
    
    # Verify song was saved
    saved_song = song_access.get_song(song_data['song_id'])
    assert saved_song is not None
    assert saved_song['title'] == song_data['title']
    assert saved_song['artist'] == song_data['artist']

def test_get_song(song_access):
    """Test retrieving a song"""
    # First save a song
    song_data = {
        'song_id': 1,
        'title': 'Test Song',
        'artist': 'Test Artist',
        'album': 'Test Album',
        'rating': 5,
        'count_play': 0
    }
    song_access.save(song_data)
    
    # Get the song
    song = song_access.get_song(song_data['song_id'])
    assert song is not None
    assert song['title'] == song_data['title']
    assert song['artist'] == song_data['artist']

def test_get_all_songs(song_access):
    """Test retrieving all songs"""
    # Save multiple songs
    songs = [
        {
            'song_id': 1,
            'title': 'Song 1',
            'artist': 'Artist 1',
            'album': 'Album 1',
            'rating': 5,
            'count_play': 0
        },
        {
            'song_id': 2,
            'title': 'Song 2',
            'artist': 'Artist 2',
            'album': 'Album 2',
            'rating': 4,
            'count_play': 0
        }
    ]
    
    for song in songs:
        song_access.save(song)
    
    # Get all songs
    all_songs = song_access.get_all_songs()
    assert len(all_songs) == len(songs)
    assert all_songs[0]['title'] == songs[0]['title']
    assert all_songs[1]['title'] == songs[1]['title']

def test_update_song(song_access):
    """Test updating a song"""
    # First save a song
    song_data = {
        'song_id': 1,
        'title': 'Original Title',
        'artist': 'Original Artist',
        'album': 'Original Album',
        'rating': 3,
        'count_play': 0
    }
    song_access.save(song_data)
    
    # Update the song
    updated_data = song_data.copy()
    updated_data['title'] = 'Updated Title'
    updated_data['rating'] = 5
    song_access.update(updated_data)
    
    # Verify update
    updated_song = song_access.get_song(song_data['song_id'])
    assert updated_song['title'] == 'Updated Title'
    assert updated_song['rating'] == 5

def test_delete_song(song_access):
    """Test deleting a song"""
    # First save a song
    song_data = {
        'song_id': 1,
        'title': 'Test Song',
        'artist': 'Test Artist',
        'album': 'Test Album',
        'rating': 5,
        'count_play': 0
    }
    song_access.save(song_data)
    
    # Delete the song
    song_access.delete(song_data['song_id'])
    
    # Verify deletion
    deleted_song = song_access.get_song(song_data['song_id'])
    assert deleted_song is None 