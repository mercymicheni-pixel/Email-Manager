from message import Message  # Import the Message class from the message module

messages = {}  # Initialise an empty dictionary to store all messages, keyed by ID
messages[1] = Message("A.Tutor@grandwich.ac.uk", "Hello", "B.Tutor@grandwich.ac.uk", "How is the course going?", 2)  # Add message 1 with priority 2
messages[2] = Message("B.Tutor@grandwich.ac.uk", "Re: Hello", "A.Tutor@grandwich.ac.uk",
                      "> How is the course going?\n\nBrilliant, thanks. The students are all fantastic and are going to get top marks in their coursework.",
                      2)  # Add message 2 as a reply to message 1, with quoted content and priority 2
messages[3] = Message("A.Friend@kmail.com", "Coffee", "A.Tutor@grandwich.ac.uk",
                      "You're working too hard - fancy meeting for coffee?.", 5)  # Add message 3 from a friend with highest priority 5
messages[4] = Message("A.Tutor@grandwich.ac.uk", "Exam", "C.Tutor@grandwich.ac.uk",
                      "I have nearly finished writing the exam - I hope the students have revised hard.", 4)  # Add message 4 about an exam with priority 4
messages[5] = Message("A.Student@grandwich.ac.uk", "Timetable", "A.Tutor@grandwich.ac.uk",
                      "Dear Tutor,\n\nhelp!!! my timetable is rubbish - i cant understand it!!! please tell me what to do?\n\nfrom A.Student", 0)  # Add message 5 from a student with priority 0
messages[6] = Message("A.Tutor@grandwich.ac.uk", "Re: Timetable", "A.Student@grandwich.ac.uk",
                      "Please follow the advice on Moodle - all will be clear.", 0)  # Add message 6 as a reply to the timetable query with priority 0
messages[7] = Message("A.Student@grandwich.ac.uk", "Re: Timetable", "A.Tutor@grandwich.ac.uk", "thx :)", 0)  # Add message 7 as a short reply from the student with priority 0


def list_all(label=None):  # Define a function to list all messages, optionally filtered by label
    output = "ID Priority From                      Label Subject\n" \
             "== ======== ====                      ===== =======\n"  # Initialise the output string with a formatted header
    for message_id in messages:  # Loop through each message ID in the dictionary
        message = messages[message_id]  # Retrieve the Message object for the current ID
        if label is not None and (len(label) == 0 or label not in message.label):  # Skip message if label filter is set but doesn't match
            continue  # Move to the next message without adding this one to output
        output += f"{message_id:2d} {message.info()}\n"  # Append the message ID (2 digits) and its info string to output
    return output  # Return the complete formatted list as a string


def get_sender(message_id):  # Define a function to get the sender of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.sender  # Return the sender attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return None  # Return None if the message was not found


def get_recipient(message_id):  # Define a function to get the recipient of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.recipient  # Return the recipient attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return None  # Return None if the message was not found


def get_subject(message_id):  # Define a function to get the subject of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.subject  # Return the subject attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return None  # Return None if the message was not found


def get_content(message_id):  # Define a function to get the body content of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.content  # Return the content attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return None  # Return None if the message was not found


def get_priority(message_id):  # Define a function to get the priority of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.priority  # Return the priority attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return -1  # Return -1 as a sentinel value indicating the message was not found


def set_priority(message_id, priority):  # Define a function to update the priority of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        message.priority = priority  # Set the message's priority to the new value
    except KeyError:  # Handle the case where the message ID doesn't exist
        return  # Do nothing if the message was not found


def get_unread(message_id):  # Define a function to get the unread status of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        return message.unread  # Return the unread attribute
    except KeyError:  # Handle the case where the message ID doesn't exist
        return -1  # Return -1 as a sentinel value indicating the message was not found


def set_label(message_id, label):  # Define a function to set the label of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        message.label = label  # Set the message's label to the new value
    except KeyError:  # Handle the case where the message ID doesn't exist
        return  # Do nothing if the message was not found


def set_unread(message_id, unread):  # Define a function to set the unread status of a message by ID
    try:
        message = messages[message_id]  # Look up the message by ID
        message.unread = unread  # Set the message's unread status to the new value
    except KeyError:  # Handle the case where the message ID doesn't exist
        return  # Do nothing if the message was not found


def delete_message(message_id):  # Define a function to delete a message by ID
    messages.pop(message_id)  # Remove the message from the dictionary using its ID


def new_message(sender, recipient, subject, content):  # Define a function to create and add a new message
    # find the next empty message_id
    message_id = 0  # Initialise message_id to 0 as a starting value
    for message_id in messages:  # Iterate through all existing message IDs to find the last one
        continue  # Do nothing each iteration — just advance message_id to the last key
    message_id += 1  # Increment by 1 to get the next available message ID
    messages[message_id] = Message(sender, subject, recipient, content, 0)  # Create and store the new Message with priority 0