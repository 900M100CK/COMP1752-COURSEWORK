import pytest
import sqlite3
import os
from Access.access_playlist import PlaylistAccess
from Model.playlist import Playlist
from config_database import DB_PATH

@pytest.fixture
def test_db():
    """Create a test database"""
    test_db_path = "test_playlists.db"
    yield test_db_path
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.fixture
def playlist_access(test_db):
    """Create a PlaylistAccess instance with test database"""
    return PlaylistAccess(test_db)

def test_initialize_database(playlist_access, test_db):
    """Test database initialization"""
    # Check if tables are created
    with sqlite3.connect(test_db) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in c.fetchall()]
        assert 'Playlists' in tables
        assert 'PlaylistSongs' in tables

def test_create_playlist(playlist_access):
    """Test creating a playlist"""
    name = "Test Playlist"
    description = "Test Description"
    
    # Create playlist
    playlist_id = playlist_access.create_playlist(name, description)
    assert playlist_id is not None
    
    # Verify playlist was created
    playlist = playlist_access.get_playlist(playlist_id)
    assert playlist is not None
    assert playlist.name == name
    assert playlist.description == description

def test_get_playlist(playlist_access):
    """Test retrieving a playlist"""
    # First create a playlist
    name = "Test Playlist"
    description = "Test Description"
    playlist_id = playlist_access.create_playlist(name, description)
    
    # Get the playlist
    playlist = playlist_access.get_playlist(playlist_id)
    assert playlist is not None
    assert playlist.name == name
    assert playlist.description == description

def test_get_all_playlists(playlist_access):
    """Test retrieving all playlists"""
    # Create multiple playlists
    playlists_data = [
        {
            'name': 'Playlist 1',
            'description': 'Description 1'
        },
        {
            'name': 'Playlist 2',
            'description': 'Description 2'
        }
    ]
    
    for data in playlists_data:
        playlist_access.create_playlist(data['name'], data['description'])
    
    # Get all playlists
    all_playlists = playlist_access.get_all_playlists()
    assert len(all_playlists) == len(playlists_data)
    assert all_playlists[0].name == playlists_data[0]['name']
    assert all_playlists[1].name == playlists_data[1]['name']

def test_add_song_to_playlist(playlist_access):
    """Test adding a song to a playlist"""
    # First create a playlist
    playlist_id = playlist_access.create_playlist("Test Playlist", "Test Description")
    
    # Add a song to the playlist
    song_id = 1
    result = playlist_access.add_song_to_playlist(playlist_id, song_id)
    assert result is True
    
    # Verify song was added
    playlist = playlist_access.get_playlist(playlist_id)
    assert song_id in playlist.songs

def test_remove_song_from_playlist(playlist_access):
    """Test removing a song from a playlist"""
    # First create a playlist and add a song
    playlist_id = playlist_access.create_playlist("Test Playlist", "Test Description")
    song_id = 1
    playlist_access.add_song_to_playlist(playlist_id, song_id)
    
    # Remove the song
    result = playlist_access.remove_song_from_playlist(playlist_id, song_id)
    assert result is True
    
    # Verify song was removed
    playlist = playlist_access.get_playlist(playlist_id)
    assert song_id not in playlist.songs

def test_play_playlist(playlist_access):
    """Test playing a playlist"""
    # First create a playlist and add a song
    playlist_id = playlist_access.create_playlist("Test Playlist", "Test Description")
    song_id = 1
    playlist_access.add_song_to_playlist(playlist_id, song_id)
    
    # Play the playlist
    result = playlist_access.play_playlist(playlist_id)
    assert result is True
    
    # Verify play count was updated
    playlist = playlist_access.get_playlist(playlist_id)
    assert playlist.count_play == 1

def test_update_playlist(playlist_access):
    """Test updating a playlist"""
    # First create a playlist
    playlist_id = playlist_access.create_playlist("Original Name", "Original Description")
    
    # Update the playlist
    updated_playlist = Playlist(playlist_id, "Updated Name", "Updated Description")
    updated_playlist.add_song(1)  # Add a song
    result = playlist_access.update_playlist(updated_playlist)
    assert result is True
    
    # Verify update
    playlist = playlist_access.get_playlist(playlist_id)
    assert playlist.name == "Updated Name"
    assert playlist.description == "Updated Description"
    assert 1 in playlist.songs

def test_delete_playlist(playlist_access):
    """Test deleting a playlist"""
    # First create a playlist
    playlist_id = playlist_access.create_playlist("Test Playlist", "Test Description")
    
    # Delete the playlist
    result = playlist_access.delete_playlist(playlist_id)
    assert result is True
    
    # Verify deletion
    deleted_playlist = playlist_access.get_playlist(playlist_id)
    assert deleted_playlist is None 