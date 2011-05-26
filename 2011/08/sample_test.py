import unittest
from copy import copy
from solution import *

raw = """
01; Mr. P.C.;                  John Coltrane;      Jazz, Bebop;        fast
02; My Favourite Things;       John Coltrane;      Jazz, Bebop;        popular, cover
03; Greensleves;               John Coltrane;      Jazz, Bebop;        popular, cover
04; Alabama;                   John Coltrane;      Jazz, Avantgarde;   melancholic
05; Acknowledgement;           John Coltrane;      Jazz, Avantgarde;
06; Afro Blue;                 John Coltrane;      Jazz;               melancholic
07; 'Round Midnight;           John Coltrane;      Jazz;               cover
08; My Funny Valentine;        Miles Davis;        Jazz;               popular
09; Tutu;                      Miles Davis;        Jazz, Fusion;
10; Miles Runs The Voodo Down; Miles Davis;        Jazz, Fusion;
11; Boplicity;                 Miles Davis;        Jazz, Bebop;
12; Autumn Leaves;             Bill Evans;         Jazz;               popular, cover
13; Waltz for Debbie;          Bill Evans;         Jazz;
14; 'Round Midnight;           Thelonious Monk;    Jazz, Bebop;
15; Ruby, My Dear;             Thelonious Monk;    Jazz;               saxophone
16; Blue Monk;                 Thelonious Monk;    Jazz;
17; Fur Elise;                 L. van Beethoven;   Classical;          popular
18; Moonlight Sonata;          L. van Beethoven;   Classical;          popular
19; Pathetique;                L. van Beethoven;   Classical;
20; Toccata e Fuga;            J.S. Bach;          Classical, Baroque; popular
21; Goldberg Variations;       J.S. Bach;          Classical, Baroque;
22; Brandenburg Concerto;      J.S. Bach;          Classical, Baroque;
23; Eine Kleine Nachtmusik;    W.A. Mozart;        Classical;          popular, violin
""".strip()

songs_text = "\n".join(line[4:] for line in raw.split("\n"))

handles = {}

for line in raw.split("\n"):
    number, name, artist, genre, tags = map(str.strip, line.split(";"))
    handles[int(number.strip())] = name + "/" + artist

tags = {
  "John Coltrane":    {'saxophone'},
  "Miles Davis":      {'trumpet'},
  "Bill Evans":       {'piano'},
  "Thelonious Monk":  {'piano', 'bebop'},
  "J.S. Bach":        {'piano', 'polyphony'},
  "L. van Beethoven": {'piano'},
  "W.A. Mozart":      {'piano'},
}

class CollectionTest(unittest.TestCase):
    def setUp(self):
        self.collection = Collection(songs_text, copy(tags))

    def assertSongs(self, song_ids, **what):
        expected = sorted([handles[song_id] for song_id in song_ids])
        actual = sorted([song.name + "/" + song.artist for song in self.collection.find('songs', **what)])
        self.assertEqual(expected, actual)

    def test_simple_tag(self):
        self.assertSongs([4, 6], tags={'melancholic'})
        self.assertSongs([2, 3, 8, 12, 17, 18, 20, 23], tags={'popular'})
        self.assertSongs([1], tags={'fast'})

    def test_negative_tags(self):
        self.assertSongs([6], tags={'melancholic', 'avantgarde!'})
        self.assertSongs([17, 18, 23], tags={'popular', 'piano', 'jazz!', 'baroque!'})

    def test_find_subgenre(self):
        self.assertEqual(
            {'Baroque', 'Bebop'},
            set(self.collection.find('subgenre', tags='popular')))

if __name__ == "__main__":
    unittest.main()
