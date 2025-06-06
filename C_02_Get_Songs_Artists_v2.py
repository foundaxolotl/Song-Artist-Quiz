import csv
import random


# Retrieve Songs from csv file and put them in a list
file = open("00_pop_rock_songs.csv", "r")
all_songs = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_songs.pop(0)

song_artist_year = []
songs_titles = []
artist_names = []
release_years = []

# loop until we have four songs, artists, and years randomly...
while len(song_artist_year) < 4:
    potential_song = random.choice(all_songs)
    potential_artist = random.choice(all_songs)
    potential_year = random.choice(all_songs)

    # Get the score and check it's not a duplicate
    if potential_song[1] not in songs_titles:
        song_artist_year.append(potential_song)
        songs_titles.append(potential_song[1])

    artist_names = [potential_artist[0] for potential_artist in song_artist_year]
    release_years = [potential_year[2] for potential_year in song_artist_year]


print(song_artist_year)
print(songs_titles)
print(artist_names)
print(release_years)





