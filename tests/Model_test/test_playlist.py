import pytest
from Model.playlist import Playlist
from Model.media_item import MediaItem

def test_playlist_initialization():
    """Test that a Playlist is initialized with correct attributes"""
    playlist_id = 1
    name = "Test Playlist"
    description = "Test Description"
    count_play = 0
    
    playlist = Playlist(playlist_id, name, description, count_play)
    
    assert playlist.playlist_id == playlist_id
    assert playlist.name == name
    assert playlist.description == description
    assert playlist.count_play == count_play
    assert playlist.songs == []

def test_add_and_remove_song():
    """Test adding and removing songs from playlist"""
    playlist = Playlist(1, "Test Playlist")
    
    # Add songs
    playlist.add_song(1)
    playlist.add_song(2)
    playlist.add_song(3)
    
    assert playlist.songs == [1, 2, 3]
    
    # Add duplicate song (should not add)
    playlist.add_song(2)
    assert playlist.songs == [1, 2, 3]
    
    # Remove song
    playlist.remove_song(2)
    assert playlist.songs == [1, 3]
    
    # Remove non-existent song (should not error)
    playlist.remove_song(5)
    assert playlist.songs == [1, 3]

def test_play_increases_count():
    """Test that play() method increases count_play and returns songs"""
    playlist = Playlist(1, "Test Playlist")
    playlist.add_song(1)
    playlist.add_song(2)
    
    initial_count = playlist.count_play
    result = playlist.play()
    
    assert playlist.count_play == initial_count + 1
    assert result == [1, 2]

def test_str_representation():
    """Test string representation of playlist"""
    playlist = Playlist(1, "Test Playlist")
    playlist.add_song(1)
    playlist.add_song(2)
    
    expected = "Playlist: Test Playlist (2 songs)"
    assert str(playlist) == expected

def test_delete():
    """Test delete() method clears songs and returns ID"""
    playlist = Playlist(1, "Test Playlist")
    playlist.add_song(1)
    playlist.add_song(2)
    
    result = playlist.delete()
    
    assert result == 1
    assert playlist.songs == [] 