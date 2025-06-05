from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartGame:
    """

    Initial Quiz interface (ask users how many rounds of questions they
    would like to play)
    """

    def __init__(self):
        """

        Gets number of rounds from user
        """

        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame.grid()

        # Create play button
        self.play_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                  fg="#000000", bg="#96AEFF", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """

        Checks user has entered a valid number for rounds
        """

        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """

        Invokes Quiz GUI and takes across number of rounds to be played.
        """
        Play(num_rounds)
        # hide root window
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):

        # Random Score test Data....
        self.all_scores_list = [2, 5, 3, 5, 5]
        self.all_high_score_list = [5, 5, 5, 5, 5]

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.quiz_frame, text="Song / Artist Quiz", font=("Arial", 16, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.results_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                     text="Results", width=15, fg="#000000",
                                     bg="#96AEFF", padx=10, pady=10, command=self.to_results)
        self.results_button.grid(row=1)

    def to_results(self):
        """
        Retrieves everything we need to display the game / round statistics
        """
        results_bundle = [self.all_scores_list,
                          self.all_high_score_list]

        Results(self, results_bundle)


class Results:
    """
    Displays results for Song / Artist Quiz
    """

    def __init__(self, partner, all_results_info):
        # Extract information from master list...
        user_scores = all_results_info[0]
        high_scores = all_results_info[1]

        # sort user scores to find high score...
        user_scores.sort()

        self.results_box = Toplevel()

        # if users press cross at top, close help and release help button
        self.results_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_results, partner))

        self.results_frame = Frame(self.results_box, width=300)
        self.results_frame.grid()

        # Math to populate results dialogue...
        rounds_played = len(user_scores)
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # strings for results labels...
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Possible Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

        # custom comment text and formatting
        if total_score == max_possible:
            comment_string = ("Amazing! You got the highest"
                              "possible score!")
            comment_colour = "#96AEFF"

        elif total_score == 0:
            comment_string = ("Oops - You've lost every round! "
                              "You might want to look at the hints!")
            comment_colour = "#96AEFF"
            best_score_string = f"Best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#96AEFF"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | font | sticky
        all_results_strings = [
            ["- Results -", heading_font, ""],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Results", heading_font, ""],
            [best_score_string, normal_font, "W"],
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
        results_comment_label = results_label_ref_list[4]
        results_comment_label.config(bg=comment_colour)

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
        partner.results_button.config(state=NORMAL)
        self.results_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()