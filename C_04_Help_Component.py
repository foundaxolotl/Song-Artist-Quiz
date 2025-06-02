from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartQuiz:
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
                                  fg="#FFFFFF", bg="#000000", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """

        Checks user has entered valid number of rounds
        """

        rounds_wanted = 5
        self.to_quiz(rounds_wanted)

    def to_quiz(self, num_rounds):
        """

        Invokes Game GUI and takes across number of rounds to be played.
        """
        Play(num_rounds)
        # hide root window
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.quiz_frame, text="Song / Artist Quiz", font="Arial",
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.helps_button = Button(self.quiz_frame, font=("Arial", 20, "bold"),
                                   text="Help", width=12, fg="#000000",
                                   bg="#FFCD93", padx=6, pady=6, command=self.to_helps)
        self.helps_button.grid(row=1)

    def to_helps(self):
        """
        Displays helps for quiz
        :return:
        """
        ShowHelp(self)


class ShowHelp:
    """
    Displays helps for Song/Artist Quiz
    """

    def __init__(self, partner):
        # setup dialogue box
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.helps_button.config(state=DISABLED)

        # if users press cross at top, close help and release help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help",
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
        partner.helps_button.config(state=NORMAL)
        self.help_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Song / Artist Quiz")
    StartQuiz()
    root.mainloop()
