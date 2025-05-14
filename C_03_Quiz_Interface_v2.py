import csv
import random
from tkinter import *
from functools import partial


def get_songs():
    # Retrieve Songs from csv file
    file = open("00_pop_rock_songs.csv", "r")
    all_songs = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_songs.pop(0)

    return all_songs


def get_round_artists():
    """
    Choose four colours from larger lists ensuring that the artists are all different
    """

    all_artist_list = get_round_artists()

    song_artist_year = []
    songs_titles = []
    artist_names = []
    release_years = []

    # loop until we have four artists...
    while len(song_artist_year) < 4:
        potential_artist = random.choice(all_artist_list)

        # Get the score and check it's not a duplicate
        if potential_artist[1] not in artist_names:
            song_artist_year.append(potential_artist)

    return song_artist_year


class StartQuiz:
    """

    Initial Game interface (ask users how many rounds of questions they
    would like to play)
    """

    def __init__(self):
        """

        Gets users input of number of rounds wanted
        """

        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame.grid()

        # Make play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#841F3F", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks user has entered a valid number of rounds
        """

        Play(5)
        # hides root window
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, check_rounds):

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(check_rounds)

        # Artist names list
        self.round_artist_list = []

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body for most labels...
        body_font = ("Arial", "12")

        # list of label details
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), "#D2C4FF", 0],
            ["Which artist was the song below written by?", body_font, "#FFF2CC", 1],
            ["                 Song Name                ", body_font, "#E1D5E7", 2],
            ["Which year was the song released?", ("Arial", "12"), "#FFF8C1", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up artist and year buttons...
        self.artist_frame = Frame(self.quiz_frame)
        self.artist_frame.grid(row=3)
        self.year_frame = Frame(self.quiz_frame)
        self.year_frame.grid(row=5)

        self.artist_button_ref = []
        self.year_button_ref = []
        self.button_songs_list = []

        # create four buttons for the artist names in a 2 x 2 grid
        for item in range(0, 4):
            self.artist_button = Button(self.artist_frame, font=("Arial", "12"),
                                        text="Artist Name", width=15, command=partial(self.round_results, item),
                                        bg="#684680", fg="#FFFFFF")
            self.artist_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # create  four buttons for the year names
        for item in range(0, 4):
            self.year_button = Button(self.year_frame, font=("Arial", "12"),
                                      text="Year Name", width=15, command=partial(self.round_results, item),
                                      bg="#684680", fg="#FFFFFF")
            self.year_button.grid(row=item // 2,
                                  column=item % 2,
                                  padx=5, pady=5)

            self.artist_button_ref.append(self.artist_button)
            self.year_button_ref.append(self.year_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column | fg)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#7FD188", self.new_round, 21, 7, None, "#000000"],
            [self.hints_stats_frame, "Help", "#FFCD93", "", 10, 0, 0, "#000000"],
            [self.hints_stats_frame, "Stats", "#96AEFF", "", 10, 0, 1, "#000000"],
            [self.quiz_frame, "End Game", "#990000", self.close_play, 21, 9, None, "#FFFFFF"]

        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg=item[7], width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve stats, next round and end game button
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Create a list for the background colour
        background_list = [
            self.quiz_frame,
            self.artist_frame,
            self.year_frame,
            self.hints_stats_frame,

        ]

        for widget in background_list:
            widget.config(bg="#D2C4FF")

        self.new_round()

    def new_round(self):
        """
        Gets four random artists for each round
        """

        # Get number of rounds played by user
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()
        print(rounds_wanted)

        # Retrieves round artists
        self.round_artist_list = get_round_artists()

        # Update heading for Rounds heading
        self.heading_label.config(text=f"Round {rounds_played} / {rounds_wanted}")

        for count, item in enumerate(self.artist_button_ref):
            item.config(fg=self.round_artist_list[count][2], bg=self.round_artist_list[count][0],
                        text=self.round_artist_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """

        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds to results to stats list
        """

        # Get user score and colour based on button press...
        score = int(self.round_artist_list[user_choice][1])

        # alternate way to get button name. Good for if button have been scrambled.
        colour_name = self.artist_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)
        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.artist_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # closes quiz for a new one to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Song / Artist Quiz")
    StartQuiz()
    root.mainloop()
