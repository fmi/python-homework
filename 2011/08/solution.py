import re

class Song:
    __slots__ = ['name', 'artist', 'genre', 'sub_genre', 'tags']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Collection:
    def __init__(self, songs_text, tags):
        self.entries = []

        for line in songs_text.split("\n"):
            name, artist, genre_and_sub_genre, tag_string = map(str.strip, line.split(';'))
            genre, sub_genre = re.match(r'(\S+)(?:,\s*(\S+))?', genre_and_sub_genre).groups()
            tags = set(map(str.strip, tag_string.split(',')))

            song = Song(name=name, artist=artist, genre=genre, sub_genre=sub_genre, tags=tags)

            self.entries.append(song)

    def find(self, result, **criteria):
        return [song for song in self.entries if criteria['tags'] & song.tags]
