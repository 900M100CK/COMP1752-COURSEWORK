class MediaItem:
    """
    Base class for media items in the jukebox application.
    Provides common attributes and methods for all media types.
    """
    def __init__(self, title, rating):
        """
        Initialize a media item with basic information

        Args:
            title (str): Title of the media item
            rating (int): User rating of the media item (1-5)
        """
        # Basic media information
        self.title = title
        self.rating = rating

    def info(self):
        return f"{self.title} {self.rating}"
