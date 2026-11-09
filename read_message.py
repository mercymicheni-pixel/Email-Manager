import tkinter as tk # import the tkinter library for building the GUI, aliased as tk
import tkinter.scrolledtext as tkst # Import the scrolledText widgets from tkinter, aliased as tkst

import message_manager as messages # import the custom message manager module, aliased as messages
import font_manager as fonts # import the custom font manager module, aliased as fonts


class ReadMessage(): # define a class called ReadMessageto encapsulate the read messages BUI
    """A GUI window for reading, updating the priority of, and deleting a message. """
    def __init__(self, window, message_id): # Define the constructor,taking a tkinter window and a message ID
        self.message_id = message_id # store the messages ID as an instance variable for use in other methods

        self.window = window # store the window references as an instance variable
        self.window.geometry("500x320") # set the window size to 500 pixels wide and 320 pixels tall 
        self.window.title(f"Read Message {message_id}") #set the window title to include the message ID

        sender_lbl = tk.Label(window, text="From:") # create a label widget with the text "from:"
        sender_lbl.grid(row=0, column=0, sticky="E", padx=10, pady=10) #place the label in row 0, column 0, aligned to the right

        self.sender_txt = tk.Entry(window, width=40) # create a text entry field for the sender, 40 characters wide
        self.sender_txt.grid(row=0, column=1, columnspan=5, sticky="W", padx=10, pady=10) #place the entry field in row 0, spanning 5 columns, aligned to the left

        recipient_lbl = tk.Label(window, text="To:")  # Create a label widget with the text "To:"
        recipient_lbl.grid(row=1, column=0, sticky="E", padx=10, pady=10) # Place the label in row 1, column 0, aligned to the right

        self.recipient_txt = tk.Entry(window, width=40)  # Create a text entry field for the recipient, 40 characters wide
        self.recipient_txt.grid(row=1, column=1, columnspan=5, sticky="W", padx=10, pady=10)  # Place the entry field in row 1, spanning 5 columns, aligned to the left

        subject_lbl = tk.Label(window, text="Subject:") # Create a label widget with the text "Subject:"
        subject_lbl.grid(row=2, column=0, sticky="E", padx=10, pady=10) # Place the label in row 2, column 0, aligned to the right

        self.subject_txt = tk.Entry(window, width=40) # Create a text entry field for the subject, 40 characters wide
        self.subject_txt.grid(row=2, column=1, columnspan=5, sticky="W", padx=10, pady=10) # Place the entry field in row 2, spanning 5 columns, aligned to the left


        self.content_txt = tkst.ScrolledText(window, width=48, height=6, wrap="word") # Create a scrollable text area, 48 chars wide, 6 lines tall, with word wrapping
        self.content_txt.grid(row=3, column=0, columnspan=6, sticky="W", padx=10, pady=10)  # Place the scrollable text area in row 3, spanning all 6 columns

        subject_lbl = tk.Label(window, text="New priority (1-5):")  # Create a label prompting the user to enter a new priority value
        subject_lbl.grid(row=4, column=0, columnspan=2, sticky="E", padx=10, pady=10)  # Place the label in row 4, spanning 2 columns, aligned to the right

        self.priority_txt = tk.Entry(window, width=3) # Create a small text entry field for the priority value, 3 characters wide
        self.priority_txt.grid(row=4, column=2, sticky="W", padx=10, pady=10) # Place the priority entry field in row 4, column 2, aligned to the left

        update_btn = tk.Button(window, text="Update", command=self.update_priority)  # Create an "Update" button that calls update_priority when clicked
        update_btn.grid(row=4, column=3, sticky="W", padx=10, pady=10)  # Place the Update button in row 4, column 3

        delete_btn = tk.Button(window, text="Delete", command=self.delete_message) # Create a "Delete" button that calls delete_message when clicked
        delete_btn.grid(row=4, column=4, padx=10, pady=10)  # Place the Delete button in row 4, column 4

        close_btn = tk.Button(window, text="Close", command=self.close) # Create a "Close" button that calls close when clicked
        close_btn.grid(row=4, column=5, padx=10, pady=10) # Place the Close button in row 4, column 5

        if message_id is not None: # Only attempt to load message data if a message ID was provided
            sender = messages.get_sender(message_id) # Fetch the sender of the message using its ID
            if sender is not None: # Only populate fields if the message was found in the system
                self.sender_txt.insert(tk.END, sender) # Insert the sender's name into the sender field
                self.sender_txt.configure(state='readonly')  # Make the sender field read-only to prevent editing
                self.recipient_txt.insert(tk.END, messages.get_recipient(message_id)) # Insert the recipient's name into the recipient field
                self.recipient_txt.configure(state='readonly') # Make the recipient field read-only to prevent editing
                self.subject_txt.insert(tk.END, messages.get_subject(message_id))  # Insert the message subject into the subject field
                self.subject_txt.configure(state='readonly') # Make the subject field read-only to prevent editing
                self.content_txt.insert(tk.END, messages.get_content(message_id)) # Insert the message body into the scrollable content area
            else:  # If the message ID did not match any existing message
                self.content_txt.insert(tk.END, 'No such message') # Display an error message in the content area
        self.content_txt["state"] = "disabled"  # Disable the content area to prevent the user from editing the message body

    def delete_message(self):  # Define the method to handle message deletion
        """delete the current message (if valid) and close the window."""
        if self.message_id is not None: # Only attempt deletion if a valid message ID exists
            messages.delete_message(self.message_id)  # Call the message manager to delete the message by ID
        self.close()  # Close the window after deletion

    def update_priority(self): # Define the method to handle priority updates
        """read the priority entry field and update the message's priority."""
        if self.message_id is not None: # Only attempt the update if a valid message ID exists
            messages.set_priority(self.message_id, int(self.priority_txt.get())) # Read the priority input, convert it to an integer, and update the message

    def close(self):  # Define the method to close the window
        """destroy the window, closing this view."""
        self.window.destroy() # Destroy the tkinter window, removing it from the screen


if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()  # create a TK object
    fonts.configure()  # configure the fonts
    ReadMessage(window, None)  # open the ReadMessage GUI
    window.mainloop()  # run the window main loop, reacting to button presses, etc
