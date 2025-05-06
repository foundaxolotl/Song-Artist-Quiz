import csv
import random


def round_ans(val):
    """
    Rounding the number
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Retrieve Songs from csv file and put them in a list
file = open("00_pop_rock_songs.csv", "r")
all_songs = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_songs.pop(0)

song_artist_year = []
songs_titles = []
artist_names = []

# loop until we have four songs, artists, and years randomly...
while len(song_artist_year) < 4:
    potential_song = random.choice(all_songs)
    potential_artist = random.choice(all_songs)

    # Get the score and check it's not a duplicate
    if potential_song[1] not in songs_titles:
        song_artist_year.append(potential_song)
        songs_titles.append(potential_song[1])


print(song_artist_year)
print(songs_titles)
print(artist_names)
