import tkinter as tk
import font_manager as fonts


class UpdateTracks():
    def __init__(self, window):
        window.title("Update Tracks")
        window.geometry("400x200")

        tk.Label(window, text="Track ID:").pack(pady=5)
        track_entry = tk.Entry(window, width=5)
        track_entry.pack(pady=5)

        tk.Label(window, text="New Rating (1-5):").pack(pady=5)
        rating_entry = tk.Entry(window, width=5)
        rating_entry.pack(pady=5)

        tk.Button(window, text="Update Track").pack(pady=10)


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    UpdateTracks(window)
    window.mainloop()


