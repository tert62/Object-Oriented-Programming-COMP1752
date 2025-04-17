import tkinter as tk
from tkinter import messagebox
import font_manager as fonts
from track_library import get_name, get_rating, set_rating, get_play_count, increment_play_count

class UpdateTracks:
    def __init__(self, window):
        window.title("Update Tracks")
        window.geometry("400x250")

        tk.Label(window, text="Track ID:").pack(pady=5)
        self.track_entry = tk.Entry(window, width=10)
        self.track_entry.pack(pady=5)

        tk.Label(window, text="New Rating (1-5):").pack(pady=5)
        self.rating_entry = tk.Entry(window, width=10)
        self.rating_entry.pack(pady=5)

        tk.Button(window, text="Update Track", command=self.update_track).pack(pady=10)

    def update_track(self):
        track_id = self.track_entry.get().strip()
        new_rating = self.rating_entry.get().strip()

        if not track_id.isdigit():
            messagebox.showerror("Error", "Track ID must be a number!")
            return

        if not new_rating.isdigit() or not (1 <= int(new_rating) <= 5):
            messagebox.showerror("Error", "Rating must be a number between 1 and 5!")
            return

        if not get_name(track_id):
            messagebox.showerror("Error", "Invalid track ID!")
            return

        set_rating(track_id, int(new_rating))
        increment_play_count(track_id)

        track_name = get_name(track_id)
        play_count = get_play_count(track_id)

        messagebox.showinfo("Update Successful", f"Track Updated:\nName: {track_name}\nNew Rating: {new_rating}\nPlay Count: {play_count}")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    UpdateTracks(window)
    window.mainloop()

    