import pytest
import sqlite3
import os
from Access.access_media import MediaItemAccess
from Model.media_item import MediaItem
from Model.song_item import SongItem

@pytest.fixture
def test_db():
    """Create a test database"""
    test_db_path = "test_media.db"
    # Cleanup any existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    if os.path.exists("db_initialized.flag"):
        os.remove("db_initialized.flag")
    yield test_db_path
    # Cleanup after test
    try:
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        if os.path.exists("db_initialized.flag"):
            os.remove("db_initialized.flag")
    except PermissionError:
        pass  # Ignore cleanup errors

@pytest.fixture
def media_access(test_db):
    """Create a MediaItemAccess instance with test database"""
    access = MediaItemAccess(test_db)
    # Ensure database is initialized
    access.initialize_database()
    return access

def test_initialize_database(media_access, test_db):
    """Test database initialization"""
    # Check if tables are created
    with sqlite3.connect(test_db) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in c.fetchall()]
        assert 'Media' in tables
        assert 'Songs' in tables

def test_insert_media(media_access):
    """Test inserting a media item"""
    media_data = {
        'media_id': 1,
        'title': 'Test Media',
        'rating': 5,
        'duration': 180,
        'genre': 'Test Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    
    # Insert media
    result = media_access.insert(**media_data)
    assert result == media_data['media_id']
    
    # Verify insertion
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Media WHERE media_id = ?", (media_data['media_id'],))
        row = c.fetchone()
        assert row is not None
        assert row[1] == media_data['title']
        assert row[2] == media_data['rating']

def test_update_media(media_access):
    """Test updating a media item"""
    # First insert a media item
    media_data = {
        'media_id': 1,
        'title': 'Original Title',
        'rating': 3,
        'duration': 180,
        'genre': 'Original Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    media_access.insert(**media_data)
    
    # Update the media
    updated_data = media_data.copy()
    updated_data['title'] = 'Updated Title'
    updated_data['rating'] = 5
    result = media_access.update(**updated_data)
    assert result == media_data['media_id']
    
    # Verify update
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Media WHERE media_id = ?", (media_data['media_id'],))
        row = c.fetchone()
        assert row[1] == 'Updated Title'
        assert row[2] == 5

def test_check_exist(media_access):
    """Test checking if a media item exists"""
    # First insert a media item
    media_data = {
        'media_id': 1,
        'title': 'Test Media',
        'rating': 5,
        'duration': 180,
        'genre': 'Test Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    media_access.insert(**media_data)
    
    # Check existence
    assert media_access.check_exist(media_data['media_id']) is True
    assert media_access.check_exist(999) is False

def test_save_media_item(media_access):
    """Test saving a MediaItem object"""
    media = MediaItem(
        media_id=1,
        title='Test Media',
        rating=5,
        duration=180,
        genre='Test Genre',
        year='2023',
        cover_url='http://test.com/cover.jpg'
    )
    
    # Save media item
    result = media_access.save(media)
    assert result == media.media_id
    
    # Verify save
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Media WHERE media_id = ?", (media.media_id,))
        row = c.fetchone()
        assert row is not None
        assert row[1] == media.title
        assert row[2] == media.rating

def test_save_song_item(media_access):
    """Test saving a SongItem object"""
    song = SongItem(
        song_id=1,
        title='Test Song',
        artist='Test Artist',
        album='Test Album',
        rating=5,
        count_play=0,
        duration=180,
        genre='Test Genre',
        year='2023',
        cover_url='http://test.com/cover.jpg'
    )
    
    # Save song item
    result = media_access.save(song)
    assert result == song.song_id
    
    # Verify save in both tables
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        # Check Media table
        c.execute("SELECT * FROM Media WHERE media_id = ?", (song.song_id,))
        media_row = c.fetchone()
        assert media_row is not None
        assert media_row[1] == song.title
        
        # Check Songs table
        c.execute("SELECT * FROM Songs WHERE song_id = ?", (song.song_id,))
        song_row = c.fetchone()
        assert song_row is not None
        assert song_row[3] == song.artist

def test_save_raw_data(media_access):
    """Test saving raw media data"""
    media_data = {
        'media_id': 1,
        'title': 'Test Media',
        'rating': 5,
        'duration': 180,
        'genre': 'Test Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    
    # Save raw data
    result = media_access.save(media_data)
    assert result == media_data['media_id']
    
    # Verify save
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Media WHERE media_id = ?", (media_data['media_id'],))
        row = c.fetchone()
        assert row is not None
        assert row[1] == media_data['title']
        assert row[2] == media_data['rating']

def test_save_invalid_data(media_access):
    """Test saving invalid media data"""
    invalid_data = {
        'title': 'Test Media'  # Missing media_id
    }
    
    # Try to save invalid data
    result = media_access.save(invalid_data)
    assert result is None

def test_save_duplicate_media(media_access):
    """Test saving a duplicate media item"""
    media_data = {
        'media_id': 1,
        'title': 'Test Media',
        'rating': 5,
        'duration': 180,
        'genre': 'Test Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    
    # Save first time
    media_access.save(media_data)
    
    # Update and save again
    media_data['title'] = 'Updated Title'
    result = media_access.save(media_data)
    assert result == media_data['media_id']
    
    # Verify update
    with sqlite3.connect(media_access.db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Media WHERE media_id = ?", (media_data['media_id'],))
        row = c.fetchone()
        assert row[1] == 'Updated Title'

def test_save_media(media_access):
    """Test saving a media item"""
    media_data = {
        'media_id': 139470659,
        'title': 'Shape of You',
        'rating': 3,
        'duration': 233,
        'genre': 'Unknown',
        'year': 'Unknown',
        'cover_url': 'https://api.deezer.com/album/6120887/image'
    }
    
    # Create media item
    media = MediaItem(**media_data)
    
    # Save media
    result = media_access.save(media)
    assert result == media_data['media_id']
    
    # Verify media was saved
    saved_media = media_access.get_media(media_data['media_id'])
    assert saved_media is not None
    assert saved_media.title == media_data['title']
    assert saved_media.rating == media_data['rating']

def test_get_media(media_access):
    """Test retrieving a media item"""
    # First save a media item
    media_data = {
        'media_id': 139470659,
        'title': 'Shape of You',
        'rating': 3,
        'duration': 233,
        'genre': 'Unknown',
        'year': 'Unknown',
        'cover_url': 'https://api.deezer.com/album/6120887/image'
    }
    media = MediaItem(**media_data)
    media_access.save(media)
    
    # Get the media
    retrieved_media = media_access.get_media(media_data[''])
    assert retrieved_media is not None
    assert retrieved_media.title == media_data['title']
    assert retrieved_media.rating == media_data['rating']

def test_get_all_media(media_access):
    """Test retrieving all media items"""
    # Save multiple media items
    media_items = [
        {
            'media_id': 1,
            'title': 'Media 1',
            'rating': 5,
            'duration': 180,
            'genre': 'Genre 1',
            'year': '2023',
            'cover_url': 'http://test.com/cover1.jpg'
        },
        {
            'media_id': 2,
            'title': 'Media 2',
            'rating': 4,
            'duration': 200,
            'genre': 'Genre 2',
            'year': '2023',
            'cover_url': 'http://test.com/cover2.jpg'
        }
    ]
    
    for media_data in media_items:
        media = MediaItem(**media_data)
        media_access.save(media)
    
    # Get all media
    all_media = media_access.get_all_media()
    assert len(all_media) == len(media_items)
    assert all_media[0].title == media_items[0]['title']
    assert all_media[1].title == media_items[1]['title']

def test_delete_media(media_access):
    """Test deleting a media item"""
    # First save a media item
    media_data = {
        'media_id': 1,
        'title': 'Test Media',
        'rating': 5,
        'duration': 180,
        'genre': 'Test Genre',
        'year': '2023',
        'cover_url': 'http://test.com/cover.jpg'
    }
    media = MediaItem(**media_data)
    media_access.save(media)
    
    # Delete the media
    media_access.delete(media_data['media_id'])
    
    # Verify deletion
    deleted_media = media_access.get_media(media_data['media_id'])
    assert deleted_media is None 