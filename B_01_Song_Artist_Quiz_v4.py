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

    # get artists/years/songs and set up empty lists
    all_artist_list = get_songs()
    selected_songs = []
    artist_names = set()

    # select four random artists with a potential song
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

        # strings for labels
        intro_string = ("In each round you will be asked to match the song title to the "
                        "artist that wrote the song and the year the song was released. \n"
                        "\n"
                        "In the box below please enter the number of rounds you would "
                        "like to play to begin")

        choose_string = "How many rounds of questions do you want to play?"

        # Title string
        title_string = "Song / Artist Quiz 🎵"

        # List of labels
        start_labels_list = [
            [title_string, ("Arial", "18", "bold"), "#D2C4FF", "#000000"],
            [intro_string, ("Arial", "11"), "#D2C4FF", "#000000"],
            [choose_string, ("Arial", "11", "bold"), "#D2C4FF", "#000000"]
        ]

        # create labels and add them to the reference list...
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], bg=item[2],
                               fg=item[3],
                               wraplength=400, justify="left", pady=10, padx=20)
            make_label.grid(row=count)
            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an error message if necessary.
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#000000", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=1, column=0)

        # Create a list for the background colour
        background_list = [
            self.start_frame,
            self.entry_area_frame
        ]

        for widget in background_list:
            widget.config(bg="#D2C4FF")


    def check_rounds(self):
        """
        Checks user has entered 1 or more rounds
        """

        rounds_wanted = self.num_rounds_entry.get()

        # reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more that zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Get play class
                Play(rounds_wanted)
                # Hide root window
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for the Song/Artist Quiz
    """

    def __init__(self, check_rounds):

        # Set up default values
        self.points_score = IntVar(value=0)
        self.rounds_played = IntVar(value=0)
        self.rounds_wanted = IntVar(value=check_rounds)

        self.play_box = Toplevel()
        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # Gets artist list and the correct artist
        self.round_artist_list = []
        self.correct_index = None

        # Score List / score tracker
        self.all_scores_list = []
        self.all_high_score_list = []
        self.round_score = 0

        # body for most of the labels
        body_font = ("Arial", "12")

        # list for labels details
        play_labels_list = [
            ["", ("Arial", "15", "bold"), "#D2C4FF", 0],
            ["Which artist was the song below written by?", body_font, "#FFF2CC", 1],
            ["", ("Arial", 13, "bold"), "#E1D5E7", 2],
            ["", ("Arial", 10), "#FFF8C1", 4],
            ["Which year was the song released?", body_font, "#FFF2CC", 5],
        ]

        self.play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            self.play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured
        self.heading_label = self.play_labels_ref[0]
        self.target_label = self.play_labels_ref[1]
        self.song_title_label = self.play_labels_ref[2]
        self.results_label = self.play_labels_ref[3]
        self.year_title_label = self.play_labels_ref[4]

        # Show heading with correct values
        self.score_title_heading()

        # set up artist buttons...
        self.artist_frame = Frame(self.quiz_frame)
        self.artist_frame.grid(row=3)
        self.artist_button_ref = []

        # create four buttons for the artist names in a grid
        for item in range(4):
            self.artist_button = Button(self.artist_frame, font=("Arial", 11),
                                        text="Artist Name", width=17,
                                        command=partial(self.round_results_artists, item),
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
                                      command=partial(self.round_results_year, item),
                                      bg="#684680", fg="#FFFFFF")
            self.year_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)
            self.year_button_ref.append(self.year_button)

        # label for year result feedback
        self.year_result_label = Label(self.quiz_frame, text="", font=("Arial", 10),
                                       bg="#FFF8C1", wraplength=300, justify="left")
        self.year_result_label.grid(row=7, pady=10, padx=10)

        # Frame to hold hints and results buttons
        self.hints_results_frame = Frame(self.quiz_frame)
        self.hints_results_frame.grid(row=9)

        # list for buttons (frame | text | bg | command | width | row | column | fg)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#7FD188", self.new_round, 21, 8, None, "#000000"],
            [self.hints_results_frame, "Help", "#FFCD93", self.to_help, 10, 0, 0, "#000000"],
            [self.hints_results_frame, "Results", "#96AEFF", self.to_results, 10, 0, 1, "#000000"],
            [self.quiz_frame, "End Quiz", "#990000", self.close_play, 21, 10, None, "#FFFFFF"]
        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg=item[7], width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)
            control_ref_list.append(make_control_button)

        # Retrieve results, next round and end quiz button
        self.next_button = control_ref_list[0]
        self.help_button = control_ref_list[1]
        self.results_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.results_button.config(state=DISABLED)

        # Create a list for the background colour
        background_list = [
            self.quiz_frame,
            self.artist_frame,
            self.year_frame,
            self.hints_results_frame
        ]
        for widget in background_list:
            widget.config(bg="#D2C4FF")

        self.new_round()

    def new_round(self):
        """
        Gets four random artists and unique years for each round
        """

        # Get number of rounds played by user
        rounds_played = self.rounds_played.get() + 1
        self.rounds_played.set(rounds_played)

        # Resets score for a new round
        self.round_score = 0

        # Reset button colors
        for button in self.artist_button_ref + self.year_button_ref:
            button.config(bg="#684680")

        # Retrieves round artists
        self.round_artist_list = get_round_artists()

        # Get the correct artist from one of the four
        self.correct_index = random.randint(0, 3)
        correct_song = self.round_artist_list[self.correct_index]

        # Displays Song and year question
        self.song_title_label.config(text=correct_song[1])
        self.year_title_label.config(text="Which year was the song released?")

        # Set artist buttons
        for item in range(4):
            self.artist_button_ref[item].config(
                text=self.round_artist_list[item][0], state=NORMAL
            )

        # Get the correct year
        correct_year = correct_song[2]

        # Collect all unique years from all songs (excluding the correct one)
        all_songs = get_songs()
        all_years = list(set([song[2] for song in all_songs if song[2] != correct_year]))

        # Ensure there are enough unique years to choose from
        if len(all_years) < 3:
            raise Exception("Not enough unique years in the song list to generate choices.")

        # Combine and shuffle the year options
        if len(all_years) >= 3:
            wrong_years = random.sample(all_years, 3)
        else:
            wrong_years = random.choices(all_years, k=3)
        year_options = wrong_years + [correct_year]
        # shuffles years for buttons
        random.shuffle(year_options)

        for item in range(4):
            self.year_button_ref[item].config(text=year_options[item], state=DISABLED)

        # Reset result labels and disable next button
        self.results_label.config(text="", bg="#FFF8C1")
        self.year_result_label.config(text="", bg="#FFF8C1")
        self.next_button.config(state=DISABLED)

        self.score_title_heading()

    def score_title_heading(self):
        self.heading_label.config(
            text=f"Round {self.rounds_played.get()} / {self.rounds_wanted.get()}    Score: {self.points_score.get()}"
        )

    def round_results_artists(self, user_choice):
        """

        Retrieves which artist button was pushed (index 0 - 3), retrieves
        score from the first question and gives the correct artist
        """
        selected_artist = self.artist_button_ref[user_choice].cget('text')
        correct_artist = self.round_artist_list[self.correct_index][0]

        # Disable artist buttons after question has been answered
        for item, button in enumerate(self.artist_button_ref):
            button.config(state=DISABLED)

        # Make correct artist green / incorrect artist red
            if self.round_artist_list[item][0] == correct_artist:
                button.config(bg="#7FD188")
            elif item == user_choice:
                button.config(bg="#FF6666")

        # Show results messages after question has been answered
        if user_choice == self.correct_index:
            self.round_score += 2
            self.points_score.set(self.points_score.get() + 2)
            result_text = f"Correct! {selected_artist} wrote the song. (+2 points)"
            result_bg = "#86D68C"

        else:
            result_text = f"Wrong! {selected_artist} didn't write it.\nCorrect: {correct_artist}"
            result_bg = "#FF6666"

        # Get results label and get score title heading (to display artist score)
        self.results_label.config(text=result_text, bg=result_bg)
        self.score_title_heading()

        # Enable year buttons now
        for button in self.year_button_ref:
            button.config(state=NORMAL)

    def round_results_year(self, user_choice):
        """

        Retrieves which year button was pushed (index 0 - 3), retrieves
        score from the second question and gives the correct year
        """
        selected_year = self.year_button_ref[user_choice].cget('text')
        correct_year = self.round_artist_list[self.correct_index][2]

        # Disable year buttons after question has been answered
        for item, button in enumerate(self.year_button_ref):
            button.config(state=DISABLED)

        # Make correct artist green / incorrect artist red
        for button in self.year_button_ref:
            if button.cget('text') == correct_year:
                button.config(bg="#7FD188")
            elif button.cget('text') == selected_year:
                button.config(bg="#FF6666")

        # Show results messages after question has been answered
        if selected_year == correct_year:
            self.round_score += 3
            self.points_score.set(self.points_score.get() + 3)
            result_text = f"Correct! The song was released in {correct_year}. (+3 points)"
            result_bg = "#86D68C"
        else:
            result_text = f"Wrong year! You chose {selected_year}.\nCorrect: {correct_year}"
            result_bg = "#FF6666"

        # Get results label and get score title heading (to display year score)
        self.year_result_label.config(text=result_text, bg=result_bg)
        self.score_title_heading()

        # Append score and high score for this round
        self.all_scores_list.append(self.round_score)
        self.all_high_score_list.append(5)

        # Disabled/Normal button
        if self.rounds_played.get() == self.rounds_wanted.get():
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")
        else:
            self.next_button.config(state=NORMAL)

        self.results_button.config(state=NORMAL)

    def close_play(self):
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_help(self):
        """
        Displays hints for playing game
        :return:
        """
        # check we have played at least one round so that
        ShowHelp(self, self.rounds_played.get())

    def to_results(self):
        """
        Retrieves everything we need to display the quiz results
        """
        results_bundle = [self.all_scores_list,
                          self.all_high_score_list]

        Results(self, results_bundle)


class ShowHelp:
    """
    Displays help for Song/Artist Quiz
    """

    def __init__(self, partner, rounds_played):
        self.rounds_played = rounds_played

        # setup dialogue box
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.results_button.config(state=DISABLED)

        # if users press cross at top, close help and release help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="- Help -",
                                        font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("In each round you will be asked to match the song title to the "
                    "artist that wrote the song and the year the song was released. "
                     "Guessing the correct artist will get you 3 points, and the correct "
                     "year will get you 2 points.\n"
                    "\n"
                    "You must answer the artist question before the year, and must take "
                     "a guess at each question before proceeding.")

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#FFCD93",
                                     fg="#000000",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # list and loop to set background colour on everything
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box (and enables help button)
        """
        # put help button back to normal
        partner.help_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.results_button.config(state=NORMAL)

        self.help_box.destroy()


class Results:
    """
    Displays results for Song / Artist Quiz
    """

    def __init__(self, partner, all_results_info):

        # disable buttons to prevent program crashing
        partner.help_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.results_button.config(state=DISABLED)

        # Extract information
        user_scores = all_results_info[0]
        high_scores = all_results_info[1]

        # if users press cross at top, close help and release help button
        self.results_box = Toplevel()
        self.results_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_results, partner))

        self.results_frame = Frame(self.results_box, width=300)
        self.results_frame.grid()

        # math to populate results dialogue
        rounds_played = len(user_scores)
        max_possible = sum(high_scores)

        # Gets average score
        total_score = sum(user_scores)
        average_score = total_score / rounds_played if rounds_played > 0 else 0

        # strings for results labels...
        total_score_string = f"Total Points: {total_score}"
        max_possible_string = f"Maximum Possible Points: {max_possible}"
        average_score_string = f"Average Score (per round): {average_score:.0f}\n"

        # comment text and formatting
        if total_score == max_possible:
            comment_string = (" ~ Amazing! You got the highest \n"
                              "possible score! ~")
            comment_colour = "#96AEFF"
            comment_background = "#BDCDFF"

        elif total_score == 0:
            comment_string = ("~ Oops - You've lost every round! "
                              "Keep Trying! ~")
            comment_colour = "#96AEFF"
            comment_background = "#BDCDFF"
        else:
            comment_string = "  ===================== "
            comment_colour = "#96AEFF"
            comment_background = "#BDCDFF"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Georgia", "13")

        # Label list (text | font | sticky)
        all_results_strings = [
            ["~~ Results of Quiz ~~", heading_font, ""],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        results_label_ref_list = []
        for count, item in enumerate(all_results_strings):
            self.results_label = Label(self.results_frame, text=item[0], font=item[1],
                                       anchor="w", justify="left", bg="#96AEFF",
                                       padx=30, pady=5)
            self.results_label.grid(row=count, sticky=item[2], padx=10)
            results_label_ref_list.append(self.results_label)

        # Configure comment label background (for all won / all lost)
        results_comment_label = results_label_ref_list[3]
        results_comment_label.config(bg=comment_colour)
        results_comment_label.config(bg=comment_background)

        self.dismiss_button = Button(self.results_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_results,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        # Create a list for the background colour
        background_list = [
            self.results_frame,
            self.results_label
        ]

        for widget in background_list:
            widget.config(bg="#96AEFF")

    def close_results(self, partner):
        # put results button back to normal
        partner.help_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.results_button.config(state=NORMAL)
        self.results_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Song / Artist Quiz")
    StartQuiz()
    root.mainloop()