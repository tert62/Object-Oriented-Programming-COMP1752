import tkinter as tk
from tkinter import messagebox
from track_library import get_name, get_play_count, increment_play_count
import font_manager as fonts

class CreateTrackList():

    def __init__(self, window):
        window.title("Create Track List")
        window.geometry("500x350")

        tk.Label(window, text="Enter Track Number(s) (separated by space):").pack(pady=5)
        self.track_entry = tk.Entry(window, width=30)
        self.track_entry.pack(pady=5)

        tk.Button(window, text="Add to Playlist", command=self.add_to_playlist).pack(pady=5)

        self.playlist_text = tk.Text(window, width=50, height=10, state="disabled")
        self.playlist_text.pack(pady=10)

        tk.Button(window, text="Play Playlist", command=self.play_playlist).pack(pady=5)
        tk.Button(window, text="Reset Playlist", command=self.reset_playlist).pack(pady=5)

        self.playlist = []

    def add_to_playlist(self):
        track_ids = self.track_entry.get().split()
        unique_track_ids = set()
        added_tracks = []
 
        for track_id in track_ids:
            if not track_id.isdigit():
                messagebox.showerror("Error", "Track ID must be a number!")
                return

            track_id = track_id.zfill(2)

            if track_id in unique_track_ids:
                messagebox.showerror("Error", f"Duplicate track ID detected: {track_id}")
                return

            unique_track_ids.add(track_id)
            track_name = get_name(track_id)

            if track_name and track_id not in self.playlist:
                self.playlist.append(track_id)
                added_tracks.append(f"{track_id} - {track_name}")

        if added_tracks:
            self.update_playlist_display()
        else:
            messagebox.showerror("Error", "Invalid or duplicate track(s)!")

    def update_playlist_display(self):
        self.playlist_text.config(state="normal")
        
        self.playlist_text.delete(1.0, tk.END)
        for track_id in self.playlist:
            track_name = get_name(track_id)
            play_count = get_play_count(track_id)
            self.playlist_text.insert(tk.END, f"{track_id} - {track_name} (Played: {play_count} times)\n")
        self.playlist_text.config(state="disabled")

    def play_playlist(self):
        if not self.playlist:
            messagebox.showerror("Error", "No tracks in the playlist!")
            return

        for track_id in self.playlist:
            increment_play_count(track_id)
        self.update_playlist_display()
        messagebox.showinfo("Play Playlist", "All tracks played successfully!")

    def reset_playlist(self):
        self.playlist = []
        self.update_playlist_display()

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateTrackList(window)
    window.mainloop()


    