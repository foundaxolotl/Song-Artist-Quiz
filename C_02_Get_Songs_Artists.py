import csv
import random


def round_ans(val):
    """
    Rounds temperatures to nearest degree
    :param val: Number to be rounded
    :return: Number rounded to nearest degree
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

round_colours = []
colour_scores = []

# loop until we have four colours with different scores...
while len(round_colours) < 4:
    potential_colour = random.choice(all_songs)

    # Get the score and check it's not a duplicate
    if potential_colour[1] not in colour_scores:
        round_colours.append(potential_colour)
        colour_scores.append(potential_colour[1])

print(round_colours)
print(colour_scores)

# find target score (median)

# change scores to integers
int_scores = [int(x) for x in colour_scores]
int_scores.sort()

median = (int_scores[1] + int_scores[2]) / 2
median = round_ans(median)
print("Median", median)