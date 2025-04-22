import requests
from Model import SongItem
from tkinter import messagebox
from Access import SongAccess
from Access import MediaItemAccess


class SongAPISync:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_host = "deezerdevs-deezer.p.rapidapi.com"
        self.base_url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        self.media_access = MediaItemAccess()
        self.song_access = SongAccess()

    def search_song(self, title):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        params = {"q": title}

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if not data:
                    messagebox.showwarning("No Results", "No songs found for the given title.")
                return data
            else:
                messagebox.showerror("API Error", f"Failed to search songs. Status code: {response.status_code}")
                return []
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to API: {str(e)}")
            return []

    def parse_song(self, song_data):
        try:
            song_id = int(song_data["id"])
            title = song_data["title"]
            album = song_data["album"]["title"]
            artist = song_data["artist"]["name"]
            rating = 4
            duration = song_data["duration"]
            genre = song_data.get("genre", "Unknown")
            year = song_data.get("release_date", "Unknown")
            cover_url = song_data["album"]["cover"]
            
            return SongItem(
                song_id=song_id,
                media_id=song_id,
                title=title,
                artist=artist,
                rating=rating,
                album=album,
                count_play=0,
                duration=duration,
                genre=genre,
                year=year,
                cover_url=cover_url
            )
        except Exception as e:
            messagebox.showerror("Parsing Error", f"Failed to parse song data: {str(e)}")
            return None

    def save_song(self, song_data):
        """Save a song and its media to the database"""
        try:
            # Check if song already exists
            if self.song_access.check_exist(song_data['id']):
                messagebox.showinfo("Exists", f"'{song_data['title']}' already exists in the database.")
                return None

            # Create a SongItem object
            song_item = self.parse_song(song_data)
            if not song_item:
                messagebox.showerror("Error", "Failed to parse song data")
                return None
            
            # Save the song
            song_id = self.song_access.save(song_item)

            if song_id:
                # Then save the media information using media_access
                media_id = self.media_access.save({
                    "media_id": song_data['id'],
                    "title": song_data['title'],
                    "rating": 0,  # Default rating
                    "duration": song_data['duration'],
                    "genre": song_data.get('genre', 'Unknown'),
                    "year": song_data.get('release_date', 'Unknown'),
                    "cover_url": song_data['album']['cover']
                })

                if media_id:
                    messagebox.showinfo("Success", f"Successfully saved song: {song_data['title']}")
                    return song_id
                else:
                    # If media save fails, delete the song
                    self.song_access.delete_song(song_id)
                    messagebox.showerror("Error", "Failed to save media information")
                    return None
            else:
                messagebox.showerror("Error", "Failed to save song information")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save song: {str(e)}")
            return None

