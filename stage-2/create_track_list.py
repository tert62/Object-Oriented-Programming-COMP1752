import tkinter as tk
import font_manager as fonts

class CreateTrackList():
    def __init__(self, window):
        window.title("Create Track List")
        window.geometry("500x350")

        tk.Label(window, text="Enter Track Number(s) (separated by space):").pack(pady=5)
        track_entry = tk.Entry(window, width=30)
        track_entry.pack(pady=5)

        tk.Button(window, text="Add to Playlist").pack(pady=5)

        playlist_text = tk.Text(window, width=50, height=10, state="disabled")
        playlist_text.pack(pady=10)

        tk.Button(window, text="Play Playlist").pack(pady=5)
        tk.Button(window, text="Reset Playlist").pack(pady=5)

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateTrackList(window)
    window.mainloop()

    