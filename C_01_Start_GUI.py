from tkinter import *


class StartQuiz:
    """

    Initial Game interface (ask users how many rounds of questions they
    would like to play)
    """

    def __init__(self):
        """

        Gets number of rounds from user
        """

        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame = Label(bg="#D2C4FF")
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In each round you will be asked to match the song title to the "
                        "artist that wrote the song and the year the song was released. \n"
                        "\n"
                        "In the box below please enter the number of rounds you would "
                        "like to play to begin")

        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds of questions do you want to play?"

        # Title string
        title_string = "Song / Artist Quiz 🎵"

        # List of labels to be made
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
        self.entry_area_frame.config(bg="#D2C4FF")

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#000000", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=1, column=0)

    def check_rounds(self):
        """

        Checks user has entered 1 or more rounds
        """

        # Retrieve temperature to be converted
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
                # temporary success message, replace with call to PlayGame class
                self.choose_label.config(text=f"You have chosen to play {rounds_wanted} rounds.")
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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Song / Artist Quiz")
    StartQuiz()
    root.mainloop()
