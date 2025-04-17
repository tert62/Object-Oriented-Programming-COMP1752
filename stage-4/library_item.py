import csv
import os

DATA_FILE = "tracks_data.csv"

class LibraryItem:
    def __init__(self, track_id, name, artist, rating, play_count=0, image_path=""):
        self.track_id = track_id
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = play_count
        self.image_path = image_path

    def get_details(self):
        return f"{self.track_id}: {self.name} - {self.artist} (Rating: {self.rating}) [Played: {self.play_count} times]"

    def set_rating(self, new_rating):
        if not isinstance(new_rating, int) or not (1 <= new_rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = new_rating

    def increment_play_count(self):
        self.play_count += 1

class LibraryItemAlbum(LibraryItem):
    def __init__(self, track_id, name, artist, rating, play_count=0, image_path="", album="", release_year=0, genre="", track_number=0):
        super().__init__(track_id, name, artist, rating, play_count, image_path)
        self.album = album  
        self.release_year = release_year  
        self.genre = genre
        self.track_number = track_number

    def get_details(self):
        return (f"{self.track_id}: {self.name} - {self.artist} (Album: {self.album}, Track {self.track_number}) "
                f"(Rating: {self.rating}) [Played: {self.play_count} times]")

    def get_album_info(self):
        return f"Album: {self.album}, Released: {self.release_year}, Genre: {self.genre}"

class TrackLibrary:
    def __init__(self):
        self.tracks = self.load_tracks()

    def load_tracks(self):
        tracks = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        track_id = int(row["Track ID"])
                        name = row["Name"]
                        artist = row["Artist"]
                        rating = int(row["Rating"])
                        play_count = int(row["Play Count"])
                        image_path = row["Image Path"].strip() if "Image Path" in row else ""
                        album = row["Album"].strip() if "Album" in row else ""
                        release_year = int(row["Release Year"]) if row["Release Year"].isdigit() else 0
                        genre = row["Genre"].strip() if "Genre" in row else ""
                        track_number = int(row["Track Number"]) if row["Track Number"].isdigit() else 0

                        if album:  
                            tracks.append(LibraryItemAlbum(track_id, name, artist, rating, play_count, image_path, album, release_year, genre, track_number))
                        else:  
                            tracks.append(LibraryItem(track_id, name, artist, rating, play_count, image_path))
                    except ValueError:
                        print(f"Skipping invalid row: {row}")
        return tracks

    def save_tracks(self):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Track ID", "Name", "Artist", "Rating", "Play Count", "Image Path", "Album", "Release Year", "Genre", "Track Number"])
            writer.writeheader()
            for track in self.tracks:
                writer.writerow({
                    "Track ID": track.track_id,
                    "Name": track.name,
                    "Artist": track.artist,
                    "Rating": track.rating,
                    "Play Count": track.play_count,
                    "Image Path": track.image_path,
                    "Album": track.album if isinstance(track, LibraryItemAlbum) else "",
                    "Release Year": track.release_year if isinstance(track, LibraryItemAlbum) else "",
                    "Genre": track.genre if isinstance(track, LibraryItemAlbum) else "",
                    "Track Number": track.track_number if isinstance(track, LibraryItemAlbum) else ""
                })

    def list_all(self):
        return self.tracks

    def get_track_by_id(self, track_id):
        return next((track for track in self.tracks if track.track_id == track_id), None)

    def add_track(self, track):
        self.tracks.append(track)
        self.save_tracks()

    def remove_track(self, track_id):
        track = self.get_track_by_id(track_id)
        if track:
            self.tracks.remove(track)
            self.save_tracks()
        else:
            print(f"Track with ID {track_id} not found.")

