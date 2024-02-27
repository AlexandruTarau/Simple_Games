import time
import tkinter as tk
import random

import pygame
from nltk.corpus import words


class EndGamePage(tk.Toplevel):
    def __init__(self, master, result_text, play_again_callback, back_to_menu_callback, wordle_window_size):
        super().__init__(master)
        self.title("Game Over")
        self.configure(bg="#f0f0f0")  # Light gray background

        # Disable window controls
        self.overrideredirect(True)

        # Center the window on the screen
        self.withdraw()
        self.update_idletasks()
        x = (self.winfo_screenwidth() - wordle_window_size[0]) // 2
        y = (self.winfo_screenheight() - wordle_window_size[1]) // 2
        self.geometry("+{}+{}".format(x, y))
        self.deiconify()

        # Set the size of the window to match the Wordle window
        self.geometry("{}x{}+{}+{}".format(*wordle_window_size, x, y))

        # Display result text
        result_label = tk.Label(self, text=result_text, font=("Helvetica", 20), bg="#f0f0f0")
        result_label.pack(pady=20)

        # Buttons
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=20)

        play_again_button = tk.Button(button_frame, text="Play Again", font=("Helvetica", 14),
                                      command=play_again_callback)
        play_again_button.pack(side=tk.LEFT, padx=20)

        back_to_menu_button = tk.Button(button_frame, text="Back to Menu", font=("Helvetica", 14),
                                        command=back_to_menu_callback)
        back_to_menu_button.pack(side=tk.RIGHT, padx=20)


class WordleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle")
        window_width = 1000
        window_height = 600
        self.master.geometry(f"{window_width}x{window_height}")
        # Center the window on the screen
        self.master.update_idletasks()
        x = (self.master.winfo_screenwidth() - window_width) // 2 - 8
        y = (self.master.winfo_screenheight() - window_height) // 2 - 30
        self.master.geometry("+{}+{}".format(x, y))

        # Get a list of five-letter words from the NLTK library
        self.word_list = [word.lower() for word in words.words() if len(word) == 5]
        self.current_word = random.choice(self.word_list)

        self.title_label = tk.Label(master, text="Wordle", font=("Helvetica", 20))
        self.title_label.pack()

        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack(pady=10)  # Added some vertical padding

        self.entry_boxes = []
        self.current_row_index = 0
        self.current_box_index = 0

        self.error_message_label = tk.Label(self.master, text="", font=("Helvetica", 16), bg="#f0f0f0")

        for _ in range(6):
            row_frame = tk.Frame(self.entry_frame)
            row_frame.pack()

            row_boxes = []
            for i in range(5):
                entry = tk.Entry(row_frame, width=4, font=("Helvetica", 16), validate="key",
                                 validatecommand=(master.register(self.validate_entry), "%P"))
                entry.pack(side=tk.LEFT, padx=5)  # Added some horizontal padding
                entry.bind("<Key>", self.handle_key)
                entry.bind("<Return>", self.check_word)
                row_boxes.append(entry)

                # Automatically focus on the first box of the first row at the beginning
                if i == 0 and _ == 0:
                    entry.focus()

            self.entry_boxes.append(row_boxes)

        # Added some vertical spacing between entry boxes and the keyboard
        tk.Label(master).pack()

        self.keyboard_frame = tk.Frame(master)
        self.keyboard_frame.pack()

        self.keyboard_buttons = []
        keyboard_layout = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm"
        ]

        for row in keyboard_layout:
            row_frame = tk.Frame(self.keyboard_frame)
            row_frame.pack()

            for letter in row:
                button = tk.Button(row_frame, text=letter, width=4, height=2, font=("Helvetica", 12),
                                   command=lambda l=letter: self.keyboard_click(l))
                button.pack(side=tk.LEFT, padx=5)  # Added some horizontal padding
                self.keyboard_buttons.append(button)

        # Add a "Back to Menu" button to the left of the keyboard
        back_to_menu_button = tk.Button(self.keyboard_frame, text="Back to Menu", width=10, height=2,
                                        font=("Helvetica", 12),
                                        command=self.back_to_menu)
        back_to_menu_button.pack(side=tk.LEFT, padx=5)  # Added some horizontal padding
        self.keyboard_buttons.append(back_to_menu_button)

        # Add an additional button for the Enter key to the right of the keyboard
        enter_button = tk.Button(self.keyboard_frame, text="Enter", width=4, height=2, font=("Helvetica", 12),
                                 command=self.check_word)
        enter_button.pack(side=tk.RIGHT, padx=5)  # Added some horizontal padding
        self.keyboard_buttons.append(enter_button)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_game)
        self.reset_button.pack()

        self.attempts = 0
        self.score = 0

        self.end_game_page = None

    def validate_entry(self, value):
        # Validate that only one character is entered in the box
        return len(value) <= 1

    def handle_key(self, event):
        current_box = event.widget
        current_index = self.entry_boxes[self.current_row_index].index(current_box)

        if event.keysym == "BackSpace":
            self.handle_backspace(current_box, current_index)
        else:
            # Move focus to the next box, except for the last box
            if current_index < 4:
                next_box = self.entry_boxes[self.current_row_index][current_index + 1]
                next_box.focus()

    def keyboard_click(self, letter):
        for box in self.entry_boxes[self.current_row_index]:
            if not box.get():
                box.insert(0, letter)
                # Move focus to the next box, except for the last box
                current_index = self.entry_boxes[self.current_row_index].index(box)
                if current_index < 4:
                    next_box = self.entry_boxes[self.current_row_index][current_index + 1]
                    next_box.focus()
                break

    def handle_backspace(self, current_box, current_index):
        if current_box.get():
            # If there is a character in the current box, delete it
            current_box.delete(0, tk.END)
        elif current_index > 0:
            # If there is not a character in the current box, delete the character from the previous box
            # and move the focus to the previous box
            prev_box = self.entry_boxes[self.current_row_index][current_index - 1]
            prev_box.delete(0, tk.END)
            prev_box.focus()

    def display_error_message(self, error_text):
        # Create a temporary label for the error message
        overlay = tk.Label(self.master, bg="#f0f0f0", width=self.master.winfo_screenwidth(),
                           height=self.master.winfo_screenheight())
        overlay.place(relx=0, rely=0)

        self.master.update()

        # Create a temporary label for the error message
        error_label = tk.Label(self.master, text=error_text, font=("Helvetica", 16), bg="#f0f0f0", fg="red")
        error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Update the display
        self.master.update()

        # Wait for 2 seconds
        time.sleep(2)

        # Remove the overlay and error label
        overlay.destroy()
        error_label.destroy()

        # Update the display again
        self.master.update()

    def show_error_message(self, message):
        self.error_message_label.config(text=message)
        self.error_message_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.master.update()
        time.sleep(2)  # Display the error message for 2 seconds
        self.error_message_label.place_forget()

    def check_word(self, event=None):
        entered_word = "".join([box.get().lower() for box in self.entry_boxes[self.current_row_index]])

        if len(entered_word) < 5:
            self.display_error_message("Not enough letters")
            return

        correct_position = sum(1 for i, letter in enumerate(entered_word) if letter == self.current_word[i])
        correct_letters = sum(1 for letter in entered_word if letter in self.current_word)

        for box, correct_letter in zip(self.entry_boxes[self.current_row_index], self.current_word):
            if box.get().lower() == correct_letter:
                box.configure({"background": "green"})
            elif box.get().lower() in self.current_word:
                box.configure({"background": "yellow"})
            else:
                box.configure({"background": "grey"})

        self.update_keyboard_colors()

        if correct_position == 5:
            result_text = "Good job! You guessed the word."
            self.score += 1
            self.master.title("Wordle - Score: {}".format(self.score))
            self.display_result_message(result_text, True)
        else:
            self.attempts += 1
            if self.attempts == 6:
                result_text = "Try again! The word was '{}'.".format(self.current_word)
                self.display_result_message(result_text, False)
            else:
                self.current_row_index += 1
                self.current_box_index = 0

                if self.current_row_index == 6:
                    self.reset_game()
                else:
                    self.entry_boxes[self.current_row_index][self.current_box_index].focus()

    def display_result_message(self, result_text, is_winner):
        # Create a full-screen grey overlay
        overlay = tk.Label(self.master, bg="#f0f0f0", width=self.master.winfo_screenwidth(),
                           height=self.master.winfo_screenheight())
        overlay.place(relx=0, rely=0)

        # Create a label for the result message
        result_label = tk.Label(self.master, text=result_text, font=("Helvetica", 20), bg="#f0f0f0",
                                fg="green" if is_winner else "red")
        result_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Create buttons for menu and play again
        menu_button = tk.Button(self.master, text="Go Back to Menu", font=("Helvetica", 14),
                                command=lambda: self.on_button_click("menu"))
        menu_button.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

        play_again_button = tk.Button(self.master, text="Play Again", font=("Helvetica", 14),
                                      command=lambda: self.on_button_click("play_again"))
        play_again_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def on_button_click(self, button_type):
        if button_type == "menu":
            self.master.destroy()
            from main import OptionsPage
            menu = OptionsPage()
            menu.run()
            pygame.quit()
        elif button_type == "play_again":
            # Add any additional actions needed for "Play Again" button
            self.master.destroy()
            root = tk.Tk()
            app = WordleApp(root)
            root.mainloop()

            # Destroy the overlay and result label
        for widget in self.master.winfo_children():
            widget.destroy()

    def remove_result_message(self, overlay, result_label, menu_button, play_again_button):
        overlay.destroy()
        result_label.destroy()
        menu_button.destroy()
        play_again_button.destroy()

    def show_end_game_page(self, result_text):
        # Callback functions for the buttons
        def play_again():
            self.end_game_page.destroy()
            self.reset_game()

        def back_to_menu():
            self.end_game_page.destroy()
            self.master.destroy()  # Close the main game window
            from main import OptionsPage
            menu = OptionsPage()
            menu.run()

        # Create and show the end game page
        wordle_window_size = (self.master.winfo_width(), self.master.winfo_height())
        self.end_game_page = EndGamePage(self.master, result_text, play_again, back_to_menu, wordle_window_size)
        self.end_game_page.wait_window()

    def update_keyboard_colors(self):
        for button, letter in zip(self.keyboard_buttons, "qwertyuiopasdfghjklzxcvbnm"):
            if any(box.get().lower() == letter and box.cget("background") == "grey" for row_boxes in self.entry_boxes
                   for box in row_boxes):
                button.configure({"background": "grey"})
            elif letter in self.current_word:
                if any(box.get().lower() == letter and box.cget("background") == "green" for row_boxes in
                       self.entry_boxes for box in row_boxes):
                    button.configure({"background": "green"})
                elif any(box.get().lower() == letter and box.cget("background") == "yellow" for row_boxes in
                         self.entry_boxes for box in row_boxes):
                    button.configure({"background": "yellow"})
                else:
                    button.configure({"background": "white"})
            else:
                button.configure({"background": "white"})

    def reset_row(self):
        for box in self.entry_boxes[self.current_row_index]:
            box.delete(0, tk.END)
            box.configure({"background": "white"})

        self.current_row_index += 1
        self.current_box_index = 0
        if self.current_row_index == 6:
            self.reset_game()
        else:
            self.entry_boxes[self.current_row_index][self.current_box_index].focus()

    def reset_game(self):
        self.current_word = random.choice(self.word_list)
        self.attempts = 0
        self.current_row_index = 0
        self.current_box_index = 0

        for row_boxes in self.entry_boxes:
            for box in row_boxes:
                box.delete(0, tk.END)
                box.configure({"background": "white"})

        for button in self.keyboard_buttons:
            button.configure({"background": "white"})

            # Automatically focus on the first box of the first row after resetting the game
        self.entry_boxes[0][0].focus()

    def back_to_menu(self):
        self.master.destroy()
        from main import OptionsPage  # Import the OptionsPage class from your options_menu file
        menu = OptionsPage()
        menu.run()
        pygame.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = WordleApp(root)
    root.mainloop()
