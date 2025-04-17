import tkinter as tk  # Import tkinter for GUI elements
import tkinter.scrolledtext as tkst  # Import scrolled text widget for text display
import track_library as lib  # Import track_library module to handle track data
import font_manager as fonts  # Import font_manager module to manage fonts


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)  # Clear existing content
    text_area.insert(1.0, content)  # Insert new content at the beginning


class TrackViewer():

    def __init__(self, window):
        window.geometry("750x350")  # Set window size
        window.title("View Tracks")  # Set window title

        # Button to list all tracks
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        # Label prompting user to enter a track number
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        # Entry field for user to input a track number
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        # Button to view details of a specific track
        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)

        # Scrolled text area for displaying the list of tracks
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Text widget for displaying individual track details
        self.track_txt = tk.Text(window, width=24, height=4, wrap="none")
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        # Label to display status messages
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Automatically list all tracks on startup
        self.list_tracks_clicked()

    def view_tracks_clicked(self):
        key = self.input_txt.get()  # Get user input from entry field
        name = lib.get_name(key)  # Retrieve track name from the library

        if name is not None:  # If track exists
            artist = lib.get_artist(key)  # Retrieve artist name
            rating = lib.get_rating(key)  # Retrieve track rating
            play_count = lib.get_play_count(key)  # Retrieve play count

            # Format track details
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}"
            set_text(self.track_txt, track_details)  # Display track details
        else:
            set_text(self.track_txt, f"Track {key} not found")  # Display error message

        self.status_lbl.configure(text="View Track button was clicked!")  # Update status label

    def list_tracks_clicked(self):
        track_list = lib.list_all()  # Get a formatted list of all tracks
        set_text(self.list_txt, track_list)  # Display track list in text area

        self.status_lbl.configure(text="List Tracks button was clicked!")  # Update status label


if __name__ == "__main__":
    window = tk.Tk()  # Create the main Tkinter window
    fonts.configure()  # Configure the fonts before launching GUI
    TrackViewer(window)  # Create an instance of TrackViewer
    window.mainloop()  # Run the Tkinter event loop


