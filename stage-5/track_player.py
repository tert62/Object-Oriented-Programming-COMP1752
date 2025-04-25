import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from library_item import TrackLibrary
import os
import csv
import datetime

PLAYLIST_FOLDER = "playlists"
IMAGE_FOLDER = "images"

# Create folders if they don't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

if not os.path.exists(PLAYLIST_FOLDER):
    os.makedirs(PLAYLIST_FOLDER)

class TrackPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JukeBox")
        self.root.geometry("1050x620")
        self.root.configure(bg="#ffffff")  # Light background for a clean look

        # Apply a modern theme
        self.style = ttk.Style(self.root)
        self.style.theme_use("arc")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("TLabel", font=("Arial", 11))

        # Initialize track library and playlist management
        self.track_library = TrackLibrary()
        self.playlists = {}
        self.current_playlist_name = None

        self.load_all_playlists()

        # Create the notebook (tabbed interface)
        self.create_notebook()

        # Automatically display all tracks when app starts
        self.view_tracks()

    def load_all_playlists(self):
        for filename in os.listdir(PLAYLIST_FOLDER):
            if filename.endswith(".csv"):
                playlist_name = filename[:-4]
                self.playlists[playlist_name] = []
                playlist_file = os.path.join(PLAYLIST_FOLDER, filename)
                with open(playlist_file, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        track_id = int(row[0])
                        track = self.track_library.get_track_by_id(track_id)
                        if track:
                            self.playlists[playlist_name].append(track)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)  # Add padding

        self.create_main_tab()
        self.create_playlist_tab()

    def create_main_tab(self):
        main_frame = ttk.Frame(self.notebook, padding=10)  # Add padding to frame
        self.notebook.add(main_frame, text="Main")

        # Top control panel for search and filter
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))

        self.search_entry = ttk.Entry(control_frame, width=30, font=("Arial", 11))
        self.search_entry.pack(side="left", padx=(0, 10))
        ttk.Button(control_frame, text="Search", command=self.search_tracks).pack(side="left", padx=5)

        self.artist_filter = ttk.Combobox(control_frame, values=["All"] + list(
            set(track.artist for track in self.track_library.list_all())), font=("Arial", 11))
        self.artist_filter.current(0)
        self.artist_filter.pack(side="left", padx=(10, 10))
        ttk.Button(control_frame, text="Filter", command=self.filter_by_artist).pack(side="left", padx=5)

        # Paned window for tracks and details
        self.paned_window = ttk.PanedWindow(main_frame, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)

        left_frame = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(left_frame, weight=1)

        self.right_frame = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.right_frame, weight=3)

        # Scrollable canvas for tracks
        self.canvas = tk.Canvas(left_frame, bg="#f5f5f5", highlightthickness=0)  # Softer background
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.tracks_display_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.tracks_display_frame, anchor="nw")

    def create_playlist_tab(self):
        playlist_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(playlist_frame, text="Playlist")

        # Management frame with better spacing
        management_frame = ttk.Frame(playlist_frame)
        management_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(management_frame, text="Playlist Name:", font=("Arial", 11, "bold")).pack(side="left", padx=(0, 5))
        self.playlist_name_entry = ttk.Entry(management_frame, width=20, font=("Arial", 11))
        self.playlist_name_entry.pack(side="left", padx=5)

        ttk.Button(management_frame, text="Create Playlist", command=self.create_playlist).pack(side="left", padx=5)
        ttk.Button(management_frame, text="Delete Playlist", command=self.delete_playlist).pack(side="left", padx=5)

        self.playlist_combobox = ttk.Combobox(management_frame, state="readonly", width=20, font=("Arial", 11))
        self.playlist_combobox.pack(side="left", padx=10)
        self.update_playlist_combobox()

        ttk.Button(management_frame, text="Select Playlist", command=self.select_playlist).pack(side="left", padx=5)

        # Scrollable canvas for playlist tracks
        self.playlist_canvas = tk.Canvas(playlist_frame, bg="#f5f5f5", highlightthickness=0)
        self.playlist_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.playlist_canvas, orient="vertical", command=self.playlist_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.playlist_canvas.configure(yscrollcommand=scrollbar.set)
        self.playlist_canvas.bind("<Configure>", lambda e: self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox("all")))

        self.playlist_tracks_frame = ttk.Frame(self.playlist_canvas)
        self.playlist_canvas.create_window((0, 0), window=self.playlist_tracks_frame, anchor="nw")

        # Button frame with consistent spacing
        button_frame = ttk.Frame(playlist_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Play Playlist", command=self.play_playlist).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset Playlist", command=self.reset_playlist).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load Playlist", command=self.load_playlist).pack(side="left", padx=5)

        # Sorting controls with better alignment
        sort_frame = ttk.Frame(playlist_frame)
        sort_frame.pack(fill="x", pady=5)

        ttk.Label(sort_frame, text="Sort by:", font=("Arial", 11)).pack(side="left", padx=(0, 5))
        self.sort_criteria = tk.StringVar(value="name")
        sort_options = ["name", "artist", "rating", "play_count"]
        self.sort_dropdown = ttk.Combobox(sort_frame, textvariable=self.sort_criteria, values=sort_options, font=("Arial", 11))
        self.sort_dropdown.pack(side="left", padx=5)
        ttk.Button(sort_frame, text="Sort Playlist", command=self.sort_playlist).pack(side="left", padx=5)

    def create_playlist(self):
        playlist_name = self.playlist_name_entry.get().strip()
        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name!")
            return

        if playlist_name in self.playlists:
            messagebox.showerror("Error", "Playlist already exists!")
            return

        self.playlists[playlist_name] = []

        playlist_file = os.path.join(PLAYLIST_FOLDER, f"{playlist_name}.csv")
        try:
            with open(playlist_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Track ID", "Name", "Artist"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create playlist file: {e}")
            del self.playlists[playlist_name]
            return

        self.update_playlist_combobox()
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
        
        self.playlist_name_entry.delete(0, tk.END)
        self.current_playlist_name = playlist_name
        self.playlist_combobox.set(playlist_name)
        self.update_playlist_display()

    def delete_playlist(self):
        playlist_name = self.playlist_combobox.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please select a playlist to delete!")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete playlist '{playlist_name}'?"):
            return

        try:
            playlist_file = os.path.join(PLAYLIST_FOLDER, f"{playlist_name}.csv")
            if os.path.exists(playlist_file):
                os.remove(playlist_file)

            del self.playlists[playlist_name]
            if self.current_playlist_name == playlist_name:
                self.current_playlist_name = None
                self.update_playlist_display()
            
            self.update_playlist_combobox()
            self.playlist_combobox.set('')
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete playlist: {e}")

    def update_playlist_combobox(self):
        # Reload all playlists from folder to ensure we have the latest data
        self.load_all_playlists()
        self.playlist_combobox['values'] = list(self.playlists.keys())
        if self.current_playlist_name and self.current_playlist_name in self.playlists:
            self.playlist_combobox.set(self.current_playlist_name)
        else:
            self.playlist_combobox.set('')

    def select_playlist(self):
        self.playlist_name_entry.delete(0, tk.END)
        playlist_name = self.playlist_combobox.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please select a playlist!")
            return

        self.current_playlist_name = playlist_name
        self.update_playlist_display()

    def view_tracks(self):
        for widget in self.tracks_display_frame.winfo_children():
            widget.destroy()

        for track in self.track_library.list_all():
            track_frame = ttk.Frame(self.tracks_display_frame, padding=5, relief="flat", borderwidth=1)
            track_frame.pack(pady=5, fill="x")

            if hasattr(track, "image_path") and track.image_path and os.path.exists(track.image_path):
                try:
                    img = Image.open(track.image_path).resize((80, 80), Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    image_label = ttk.Label(track_frame, image=img_tk)
                    image_label.image = img_tk
                    image_label.pack(side="left", padx=10)
                except Exception as e:
                    print(f"Error loading image {track.image_path}: {e}")
                    ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)
            else:
                ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)

            info_frame = ttk.Frame(track_frame)
            info_frame.pack(side="left", fill="x", expand=True)

            ttk.Label(info_frame, text=f"{track.name}", font=("Arial", 13, "bold")).pack(anchor="w")
            ttk.Label(info_frame, text=f"by {track.artist}", font=("Arial", 11)).pack(anchor="w")

            track_frame.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))
            for child in track_frame.winfo_children():
                child.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))

        self.tracks_display_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_track_details(self, track):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        details_container = ttk.Frame(self.right_frame, padding=10, relief="flat")
        details_container.pack(fill="both", expand=True)

        if hasattr(track, "image_path") and track.image_path and os.path.exists(track.image_path):
            try:
                img = Image.open(track.image_path).resize((150, 150), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_label = ttk.Label(details_container, image=img_tk)
                image_label.image = img_tk
                image_label.pack(pady=(0, 10))
            except Exception as e:
                print(f"Error loading image {track.image_path}: {e}")
                ttk.Label(details_container, text="No Image", font=("Arial", 10)).pack(pady=(0, 10))
        else:
            ttk.Label(details_container, text="No Image", font=("Arial", 10)).pack(pady=(0, 10))

        details_frame = ttk.Frame(details_container)
        details_frame.pack(pady=10, fill="x")

        ttk.Label(details_frame, text=f"{track.name}", font=("Arial", 16, "bold")).pack(anchor="w")
        ttk.Label(details_frame, text=f"Artist: {track.artist}", font=("Arial", 12)).pack(anchor="w")
        ttk.Label(details_frame, text=f"Rating: {track.rating}/5", font=("Arial", 12)).pack(anchor="w")
        ttk.Label(details_frame, text=f"Play Count: {track.play_count}", font=("Arial", 12)).pack(anchor="w")

        if hasattr(track, "album") and track.album:
            ttk.Label(details_frame, text=f"Album: {track.album}", font=("Arial", 12)).pack(anchor="w")
        if hasattr(track, "release_year") and track.release_year:
            ttk.Label(details_frame, text=f"Year: {track.release_year}", font=("Arial", 12)).pack(anchor="w")
        if hasattr(track, "genre") and track.genre:
            ttk.Label(details_frame, text=f"Genre: {track.genre}", font=("Arial", 12)).pack(anchor="w")

        button_frame = ttk.Frame(details_container)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Play", command=lambda: self.play_track(track)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add to Playlist", command=lambda: self.add_to_playlist(track)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Track", command=lambda: self.edit_track(track)).pack(side="left", padx=5)

    def play_track(self, track):
        track.increment_play_count()
        self.track_library.save_tracks()
        self.show_track_details(track)
        messagebox.showinfo("Play Track", f"Playing: {track.name}")

    def add_to_playlist(self, track):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add to Playlist")
        add_window.geometry("400x250")
        add_window.configure(bg="#ffffff")

        self.use_existing_playlist = tk.BooleanVar(value=True)
        
        control_frame = ttk.Frame(add_window, padding=20)
        control_frame.pack(fill="x")

        ttk.Radiobutton(control_frame, text="Select existing playlist:", variable=self.use_existing_playlist, 
                        value=True, command=lambda: self.toggle_playlist_entries(playlist_combobox, new_playlist_entry)).pack(anchor="w")
        playlist_combobox = ttk.Combobox(control_frame, values=list(self.playlists.keys()), state="readonly", font=("Arial", 11))
        playlist_combobox.pack(fill="x", pady=5)

        ttk.Radiobutton(control_frame, text="Create new playlist:", variable=self.use_existing_playlist, 
                        value=False, command=lambda: self.toggle_playlist_entries(playlist_combobox, new_playlist_entry)).pack(anchor="w", pady=(10, 0))
        new_playlist_entry = ttk.Entry(control_frame, font=("Arial", 11))
        new_playlist_entry.pack(fill="x", pady=5)
        new_playlist_entry.config(state='disabled')

        ttk.Label(control_frame, text=f"Track: {track.name} - {track.artist}", font=('Arial', 10, "italic")).pack(anchor="w", pady=(10, 0))

        button_frame = ttk.Frame(add_window, padding=10)
        button_frame.pack(fill="x")

        def handle_add():
            if self.use_existing_playlist.get():
                selected_playlist = playlist_combobox.get()
                if not selected_playlist:
                    messagebox.showerror("Error", "Please select a playlist!")
                    return
            else:
                new_playlist_name = new_playlist_entry.get().strip()
                if not new_playlist_name:
                    messagebox.showerror("Error", "Please enter new playlist name!")
                    return
                if new_playlist_name in self.playlists:
                    messagebox.showerror("Error", "Playlist already exists!")
                    return
                self.playlists[new_playlist_name] = []
                selected_playlist = new_playlist_name
            
            if track in self.playlists[selected_playlist]:
                messagebox.showwarning("Warning", f"'{track.name}' is already in playlist '{selected_playlist}'")
                add_window.destroy()
                return
            
            self.playlists[selected_playlist].append(track)
            self.save_playlist_to_file(selected_playlist)
            
            # Update combobox and select the new playlist
            self.update_playlist_combobox()
            self.current_playlist_name = selected_playlist
            self.playlist_combobox.set(selected_playlist)
            self.update_playlist_display()
            
            messagebox.showinfo("Success", f"Added '{track.name}' to playlist '{selected_playlist}'")
            add_window.destroy()
        
        ttk.Button(button_frame, text="Add", command=handle_add).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left", padx=5)

    def toggle_playlist_entries(self, combobox, entry):
        if self.use_existing_playlist.get():
            combobox.config(state='readonly')
            entry.config(state='disabled')
        else:
            combobox.config(state='disabled')
            entry.config(state='normal')

    def save_playlist_to_file(self, playlist_name):
        playlist_file = os.path.join(PLAYLIST_FOLDER, f"{playlist_name}.csv")
        try:
            with open(playlist_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Track ID", "Name", "Artist"])
                for track in self.playlists[playlist_name]:
                    writer.writerow([track.track_id, track.name, track.artist])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save playlist: {e}")

    def edit_track(self, track):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Track")
        edit_window.geometry("400x350")
        edit_window.configure(bg="#ffffff")
        edit_window.grab_set()

        form_frame = ttk.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        entry_vars = {}
        entries = {}
        required_fields = ["Title:", "Artist:"]
        
        fields = [
            ("Title:", track.name),
            ("Artist:", track.artist),
            ("Album:", getattr(track, "album", "")),
            ("Release Year:", getattr(track, "release_year", "")),
            ("Genre:", getattr(track, "genre", "")),
            ("Rating (1-5):", str(track.rating))
        ]

        for i, (label, value) in enumerate(fields):
            ttk.Label(form_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if label in required_fields:
                ttk.Label(form_frame, text="*", foreground="red").grid(row=i, column=0, padx=(0,5), sticky="e")
            
            var = tk.StringVar(value=value)
            entry_vars[label] = var
            
            if label == "Rating (1-5):":
                entry = ttk.Combobox(form_frame, textvariable=var, 
                                    values=[1, 2, 3, 4, 5], 
                                    state="readonly", 
                                    font=("Arial", 11))
            else:
                entry = ttk.Entry(form_frame, textvariable=var, width=30, font=("Arial", 11))
            
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def save_changes():
            errors = []
            # Validate required fields
            for field in required_fields:
                if not entry_vars[field].get().strip():
                    errors.append(f"{field} is required")
                    entries[field].config(style="Error.TEntry")
                else:
                    entries[field].config(style="TEntry")
            
            # Validate release year
            release_year = entry_vars["Release Year:"].get().strip()
            if release_year:  # Only validate if not empty
                try:
                    year = int(release_year)
                    current_year = datetime.datetime.now().year
                    if year < 1900 or year > current_year:
                        errors.append(f"Release year must be between 1900 and {current_year}")
                except ValueError:
                    errors.append("Release year must be a valid number")
            
            if errors:
                messagebox.showerror("Error", "\n".join(errors))
                return

            # All validations passed - save changes
            track.name = entry_vars["Title:"].get().strip()
            track.artist = entry_vars["Artist:"].get().strip()
            track.album = entry_vars["Album:"].get().strip()
            track.release_year = entry_vars["Release Year:"].get().strip()
            track.genre = entry_vars["Genre:"].get().strip()
            track.rating = int(entry_vars["Rating (1-5):"].get())

            self.track_library.save_tracks()
            self.show_track_details(track)
            edit_window.destroy()
            messagebox.showinfo("Edit Track", "Track updated successfully!")

        ttk.Button(form_frame, text="Save", command=save_changes).grid(row=len(fields), column=1, pady=10, sticky="e")

    def update_playlist_display(self):
        for widget in self.playlist_tracks_frame.winfo_children():
            widget.destroy()

        if not self.current_playlist_name:
            return

        for track in self.playlists[self.current_playlist_name]:
            track_frame = ttk.Frame(self.playlist_tracks_frame, padding=5, relief="flat", borderwidth=1)
            track_frame.pack(pady=5, fill="x")

            if hasattr(track, "image_path") and track.image_path and os.path.exists(track.image_path):
                try:
                    img = Image.open(track.image_path).resize((80, 80), Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    image_label = ttk.Label(track_frame, image=img_tk)
                    image_label.image = img_tk
                    image_label.pack(side="left", padx=10)
                except Exception as e:
                    print(f"Error loading image {track.image_path}: {e}")
                    ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)
            else:
                ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)

            info_frame = ttk.Frame(track_frame)
            info_frame.pack(side="left", fill="x", expand=True)

            ttk.Label(info_frame, text=f"{track.name}", font=("Arial", 13, "bold")).pack(anchor="w")
            ttk.Label(info_frame, text=f"by {track.artist}", font=("Arial", 11)).pack(anchor="w")

            button_frame = ttk.Frame(track_frame)
            button_frame.pack(side="right", padx=10)

            ttk.Button(button_frame, text="Play", command=lambda t=track: self.play_track(t)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Remove", command=lambda t=track: self.remove_from_playlist(t)).pack(side="left", padx=5)

        self.playlist_tracks_frame.update_idletasks()
        self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox("all"))

    def play_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected!")
            return

        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            messagebox.showerror("Error", "The playlist is empty!")
            return

        for track in playlist:
            track.increment_play_count()

        self.track_library.save_tracks()
        self.update_playlist_display()
        messagebox.showinfo("Play Playlist", "All tracks in the playlist have been played.")

    def reset_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected!")
            return

        self.playlists[self.current_playlist_name] = []
        self.update_playlist_display()

    def load_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected!")
            return

        playlist_file = os.path.join(PLAYLIST_FOLDER, f"{self.current_playlist_name}.csv")
        if not os.path.exists(playlist_file):
            messagebox.showerror("Error", "No playlist file found!")
            return

        self.playlists[self.current_playlist_name] = []
        with open(playlist_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                track_id = int(row[0])
                track = self.track_library.get_track_by_id(track_id)
                if track:
                    self.playlists[self.current_playlist_name].append(track)

        self.update_playlist_display()

    def remove_from_playlist(self, track):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected!")
            return

        if track in self.playlists[self.current_playlist_name]:
            self.playlists[self.current_playlist_name].remove(track)
            self.update_playlist_display()
            self.save_playlist_to_file(self.current_playlist_name)
            messagebox.showinfo("Remove from Playlist", f"{track.name} has been removed from the playlist.")
        else:
            messagebox.showinfo("Remove from Playlist", f"{track.name} is not in the playlist.")

    def sort_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected!")
            return

        criteria = self.sort_criteria.get()
        playlist = self.playlists[self.current_playlist_name]
        if not playlist:
            messagebox.showwarning("Warning", "The playlist is empty!")
            return

        if criteria == "name":
            playlist.sort(key=lambda x: x.name)
        elif criteria == "artist":
            playlist.sort(key=lambda x: x.artist)
        elif criteria == "rating":
            playlist.sort(key=lambda x: x.rating, reverse=True)
        elif criteria == "play_count":
            playlist.sort(key=lambda x: x.play_count, reverse=True)
        else:
            messagebox.showerror("Error", "Invalid sorting criteria!")
            return

        self.update_playlist_display()

    def search_tracks(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Error", "Please enter a search term!")
            return

        self.artist_filter.set("All")
        results = [track for track in self.track_library.list_all() if
                   query in track.name.lower() or query in track.artist.lower()]

        for widget in self.tracks_display_frame.winfo_children():
            widget.destroy()

        if results:
            for track in results:
                track_frame = ttk.Frame(self.tracks_display_frame, padding=5, relief="flat", borderwidth=1)
                track_frame.pack(pady=5, fill="x")

                if hasattr(track, "image_path") and track.image_path and os.path.exists(track.image_path):
                    try:
                        img = Image.open(track.image_path).resize((80, 80), Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        image_label = ttk.Label(track_frame, image=img_tk)
                        image_label.image = img_tk
                        image_label.pack(side="left", padx=10)
                    except Exception as e:
                        print(f"Error loading image {track.image_path}: {e}")
                        ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)
                else:
                    ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)

                info_frame = ttk.Frame(track_frame)
                info_frame.pack(side="left", fill="x", expand=True)

                ttk.Label(info_frame, text=f"{track.name}", font=("Arial", 13, "bold")).pack(anchor="w")
                ttk.Label(info_frame, text=f"by {track.artist}", font=("Arial", 11)).pack(anchor="w")

                track_frame.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))
                for child in track_frame.winfo_children():
                    child.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))
        else:
            messagebox.showerror("Error", "No tracks found!")

        self.tracks_display_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def filter_by_artist(self):
        self.search_entry.delete(0, tk.END)
        selected_artist = self.artist_filter.get()

        for widget in self.tracks_display_frame.winfo_children():
            widget.destroy()

        if selected_artist == "All":
            self.view_tracks()
        else:
            filtered_tracks = [track for track in self.track_library.list_all() if track.artist == selected_artist]
            if filtered_tracks:
                for track in filtered_tracks:
                    track_frame = ttk.Frame(self.tracks_display_frame, padding=5, relief="flat", borderwidth=1)
                    track_frame.pack(pady=5, fill="x")

                    if hasattr(track, "image_path") and track.image_path and os.path.exists(track.image_path):
                        try:
                            img = Image.open(track.image_path).resize((80, 80), Image.Resampling.LANCZOS)
                            img_tk = ImageTk.PhotoImage(img)
                            image_label = ttk.Label(track_frame, image=img_tk)
                            image_label.image = img_tk
                            image_label.pack(side="left", padx=10)
                        except Exception as e:
                            print(f"Error loading image {track.image_path}: {e}")
                            ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)
                    else:
                        ttk.Label(track_frame, text="No Image", font=("Arial", 10)).pack(side="left", padx=10)

                    info_frame = ttk.Frame(track_frame)
                    info_frame.pack(side="left", fill="x", expand=True)

                    ttk.Label(info_frame, text=f"{track.name}", font=("Arial", 13, "bold")).pack(anchor="w")
                    ttk.Label(info_frame, text=f"by {track.artist}", font=("Arial", 11)).pack(anchor="w")

                    track_frame.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))
                    for child in track_frame.winfo_children():
                        child.bind("<Button-1>", lambda e, t=track: self.show_track_details(t))
            else:
                messagebox.showerror("Error", f"No tracks found for artist: {selected_artist}")

        self.tracks_display_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = TrackPlayerGUI(root)
    root.mainloop()
