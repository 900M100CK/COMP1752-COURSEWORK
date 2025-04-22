import pytest
from Model.song_item import SongItem

def test_song_item_initialization():
    """Test that a SongItem is initialized with correct attributes"""
    song_id = 1
    media_id = 2
    title = "Test Song"
    artist = "Test Artist"
    rating = 4
    album = "Test Album"
    count_play = 5
    duration = 180
    genre = "Rock"
    year = "2023"
    cover_url = "http://example.com/cover.jpg"
    
    song = SongItem(
        song_id=song_id,
        media_id=media_id,
        title=title,
        artist=artist,
        rating=rating,
        album=album,
        count_play=count_play,
        duration=duration,
        genre=genre,
        year=year,
        cover_url=cover_url
    )
    
    assert song.song_id == song_id
    assert song.media_id == media_id
    assert song.title == title
    assert song.artist == artist
    assert song.rating == rating
    assert song.album == album
    assert song.count_play == count_play
    assert song.duration == duration
    assert song.genre == genre
    assert song.year == year
    assert song.cover_url == cover_url

def test_song_item_inheritance():
    """Test that SongItem properly inherits from MediaItem"""
    song = SongItem(song_id=1, title="Test Song", rating=4)
    
    # Test inheritance of info method
    assert song.info() == f"{song.album} {song.title} {song.artist} {song.stars()}"

def test_get_duration_formatted():
    """Test formatting of duration"""
    song = SongItem(song_id=1, duration=185)  # 3:05
    
    assert song.get_duration_formatted() == "03:05"
    
    song.duration = 60  # 1:00
    assert song.get_duration_formatted() == "01:00"
    
    song.duration = 5  # 0:05
    assert song.get_duration_formatted() == "00:05"

def test_to_dict():
    """Test conversion to dictionary"""
    song = SongItem(
        song_id=1,
        media_id=2,
        title="Test Song",
        artist="Test Artist",
        rating=4,
        album="Test Album",
        count_play=5
    )
    
    expected_dict = {
        "song_id": 1,
        "media_id": 2,
        "title": "Test Song",
        "artist": "Test Artist",
        "album": "Test Album",
        "rating": 4,
        "count_play": 5
    }
    
    assert song.to_dict() == expected_dict

def test_stars_rating():
    """Test stars representation of rating"""
    song = SongItem(song_id=1, rating=3)
    
    # Should have 3 filled stars and 2 empty stars
    assert song.stars() == "🥰🥰🥰🫥🫥"
    
    song.rating = 5
    assert song.stars() == "🥰🥰🥰🥰🥰"
    
    song.rating = 0
    assert song.stars() == "🫥🫥🫥🫥🫥" 