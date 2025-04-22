import pytest
from Model import MediaItem

def test_media_item_initialization():
    """Test that a MediaItem is initialized with correct attributes"""
    title = "Test Title"
    rating = 4
    media = MediaItem(title, rating)
    
    assert media.title == title
    assert media.rating == rating

def test_media_item_info():
    """Test that info() method returns correct string representation"""
    title = "Test Title"
    rating = 4
    media = MediaItem(title, rating)
    
    expected = f"{title} {rating}"
    assert media.info() == expected 