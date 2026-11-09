import tkinter as tk  # Import tkinter library for GUI, aliased as 'tk'
import tkinter.scrolledtext as tkst  # Import scrolledtext widget from tkinter, aliased as 'tkst'
from tkinter import messagebox  # Import messagebox from tkinter for popup error dialogs

import message_manager as messages  # Import custom message_manager module, aliased as 'messages'
import font_manager as fonts  # Import custom font_manager module, aliased as 'fonts'

# --- Colour scheme ---
# All colours are defined here so they are easy to change in one place
BG_MAIN = "#f0f4f8"       # Light blue-grey background for the main window
BG_TEXT = "#ffffff"       # White background for text/entry fields
BTN_PRIMARY = "#4a7fc1"   # Medium blue for main action buttons
BTN_CLOSE = "#888888"     # Grey for the Close button (less prominent)
BTN_FG = "#ffffff"        # White text on all buttons
LBL_FG = "#333333"        # Dark text for labels


class LabelMessage():  # Define a class called LabelMessage for the label/search message window
    def __init__(self, window):  # Constructor method, takes a tkinter window as argument

        self.window = window  # Store the window reference as an instance variable
        self.window.geometry("500x320")  # Set the window size to 500x320 pixels
        self.window.title("Label Message")  # Set the window title to "Label Message"
        self.window.configure(bg=BG_MAIN)  # Set the window background to the light blue-grey colour

        id_lbl = tk.Label(window, text="Message ID:", bg=BG_MAIN, fg=LBL_FG)  # Create a label with text "Message ID:" on matching background
        id_lbl.grid(row=0, column=0, sticky="E", padx=10, pady=10)  # Place label at row 0, col 0, aligned east

        self.message_id_txt = tk.Entry(window, width=40, bg=BG_TEXT)  # Create a text entry field for the message ID, 40 chars wide, white background
        self.message_id_txt.grid(row=0, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place entry spanning 5 columns at row 0

        label_messages_lbl = tk.Label(window, text="Label:", bg=BG_MAIN, fg=LBL_FG)  # Create a label with text "Label:" on matching background
        label_messages_lbl.grid(row=1, column=0, sticky="E", padx=10, pady=10)  # Place label at row 1, col 0, aligned east

        self.label_txt = tk.Entry(window, width=40, bg=BG_TEXT)  # Create a text entry field for the label, 40 chars wide, white background
        self.label_txt.grid(row=1, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place entry spanning 5 columns at row 1

        addlabel_btn = tk.Button(window, text="Add Label to Message", command=self.add_label,
                                 bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)  # Create an "Add Label to Message" button with blue styling
        addlabel_btn.grid(row=2, column=1, padx=10, pady=10)  # Place button at row 2, col 1

        listmessages_btn = tk.Button(window, text="List All Messages Labelled", command=self.list_messages,
                                     bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)  # Create a "List All Messages Labelled" button with blue styling
        listmessages_btn.grid(row=2, column=2, padx=10, pady=10)  # Place button at row 2, col 2

        close_btn = tk.Button(window, text="Close", command=self.close,
                              bg=BTN_CLOSE, fg=BTN_FG, relief="flat", padx=6)  # Create a "Close" button with grey styling
        close_btn.grid(row=2, column=3, padx=10, pady=10)  # Place button at row 2, col 3

        self.output_txt = tkst.ScrolledText(window, width=48, height=8, wrap="word",
                                            bg=BG_TEXT, relief="flat")  # Create a scrollable text area with white background and no border
        self.output_txt.grid(row=3, column=0, columnspan=6, sticky="W", padx=10, pady=10)  # Place text area spanning all 6 columns at row 3

    def add_label(self):  # Method to add a label to a message
        message_id_string = self.message_id_txt.get()  # Get the raw text from the message ID entry field

        # Stage 4 validation: check if the input is a valid integer before converting
        if not message_id_string.isdigit():  # isdigit() returns False for text like "four", empty strings, or negative numbers
            messagebox.showerror("Error", "Please enter a valid numeric message ID")  # Show a popup error dialog for bad input
            return  # Exit the method early without making changes

        message_id = int(message_id_string)  # Convert the validated string to an integer
        label = self.label_txt.get()  # Get the label text from the entry field

        if label == "":  # Check if the label field is empty
            messagebox.showerror("Error", "Label cannot be empty")  # Show a popup error if label is empty
            return  # Exit the method early without making changes

        # Check whether the message ID actually exists in the message manager
        if messages.get_sender(message_id) is None:  # get_sender returns None if no message has that ID
            messagebox.showerror("Error", f"No message found with ID {message_id}")  # Show error popup for non-existent message
            return  # Exit early if the message doesn't exist

        messages.set_label(message_id, label)  # Call set_label from message_manager to apply the label to the message
        self.output_txt.insert(tk.END, f"Label '{label}' added to message {message_id}\n")  # Display a success message in the output area

    def list_messages(self):  # Method to list messages filtered by the entered label
        label = self.label_txt.get()  # Get the label text from the entry field

        if label == "":  # Check if the label field is empty
            messagebox.showerror("Error", "Please enter a label to search for")  # Show popup error if no label was entered
            return  # Exit the method early without searching

        result = messages.list_all(label)  # Call list_all from message_manager with the label as a filter

        self.output_txt.delete("1.0", tk.END)  # Clear the output text area before displaying new results
        self.output_txt.insert(tk.END, result)  # Insert the filtered message list into the output area

    def close(self):  # Method to close the window
        self.window.destroy()  # Destroy the tkinter window


if __name__ == "__main__":  # Only runs when this file is run as a standalone
    window = tk.Tk()  # Create a TK root window object
    fonts.configure()  # Configure the fonts using the font_manager module
    LabelMessage(window)  # Instantiate the LabelMessage GUI with the window
    window.mainloop()  # Start the tkinter event loop, keeping the window open and reactive