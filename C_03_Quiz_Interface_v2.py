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
    Choose four songs from the CSV ensuring the artists are all different.
    Returns a list of 4 items: [artist, song, year]
    """
    # gets the artists/songs/years
    all_artist_list = get_songs()

    # gets empty list for songs
    selected_songs = []
    artist_names = set()

    while len(selected_songs) < 4:
        potential_song = random.choice(all_artist_list)
        artist = potential_song[0]

        if artist not in artist_names:
            artist_names.add(artist)
            selected_songs.append(potential_song)

    return selected_songs


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
        Play(5)
        # hides root window
        root.withdraw()


class Play:
    """
    Interface
    """

    def __init__(self, check_rounds):

        # set points to 0
        self.points_score = IntVar()
        self.points_score.set(0)

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(check_rounds)

        # Artist names list
        self.round_artist_list = []
        self.correct_item = None

        self.play_box = Toplevel()
        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body for most labels...
        body_font = ("Arial", "12")

        # list of label details
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), "#D2C4FF", 0],
            ["Which artist was the song below written by?", body_font, "#FFF2CC", 1],
            ["                 Song Name                ", ("Arial", "14"), "#E1D5E7", 2],
            ["Which year was the song released?", ("Arial", "12"), "#FFF8C1", 4]
        ]

        self.play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            self.play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = self.play_labels_ref[0]
        self.target_label = self.play_labels_ref[1]
        self.song_title_label = self.play_labels_ref[2]
        self.results_label = self.play_labels_ref[3]

        # set up artist and year buttons...
        self.artist_frame = Frame(self.quiz_frame)
        self.artist_frame.grid(row=3)
        self.artist_button_ref = []

        # create four buttons for the artist names in a 2 x 2 grid
        for item in range(0, 4):
            self.artist_button = Button(self.artist_frame, font=("Arial", "10"),
                                        text="Artist Name", width=18, command=partial(self.round_results, item),
                                        bg="#684680", fg="#FFFFFF")
            self.artist_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.artist_button_ref.append(self.artist_button)

            # set up year buttons...
            self.year_frame = Frame(self.quiz_frame)
            self.year_frame.grid(row=6)
            self.year_button_ref = []

            # create four buttons for the year names in a grid
            for item in range(4):
                self.year_button = Button(self.year_frame, font=("Arial", 11),
                                          text="Year Name", width=17,
                                          command=partial(self.round_results, item),
                                          bg="#684680", fg="#FFFFFF")
                self.year_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)
                self.year_button_ref.append(self.year_button)

            # New label for year result feedback
            self.year_result_label = Label(self.quiz_frame, text="", font=("Arial", 10),
                                           bg="#FFF8C1", wraplength=300, justify="left")
            self.year_result_label.grid(row=7, pady=10, padx=10)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=7)

        # list for buttons (frame | text | bg | command | width | row | column | fg)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#7FD188", self.new_round, 21, 8, None, "#000000"],
            [self.hints_stats_frame, "Help", "#FFCD93", "", 10, 0, 0, "#000000"],
            [self.hints_stats_frame, "Stats", "#96AEFF", "", 10, 0, 1, "#000000"],
            [self.quiz_frame, "End Game", "#990000", self.close_play, 21, 10, None, "#FFFFFF"]

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

        # Update heading for Rounds heading
        self.heading_label.config(text=f"Round {rounds_played} / {rounds_wanted}")

        # Retrieves round artists
        self.round_artist_list = get_round_artists()

        # Get the correct artist from one of the four
        self.correct_item = random.randint(0, 3)
        correct_artist = self.round_artist_list[self.correct_item]

        # Displays Song above artist options
        self.song_title_label.config(text=correct_artist[1])

        for item, button in enumerate(self.artist_button_ref):
            button.config(text=self.round_artist_list[item][0], state=NORMAL)

        self.results_label.config(text="", bg="#FFF8C1")
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """

        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds to results to stats list
        """

        # alternate way to get button name.
        selected_artist = self.artist_button_ref[user_choice].cget('text')
        correct_artist = self.round_artist_list[self.correct_item][0]

        if user_choice == self.correct_item:
            self.points_score.set(self.points_score.get() + 3)
            result_text = f" Correct! {selected_artist} wrote the song. (+3 points)"
            result_bg = "#82B366"
        else:
            result_text = f" Wrong! {selected_artist} didn't write it.\n {correct_artist} did."
            result_bg = "#F8CECC"

        self.results_label.config(text=result_text, bg=result_bg)

        for button in self.artist_button_ref:
            button.config(state=DISABLED)

        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        if self.rounds_played.get() == self.rounds_wanted.get():
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

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
