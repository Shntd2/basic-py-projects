import random


class Song:
    """Represents a song with its artist, album, year, and name"""
    def __init__(self, artist, album, year, song_name):
        self.artist = artist
        self.album = album
        self.year = year
        self.song_name = song_name

    def __str__(self):
        """Returns a string representation of the song in the format 'Artist - Song Name/Album, Year'"""
        return f'{self.artist} - {self.song_name}/{self.album}, {self.year}'


class Playlist:
    """Represents a collection of songs."""
    def __init__(self):
        self.songs = []

    def load_songs_from_file(self, filename):
        """Loads songs from a file into the playlist"""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    song_info = line.strip().split('\t')
                    if len(song_info) == 4:
                        artist, album, year, name = song_info
                        song = Song(artist, album, year, name)
                        self.songs.append(song)
                    else:
                        print(f"Skipping invalid line: {line}")
        except FileNotFoundError:
            print(f"File '{filename}' not found")
        except ValueError:
            print(f"Error parsing data in file '{filename}'")


class Player:
    """Represents a music player that can play songs from a playlist"""
    def __init__(self, filename):
        self.playlist = Playlist()
        self.playlist.load_songs_from_file(filename)

        self.is_on = False
        self.current_song_index = None
        self.current_song = None
        self.is_shuffle = False

    def get_current_song(self):
        """Returns the current song being played"""
        get_song = self.playlist.songs.__getitem__
        return get_song(self.current_song_index)

    def play(self):
        """Plays the current song"""
        if not self.is_on:
            self.is_on = True
            self.current_song_index = 0
            print(f'Playing {self.get_current_song()}')

    def stop(self):
        """Stops the current song"""
        if self.is_on:
            self.is_on = False
            print(f'Stopping {self.get_current_song()}')

    def next_song(self):
        """Plays the next song"""
        if self.is_on:
            if not self.is_shuffle:
                next_index = (self.current_song_index + 1) % len(self.playlist.songs)
            else:
                next_index = random.randrange(len(self.playlist.songs))
            self.current_song_index = next_index
            print(f'Playing {self.get_current_song()}')
        else:
            print('Player is off')

    def previous_song(self):
        """Plays the previous song"""
        if self.is_on:
            if not self.is_shuffle:
                next_index = (self.current_song_index - 1) % len(self.playlist.songs)
            else:
                next_index = random.randrange(len(self.playlist.songs))
            self.current_song_index = next_index
            print(f'Playing {self.get_current_song()}')
        else:
            print('Player is off')

    def shuffle(self):
        """Shuffles the order of songs in the playlist"""
        self.is_shuffle = not self.is_shuffle
        if self.is_shuffle:
            random.shuffle(self.playlist.songs)


player = Player('albums.txt')
player.play()
player.next_song()
player.next_song()
player.next_song()
player.shuffle()
player.next_song()
player.next_song()
player.shuffle()
player.next_song()
player.next_song()
player.previous_song()
player.stop()
