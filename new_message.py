import tkinter as tk  # Import tkinter library for GUI, aliased as 'tk'
import tkinter.scrolledtext as tkst  # Import scrolledtext widget from tkinter, aliased as 'tkst'
from tkinter import messagebox  # Import messagebox from tkinter for popup dialogs

import message_manager as messages  # Import custom message_manager module, aliased as 'messages'
import font_manager as fonts  # Import custom font_manager module, aliased as 'fonts'

# --- Colour scheme ---
# All colours are defined here so they are easy to change in one place
BG_MAIN = "#f0f4f8"       # Light blue-grey background for the main window
BG_TEXT = "#ffffff"       # White background for text/entry fields
BTN_PRIMARY = "#4a7fc1"   # Medium blue for the Send button
BTN_CANCEL = "#888888"    # Grey for the Cancel button (less prominent than Send)
BTN_FG = "#ffffff"        # White text on all buttons
LBL_FG = "#333333"        # Dark text for labels


class NewMessage():  # Define a class called NewMessage for the compose message window
    def __init__(self, window):  # Constructor method, takes a tkinter window as argument

        self.window = window  # Store the window reference as an instance variable
        self.window.geometry("500x320")  # Set the window size to 500x320 pixels
        self.window.title("NewMessage")  # Set the window title to "NewMessage"
        self.window.configure(bg=BG_MAIN)  # Set the window background to the light blue-grey colour

        sender_lbl = tk.Label(window, text="From:", bg=BG_MAIN, fg=LBL_FG)  # Create a label with text "From:" on matching background
        sender_lbl.grid(row=0, column=0, sticky="E", padx=10, pady=10)  # Place label in grid at row 0, col 0, aligned east

        self.sender_txt = tk.Entry(window, width=40, bg=BG_TEXT)  # Create a text entry field for the sender, 40 chars wide, white background
        self.sender_txt.grid(row=0, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place entry in grid, spanning 5 columns

        recipient_lbl = tk.Label(window, text="To:", bg=BG_MAIN, fg=LBL_FG)  # Create a label with text "To:" on matching background
        recipient_lbl.grid(row=1, column=0, sticky="E", padx=10, pady=10)  # Place label in grid at row 1, col 0, aligned east

        self.recipient_txt = tk.Entry(window, width=40, bg=BG_TEXT)  # Create a text entry field for the recipient, 40 chars wide, white background
        self.recipient_txt.grid(row=1, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place entry in grid, spanning 5 columns

        subject_lbl = tk.Label(window, text="Subject:", bg=BG_MAIN, fg=LBL_FG)  # Create a label with text "Subject:" on matching background
        subject_lbl.grid(row=2, column=0, sticky="E", padx=10, pady=10)  # Place label in grid at row 2, col 0, aligned east

        self.subject_txt = tk.Entry(window, width=40, bg=BG_TEXT)  # Create a text entry field for the subject, 40 chars wide, white background
        self.subject_txt.grid(row=2, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place entry in grid, spanning 5 columns

        self.content_txt = tkst.ScrolledText(window, width=48, height=6, wrap="word",
                                             bg=BG_TEXT, relief="flat")  # Create a scrollable text area with white background and no border
        self.content_txt.grid(row=3, column=0, columnspan=6, sticky="W", padx=10, pady=10)  # Place text area spanning all 6 columns at row 3

        # BUG FIX: removed the "New priority (1-5)" label and priority field — new messages
        # don't have a priority set by the user; that belongs in read_message.py only

        cancel_btn = tk.Button(window, text="Cancel", command=self.close,
                               bg=BTN_CANCEL, fg=BTN_FG, relief="flat", padx=6)  # Create a Cancel button with grey styling
        cancel_btn.grid(row=4, column=3, sticky="W", padx=10, pady=10)  # Place cancel button at row 4, col 3

        # BUG FIX: command was set to self.sender_txt (the Entry widget) instead of self.send_message (a method)
        send_btn = tk.Button(window, text="Send", command=self.send_message,
                             bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)  # Create a Send button with blue styling
        send_btn.grid(row=4, column=5, padx=10, pady=10)  # Place send button at row 4, col 5

        self.content_txt["state"] = "normal"  # Set the content text area state to normal (editable)

    def send_message(self):  # Method to collect form data and save the new message
        # BUG FIX: the original code had a method named sender_txt which conflicted with
        # the self.sender_txt Entry widget, and referenced self.message_id which was never defined.
        # This new method correctly reads the fields and calls message_manager.new_message().

        sender = self.sender_txt.get()  # Read the sender text from the From: entry field
        recipient = self.recipient_txt.get()  # Read the recipient text from the To: entry field
        subject = self.subject_txt.get()  # Read the subject text from the Subject: entry field
        content = self.content_txt.get("1.0", tk.END).strip()  # Read all content from the scrolled text area, stripping trailing whitespace

        # Validate that none of the required fields are empty before sending
        if sender == "" or recipient == "" or subject == "":
            messagebox.showerror("Error", "Please fill in From, To, and Subject fields")  # Show error popup if any required field is empty
            return  # Exit the method early without saving

        messages.new_message(sender, recipient, subject, content)  # Add the new message to the message manager database
        self.close()  # Close the New Message window after sending

    def close(self):  # Method to close the window
        self.window.destroy()  # Destroy the tkinter window


if __name__ == "__main__":  # Only runs when this file is run as a standalone
    window = tk.Tk()  # Create a TK root window object
    fonts.configure()  # Configure the fonts using the font_manager module
    NewMessage(window)  # Instantiate the NewMessage GUI with the window
    window.mainloop()  # Start the tkinter event loop, keeping the window open and reactive