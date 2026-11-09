import tkinter as tk  # Import tkinter library for GUI, aliased as 'tk'
import tkinter.scrolledtext as tkst  # Import scrolledtext widget from tkinter, aliased as 'tkst'
from tkinter import messagebox  # Import messagebox from tkinter for popup dialogs

import message_manager as messages  # Import custom message_manager module, aliased as 'messages'
import font_manager as fonts  # Import custom font_manager module, aliased as 'fonts'

# --- Colour scheme ---
# All colours are defined here so they are easy to change in one place
BG_MAIN = "#f0f4f8"       # Light blue-grey background for the main window
BG_TEXT = "#ffffff"       # White background for text/entry fields
BG_DETAIL = "#f8fafc"     # Slightly off-white background for the detail panel
BTN_PRIMARY = "#4a7fc1"   # Medium blue for main action buttons
BTN_DANGER = "#c0392b"    # Red for destructive actions like Delete
BTN_NEUTRAL = "#888888"   # Grey for secondary actions like Close/Cancel
BTN_FG = "#ffffff"        # White text on all buttons
LBL_FG = "#333333"        # Dark text for labels
HEADING_FG = "#1a3a5c"    # Dark navy for section headings
DIVIDER = "#d0dce8"       # Soft blue-grey for separator lines


def set_text(text_area, content):  # Define a helper function to safely update a disabled text area
    text_area["state"] = "normal"  # Enable the text area so it can be edited programmatically
    text_area.delete("1.0", tk.END)  # Clear all existing content from the text area
    text_area.insert(1.0, content)  # Insert the new content starting at the first line
    text_area["state"] = "disabled"  # Disable the text area again to prevent user edits


class EmailManager():  # Define the main EmailManager class — Innovation 1: single combined GUI
    def __init__(self, window):  # Constructor method, takes a tkinter window as argument
        self.window = window  # Store the window reference as an instance variable
        self.window.geometry("780x680")  # Set the window size to 780x680 pixels
        self.window.title("Email Manager")  # Set the window title
        self.window.configure(bg=BG_MAIN)  # Apply the main background colour to the window
        self.window.resizable(True, True)  # Allow the window to be resized by the user

        # ── INNOVATION 1: COMBINED GUI ─────────────────────────────────────
        # Rather than opening separate windows for each action, everything is
        # handled inside this single window. The detail panel at the bottom
        # expands and collapses depending on what the user is doing (reading,
        # composing, or labelling), replacing the need for new_message.py,
        # read_message.py, and label_messages.py to open as separate windows.
        # ──────────────────────────────────────────────────────────────────

        # === ROW 0: Top toolbar ===
        toolbar = tk.Frame(window, bg=BG_MAIN)  # Create a frame to hold all toolbar buttons
        toolbar.grid(row=0, column=0, sticky="EW", padx=10, pady=(10, 4))  # Place toolbar at the top

        list_btn = tk.Button(toolbar, text="Refresh", command=self.list_messages,
                             bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8, pady=4)  # Refresh list button
        list_btn.pack(side="left", padx=(0, 6))  # Pack to the left

        new_btn = tk.Button(toolbar, text="New Message", command=self.show_compose_panel,
                            bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8, pady=4)  # Open compose panel button
        new_btn.pack(side="left", padx=6)  # Pack to the left

        read_btn = tk.Button(toolbar, text="Read", command=self.show_read_panel,
                             bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8, pady=4)  # Open read panel button
        read_btn.pack(side="left", padx=6)  # Pack to the left

        self.read_id_txt = tk.Entry(toolbar, width=4, bg=BG_TEXT)  # Entry for the message ID to read
        self.read_id_txt.pack(side="left", padx=(0, 6))  # Pack next to the Read button

        label_btn = tk.Button(toolbar, text="Labels", command=self.show_label_panel,
                              bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8, pady=4)  # Open label panel button
        label_btn.pack(side="left", padx=6)  # Pack to the left

        # === ROW 1: INNOVATION 2 — Search bar ===
        # Filters the message list by sender when Search is pressed.
        # Clear restores the full list. The result count is shown inline.
        search_frame = tk.Frame(window, bg=BG_MAIN)  # Frame to hold all search widgets
        search_frame.grid(row=1, column=0, sticky="EW", padx=10, pady=(0, 4))  # Place below toolbar

        search_lbl = tk.Label(search_frame, text="Search by sender:", bg=BG_MAIN, fg=LBL_FG)  # Search label
        search_lbl.pack(side="left", padx=(0, 6))  # Pack to the left

        self.search_txt = tk.Entry(search_frame, width=30, bg=BG_TEXT)  # Entry for the sender search query
        self.search_txt.pack(side="left", padx=(0, 6))  # Pack next to the label
        self.search_txt.bind("<Return>", lambda e: self.search_messages())  # Pressing Enter triggers the search

        search_btn = tk.Button(search_frame, text="Search", command=self.search_messages,
                               bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8, pady=2)  # Search button
        search_btn.pack(side="left", padx=(0, 6))  # Pack to the left

        clear_btn = tk.Button(search_frame, text="Clear", command=self.clear_search,
                              bg=BTN_NEUTRAL, fg=BTN_FG, relief="flat", padx=8, pady=2)  # Clear search button
        clear_btn.pack(side="left")  # Pack to the left

        self.search_status_lbl = tk.Label(search_frame, text="", bg=BG_MAIN, fg=HEADING_FG)  # Shows result count
        self.search_status_lbl.pack(side="left", padx=10)  # Pack next to Clear

        # === ROW 2: Message list ===
        self.list_txt = tkst.ScrolledText(window, width=80, height=10, wrap="none",
                                          bg=BG_TEXT, relief="flat", font=("Courier", 10))  # Monospace for column alignment
        self.list_txt.grid(row=2, column=0, sticky="EW", padx=10, pady=4)  # Place below search bar

        # === ROW 3: Status label ===
        self.status_lbl = tk.Label(window, text="", bg=BG_MAIN, fg="#555555",
                                   font=("Helvetica", 10))  # Status bar for feedback messages
        self.status_lbl.grid(row=3, column=0, sticky="W", padx=10, pady=(0, 2))  # Place below message list

        # === ROW 4: Divider line ===
        divider = tk.Frame(window, height=2, bg=DIVIDER)  # Thin horizontal separator line
        divider.grid(row=4, column=0, sticky="EW", padx=10, pady=4)  # Place as full-width divider

        # === ROW 5: Detail panel heading ===
        self.detail_heading = tk.Label(window, text="", bg=BG_MAIN, fg=HEADING_FG,
                                       font=("Arial", 11, "bold"))  # Heading for the active detail panel
        self.detail_heading.grid(row=5, column=0, sticky="W", padx=14, pady=(4, 0))  # Place above detail panel

        # === ROW 6: Detail panel ===
        # This frame's contents change depending on whether the user is
        # reading, composing, or labelling — no separate windows needed.
        self.detail_frame = tk.Frame(window, bg=BG_DETAIL)  # Container for the swappable detail panel content
        self.detail_frame.grid(row=6, column=0, sticky="EW", padx=10, pady=(4, 10))  # Place at the bottom

        window.columnconfigure(0, weight=1)  # Allow column 0 to stretch horizontally on resize
        window.rowconfigure(2, weight=1)  # Allow the message list to stretch vertically on resize

        self.list_messages()  # Populate the message list automatically on startup

    # ── MESSAGE LIST ────────────────────────────────────────────────────

    def list_messages(self):  # Method to display all messages in the list area
        message_list = messages.list_all()  # Retrieve the full formatted message list
        set_text(self.list_txt, message_list)  # Update the text area
        self.search_txt.delete(0, tk.END)  # Clear the search field
        self.search_status_lbl.configure(text="")  # Clear the search result count
        self.status_lbl.configure(text="Message list refreshed.")  # Update the status bar

    # ── INNOVATION 2: SEARCH BY SENDER ──────────────────────────────────
    # search_messages() iterates through all messages in message_manager and
    # checks whether the search query appears in the sender field (case-insensitive).
    # Only matching messages are shown in the list. The result count is displayed
    # next to the search bar. clear_search() restores the full unfiltered list.

    def search_messages(self):  # Method to filter the message list by sender name
        query = self.search_txt.get().strip().lower()  # Read and lowercase the search query

        if query == "":  # Check if the search field is empty
            messagebox.showerror("Error", "Please enter a sender name to search for")  # Show error popup
            return  # Exit early

        # Build the filtered output using the same header format as list_all()
        output = "ID Priority From                      Label Subject\n" \
                 "== ======== ====                      ===== =======\n"

        count = 0  # Counter for the number of matching messages
        for message_id in messages.messages:  # Loop through every message ID in the dictionary
            sender = messages.get_sender(message_id)  # Get the sender for this message
            if sender is not None and query in sender.lower():  # Case-insensitive match check
                msg = messages.messages[message_id]  # Retrieve the Message object
                output += f"{message_id:2d} {msg.info()}\n"  # Append the formatted message line
                count += 1  # Increment the match counter

        set_text(self.list_txt, output)  # Display the filtered results in the list area

        if count == 0:
            self.search_status_lbl.configure(text="No results found.")  # Show no-results message
        else:
            self.search_status_lbl.configure(text=f"{count} message(s) found.")  # Show result count

        self.status_lbl.configure(text=f"Showing messages from senders matching '{query}'.")  # Update status bar

    def clear_search(self):  # Method to clear the search and restore the full message list
        self.search_txt.delete(0, tk.END)  # Clear the search entry
        self.search_status_lbl.configure(text="")  # Clear the result count label
        self.list_messages()  # Reload the full unfiltered list

    # ── DETAIL PANEL HELPERS ─────────────────────────────────────────────

    def clear_detail_panel(self):  # Method to destroy all widgets in the detail panel
        for widget in self.detail_frame.winfo_children():  # Loop through all child widgets
            widget.destroy()  # Destroy each one to fully clear the panel

    # ── READ PANEL ───────────────────────────────────────────────────────

    def show_read_panel(self):  # Method to show the read message panel in the detail area
        message_id_string = self.read_id_txt.get()  # Read the message ID from the toolbar entry

        if not message_id_string.isdigit():  # Validate: must be a number (catches empty string and 'four' etc.)
            messagebox.showerror("Error", "Please enter a valid numeric message ID in the box next to Read")
            return  # Exit early

        message_id = int(message_id_string)  # Convert to integer after validation

        if messages.get_sender(message_id) is None:  # Check the message actually exists
            messagebox.showerror("Error", f"No message found with ID {message_id}")
            return  # Exit early

        self.clear_detail_panel()  # Clear the panel before populating
        self.detail_heading.configure(text=f"Reading Message {message_id}")  # Set the heading

        frame = self.detail_frame  # Shorthand

        # Display From, To, Subject as read-only labels
        fields = [
            ("From:", messages.get_sender(message_id)),
            ("To:", messages.get_recipient(message_id)),
            ("Subject:", messages.get_subject(message_id)),
        ]
        for i, (label_text, value) in enumerate(fields):  # Loop through and render each field row
            lbl = tk.Label(frame, text=label_text, bg=BG_DETAIL, fg=LBL_FG, width=10, anchor="e")
            lbl.grid(row=i, column=0, sticky="E", padx=(10, 4), pady=4)
            val_lbl = tk.Label(frame, text=value, bg=BG_DETAIL, fg=LBL_FG, anchor="w")
            val_lbl.grid(row=i, column=1, columnspan=4, sticky="W", padx=4, pady=4)

        # Message body in a read-only scrolled text area
        content_lbl = tk.Label(frame, text="Content:", bg=BG_DETAIL, fg=LBL_FG, anchor="e", width=10)
        content_lbl.grid(row=3, column=0, sticky="NE", padx=(10, 4), pady=4)
        content_area = tkst.ScrolledText(frame, width=60, height=4, wrap="word", bg=BG_TEXT, relief="flat")
        content_area.grid(row=3, column=1, columnspan=4, sticky="W", padx=4, pady=4)
        content_area.insert("1.0", messages.get_content(message_id))  # Insert the message body
        content_area["state"] = "disabled"  # Make content read-only

        # Priority update row
        pri_lbl = tk.Label(frame, text="Priority:", bg=BG_DETAIL, fg=LBL_FG, anchor="e", width=10)
        pri_lbl.grid(row=4, column=0, sticky="E", padx=(10, 4), pady=4)
        self.new_priority_txt = tk.Entry(frame, width=4, bg=BG_TEXT)
        self.new_priority_txt.grid(row=4, column=1, sticky="W", padx=4, pady=4)
        self.new_priority_txt.insert(0, str(messages.get_priority(message_id)))  # Pre-fill with current priority

        update_btn = tk.Button(frame, text="Update Priority",
                               command=lambda: self.update_priority(message_id),
                               bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)
        update_btn.grid(row=4, column=2, padx=6, pady=4)

        delete_btn = tk.Button(frame, text="Delete Message",
                               command=lambda: self.delete_message(message_id),
                               bg=BTN_DANGER, fg=BTN_FG, relief="flat", padx=6)  # Red delete button
        delete_btn.grid(row=4, column=3, padx=6, pady=4)

        close_btn = tk.Button(frame, text="Close", command=self.close_detail_panel,
                              bg=BTN_NEUTRAL, fg=BTN_FG, relief="flat", padx=6)
        close_btn.grid(row=4, column=4, padx=6, pady=4)

        self.status_lbl.configure(text=f"Reading message {message_id}.")  # Update status bar

    def update_priority(self, message_id):  # Method to update the priority of the currently viewed message
        priority_string = self.new_priority_txt.get()  # Read the priority entry

        if not priority_string.isdigit() or not (1 <= int(priority_string) <= 5):  # Validate range 1-5
            messagebox.showerror("Error", "Priority must be a number between 1 and 5")
            return  # Exit early

        messages.set_priority(message_id, int(priority_string))  # Save the new priority
        self.status_lbl.configure(text=f"Priority of message {message_id} updated to {priority_string}.")

    def delete_message(self, message_id):  # Method to delete the currently viewed message
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete message {message_id}?")  # Confirm dialog
        if confirm:  # Only proceed if the user clicked Yes
            messages.delete_message(message_id)  # Remove the message
            self.close_detail_panel()  # Hide the detail panel
            self.list_messages()  # Refresh the list
            self.status_lbl.configure(text=f"Message {message_id} deleted.")

    # ── COMPOSE PANEL ────────────────────────────────────────────────────

    def show_compose_panel(self):  # Method to show the new message compose panel
        self.clear_detail_panel()  # Clear the detail panel
        self.detail_heading.configure(text="New Message")  # Set the heading

        frame = self.detail_frame  # Shorthand

        fields = [("From:", "sender"), ("To:", "recipient"), ("Subject:", "subject")]  # Field definitions
        self.compose_entries = {}  # Store entry widget references by name

        for i, (label_text, key) in enumerate(fields):  # Render each labelled entry field
            lbl = tk.Label(frame, text=label_text, bg=BG_DETAIL, fg=LBL_FG, width=10, anchor="e")
            lbl.grid(row=i, column=0, sticky="E", padx=(10, 4), pady=4)
            entry = tk.Entry(frame, width=55, bg=BG_TEXT)
            entry.grid(row=i, column=1, columnspan=4, sticky="W", padx=4, pady=4)
            self.compose_entries[key] = entry  # Store the entry widget

        # Content area
        content_lbl = tk.Label(frame, text="Content:", bg=BG_DETAIL, fg=LBL_FG, anchor="e", width=10)
        content_lbl.grid(row=3, column=0, sticky="NE", padx=(10, 4), pady=4)
        self.compose_content = tkst.ScrolledText(frame, width=55, height=4, wrap="word",
                                                 bg=BG_TEXT, relief="flat")
        self.compose_content.grid(row=3, column=1, columnspan=4, sticky="W", padx=4, pady=4)

        send_btn = tk.Button(frame, text="Send", command=self.send_message,
                             bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=8)
        send_btn.grid(row=4, column=3, padx=6, pady=6)

        cancel_btn = tk.Button(frame, text="Cancel", command=self.close_detail_panel,
                               bg=BTN_NEUTRAL, fg=BTN_FG, relief="flat", padx=8)
        cancel_btn.grid(row=4, column=4, padx=6, pady=6)

        self.status_lbl.configure(text="Composing a new message.")

    def send_message(self):  # Method to validate and save the composed message
        sender = self.compose_entries["sender"].get()  # Read the From field
        recipient = self.compose_entries["recipient"].get()  # Read the To field
        subject = self.compose_entries["subject"].get()  # Read the Subject field
        content = self.compose_content.get("1.0", tk.END).strip()  # Read the content area

        if sender == "" or recipient == "" or subject == "":  # Validate required fields are not empty
            messagebox.showerror("Error", "Please fill in the From, To, and Subject fields")
            return  # Exit early

        messages.new_message(sender, recipient, subject, content)  # Save the new message
        self.close_detail_panel()  # Hide the compose panel
        self.list_messages()  # Refresh the list to show the new message
        self.status_lbl.configure(text="Message sent successfully.")

    # ── LABEL PANEL ──────────────────────────────────────────────────────

    def show_label_panel(self):  # Method to show the label management panel
        self.clear_detail_panel()  # Clear the detail panel
        self.detail_heading.configure(text="Label Messages")  # Set the heading

        frame = self.detail_frame  # Shorthand

        id_lbl = tk.Label(frame, text="Message ID:", bg=BG_DETAIL, fg=LBL_FG, anchor="e", width=14)
        id_lbl.grid(row=0, column=0, sticky="E", padx=(10, 4), pady=6)
        self.label_id_txt = tk.Entry(frame, width=6, bg=BG_TEXT)  # Entry for message ID
        self.label_id_txt.grid(row=0, column=1, sticky="W", padx=4, pady=6)

        label_lbl = tk.Label(frame, text="Label:", bg=BG_DETAIL, fg=LBL_FG, anchor="e", width=14)
        label_lbl.grid(row=1, column=0, sticky="E", padx=(10, 4), pady=6)
        self.label_name_txt = tk.Entry(frame, width=20, bg=BG_TEXT)  # Entry for the label text
        self.label_name_txt.grid(row=1, column=1, columnspan=2, sticky="W", padx=4, pady=6)

        add_btn = tk.Button(frame, text="Add Label to Message", command=self.add_label,
                            bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)
        add_btn.grid(row=2, column=0, columnspan=2, padx=(14, 6), pady=6, sticky="W")

        list_btn = tk.Button(frame, text="List All Messages Labelled", command=self.list_labelled,
                             bg=BTN_PRIMARY, fg=BTN_FG, relief="flat", padx=6)
        list_btn.grid(row=2, column=2, columnspan=2, padx=6, pady=6, sticky="W")

        close_btn = tk.Button(frame, text="Close", command=self.close_detail_panel,
                              bg=BTN_NEUTRAL, fg=BTN_FG, relief="flat", padx=6)
        close_btn.grid(row=2, column=4, padx=6, pady=6)

        self.label_output = tkst.ScrolledText(frame, width=70, height=5, wrap="word",
                                              bg=BG_TEXT, relief="flat")  # Output area for label search results
        self.label_output.grid(row=3, column=0, columnspan=5, sticky="W", padx=10, pady=6)

        self.status_lbl.configure(text="Label panel open.")

    def add_label(self):  # Method to add a label to a message from the label panel
        message_id_string = self.label_id_txt.get()  # Read the message ID entry

        if not message_id_string.isdigit():  # Validate: must be a number
            messagebox.showerror("Error", "Please enter a valid numeric message ID")
            return

        message_id = int(message_id_string)  # Convert to integer
        label = self.label_name_txt.get()  # Read the label entry

        if label == "":  # Check label is not empty
            messagebox.showerror("Error", "Label cannot be empty")
            return

        if messages.get_sender(message_id) is None:  # Check the message exists
            messagebox.showerror("Error", f"No message found with ID {message_id}")
            return

        messages.set_label(message_id, label)  # Apply the label
        self.label_output.insert(tk.END, f"Label '{label}' added to message {message_id}\n")  # Show success
        self.status_lbl.configure(text=f"Label '{label}' applied to message {message_id}.")

    def list_labelled(self):  # Method to list all messages matching the entered label
        label = self.label_name_txt.get()  # Read the label entry

        if label == "":  # Check label is not empty
            messagebox.showerror("Error", "Please enter a label to search for")
            return

        result = messages.list_all(label)  # Get the filtered message list
        self.label_output.delete("1.0", tk.END)  # Clear the output area
        self.label_output.insert(tk.END, result)  # Display results

    # ── PANEL CLOSE ──────────────────────────────────────────────────────

    def close_detail_panel(self):  # Method to hide the detail panel and reset the heading
        self.clear_detail_panel()  # Remove all panel widgets
        self.detail_heading.configure(text="")  # Clear the heading
        self.status_lbl.configure(text="")  # Clear the status bar


if __name__ == "__main__":  # Only runs when this file is run as a standalone
    window = tk.Tk()  # Create a TK root window object
    fonts.configure()  # Configure the fonts using the font_manager module
    EmailManager(window)  # Instantiate the combined EmailManager GUI
    window.mainloop()  # Start the tkinter event loop