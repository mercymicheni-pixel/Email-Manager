class Message:  # Define a class called Message to represent an email/message object
    def __init__(self, sender, subject, recipient, message, priority=0):  # Constructor taking sender, subject, recipient, message, and optional priority (defaults to 0)
        self.sender = sender  # Store the sender's name/address as an instance variable
        self.subject = subject  # Store the message subject as an instance variable
        self.recipient = recipient  # Store the recipient's name/address as an instance variable
        self.content = message  # Store the message body content as an instance variable
        self.label = ""  # Initialise the label as an empty string
        self.priority = priority  # Store the priority level as an instance variable
        self.unread = False  # Initialise the message as read (unread=False)

    def info(self):  # Method that returns a formatted summary string of the message
        return f"{self.stars():8} {self.sender:25} {self.label:5} {self.subject}"  # Return stars (padded to 8), sender (padded to 25), label (padded to 5), and subject

    def stars(self):  # Method that returns a string of asterisks representing the priority level
        stars = ""  # Initialise an empty string to hold the asterisks
        for i in range(self.priority):  # Loop once for each priority level (e.g. priority=3 gives 3 iterations)
            stars += "*"  # Append one asterisk per iteration
        return stars  # Return the completed string of asterisks