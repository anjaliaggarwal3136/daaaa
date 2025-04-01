import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime

class Song:
    def __init__(self, title, artist, genre, duration, release_year):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.duration = duration
        self.release_year = int(release_year)  # Store as integer for proper sorting

class PlaylistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personalized Playlist Manager")
        self.playlist = []
        # Pre-fill the playlist with some Bollywood songs
        self.populate_initial_playlist()
        # Create GUI elements
        self.create_widgets()

    def populate_initial_playlist(self):
        self.playlist.append(Song("Tum Hi Ho", "Arijit Singh", "Romantic", "4:22", 2013))
        self.playlist.append(Song("Tera Ban Jaunga", "Akhil Sachdeva & Tulsi Kumar", "Romantic", "3:56", 2019))
        self.playlist.append(Song("Kala Chashma", "Badshah & Neha Kakkar", "Party", "3:06", 2016))
        self.playlist.append(Song("Channa Mereya", "Arijit Singh", "Romantic", "5:24", 2016))
        self.playlist.append(Song("Kabira", "Amit Trivedi", "Romantic", "4:18", 2013))

    def create_widgets(self):
        self.add_button = tk.Button(self.root, text="Add Song", command=self.add_song)
        self.add_button.pack(pady=10)

        self.show_button = tk.Button(self.root, text="Show Playlist", command=self.show_playlist)
        self.show_button.pack(pady=10)

        self.sort_button = tk.Button(self.root, text="Sort Playlist", command=self.sort_playlist)
        self.sort_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Playlist", command=self.save_playlist)
        self.save_button.pack(pady=10)

        self.display_area = scrolledtext.ScrolledText(self.root, width=50, height=15, wrap=tk.WORD)
        self.display_area.pack(pady=10)

    def add_song(self):
        title = simpledialog.askstring("Input", "Enter the song title:")
        artist = simpledialog.askstring("Input", "Enter the artist(s):")
        genre = simpledialog.askstring("Input", "Enter the genre:")
        duration = simpledialog.askstring("Input", "Enter the duration (mm:ss):")
        release_year = simpledialog.askstring("Input", "Enter the release year:")

        if self.validate_inputs(title, artist, genre, duration, release_year):
            self.playlist.append(Song(title, artist, genre, duration, int(release_year)))
            messagebox.showinfo("Success", f"Added '{title}' to the playlist.")
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def validate_inputs(self, title, artist, genre, duration, release_year):
        if not title or not artist or not genre or not duration or not release_year:
            return False
        
        parts = duration.split(":")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            return False
        
        try:
            year = int(release_year)
            if year < 0 or year > datetime.datetime.now().year:
                return False
        except ValueError:
            return False
        
        return True

    def show_playlist(self):
        self.display_area.delete(1.0, tk.END)
        if not self.playlist:
            self.display_area.insert(tk.END, "Playlist is empty.")
            return

        self.display_area.insert(tk.END, "Your Playlist:\n")
        self.display_area.insert(tk.END, "-" * 50 + "\n")

        for song in self.playlist:
            self.display_area.insert(tk.END, f"{song.title} - {song.artist} ({song.genre}) [{song.duration}] ({song.release_year})\n")
            self.display_area.insert(tk.END, "-" * 50 + "\n")

    def sort_playlist(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty. Add songs before sorting.")
            return

        sort_options = {
            '1': ('title', 'Title'),
            '2': ('artist', 'Artist'),
            '3': ('genre', 'Genre'),
            '4': ('duration', 'Duration'),
            '5': ('release_year', 'Release Year')
        }

        options_message = "\n".join([f"{key}: Sort by {value[1]}" for key, value in sort_options.items()])
        sort_key_choice = simpledialog.askstring("Input", f"Choose attribute to sort by:\n{options_message}\nEnter number:")

        if sort_key_choice not in sort_options:
            messagebox.showerror("Error", "Invalid choice. Please enter a valid number.")
            return

        order_choice = simpledialog.askstring("Input", "Enter 1 for Ascending or 2 for Descending:").strip()

        if order_choice not in ['1', '2']:
            messagebox.showerror("Error", "Invalid choice. Please enter 1 or 2.")
            return

        ascending = order_choice == '1'

        key_attribute = sort_options[sort_key_choice][0]
        if key_attribute == 'release_year':  
            self.playlist.sort(key=lambda song: int(getattr(song, key_attribute)), reverse=(not ascending))
        else:
            self.playlist.sort(key=lambda song: getattr(song, key_attribute), reverse=(not ascending))

        order_text = 'ascending' if ascending else 'descending'
        messagebox.showinfo("Success", f"Playlist sorted by {sort_options[sort_key_choice][1]} in {order_text} order.")

    def save_playlist(self):
        filename = simpledialog.askstring("Input", "Enter filename to save the playlist:")
        if not filename:
            messagebox.showerror("Error", "Filename cannot be empty.")
            return

        try:
            with open(filename, 'w') as f:
                for song in self.playlist:
                    f.write(f"{song.title} - {song.artist} ({song.genre}) [{song.duration}] ({song.release_year})\n")
            messagebox.showinfo("Success", f"Playlist saved as '{filename}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save playlist: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()
