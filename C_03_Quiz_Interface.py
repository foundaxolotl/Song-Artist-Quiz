from tkinter import *


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

            play_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons...
        self.artist_frame = Frame(self.quiz_frame)
        self.artist_frame.grid(row=3)
        self.year_frame = Frame(self.quiz_frame)
        self.year_frame.grid(row=5)

        # create four buttons for the artist names in a 2 x 2 grid
        for item in range(0, 4):
            self.artist_button = Button(self.artist_frame, font=("Arial", "12"),
                                        text="Artist Name", width=15, bg="#684680", fg="#FFFFFF")
            self.artist_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
        # create  four buttons for the year names
        for item in range(0, 4):
            self.year_button = Button(self.year_frame, font=("Arial", "12"),
                                      text="Year Name", width=15, bg="#684680", fg="#FFFFFF")
            self.year_button.grid(row=item // 2,
                                  column=item % 2,
                                  padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column | fg)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#7FD188", "", 21, 7, None, "#000000"],
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

        # Create a list for the background colour
        background_list = [
            self.quiz_frame,
            self.artist_frame,
            self.year_frame,
            self.hints_stats_frame,

        ]

        for widget in background_list:
            widget.config(bg="#D2C4FF")

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
