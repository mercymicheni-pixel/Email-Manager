import pytest  # Import pytest framework for running unit tests
from message import Message  # Import the Message class from message.py to be tested
import message_manager as mm  # Import message_manager to test its functions


# ============================================================
# TESTS FOR: message.py — the Message class
# ============================================================

# --- Tests for the Message constructor (__init__) ---

def test_sender_stored_correctly():  # Test that the sender is saved properly
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a Message with sender "Alice"
    assert msg.sender == "Alice"  # Check that the sender attribute equals "Alice"

def test_recipient_stored_correctly():  # Test that the recipient is saved properly
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a Message with recipient "Bob"
    assert msg.recipient == "Bob"  # Check that the recipient attribute equals "Bob"

def test_subject_stored_correctly():  # Test that the subject is saved properly
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a Message with subject "Hello"
    assert msg.subject == "Hello"  # Check that the subject attribute equals "Hello"

def test_content_stored_correctly():  # Test that the message body is saved properly
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a Message with content "How are you?"
    assert msg.content == "How are you?"  # Check that the content attribute equals "How are you?"

def test_default_priority_is_zero():  # Test that priority defaults to 0 when not provided
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a Message without specifying priority
    assert msg.priority == 0  # Check that priority defaults to 0

def test_custom_priority_stored():  # Test that a custom priority value is saved properly
    msg = Message("Alice", "Hello", "Bob", "How are you?", priority=3)  # Create a Message with priority 3
    assert msg.priority == 3  # Check that the priority attribute equals 3

def test_label_initialised_as_empty_string():  # Test that label starts as an empty string
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a new Message
    assert msg.label == ""  # Check that label is initialised to an empty string

def test_unread_initialised_as_false():  # Test that unread starts as False (message begins as read)
    msg = Message("Alice", "Hello", "Bob", "How are you?")  # Create a new Message
    assert msg.unread == False  # Check that unread is initialised to False


# --- Tests for the stars() method ---

def test_stars_returns_empty_string_for_priority_zero():  # Test that priority 0 gives no asterisks
    msg = Message("Alice", "Hello", "Bob", "Content", priority=0)  # Create a Message with priority 0
    assert msg.stars() == ""  # Check that stars() returns an empty string

def test_stars_returns_one_star_for_priority_one():  # Test that priority 1 gives exactly one asterisk
    msg = Message("Alice", "Hello", "Bob", "Content", priority=1)  # Create a Message with priority 1
    assert msg.stars() == "*"  # Check that stars() returns a single asterisk

def test_stars_returns_three_stars_for_priority_three():  # Test that priority 3 gives three asterisks
    msg = Message("Alice", "Hello", "Bob", "Content", priority=3)  # Create a Message with priority 3
    assert msg.stars() == "***"  # Check that stars() returns exactly three asterisks

def test_stars_returns_five_stars_for_priority_five():  # Test that priority 5 gives five asterisks
    msg = Message("Alice", "Hello", "Bob", "Content", priority=5)  # Create a Message with priority 5
    assert msg.stars() == "*****"  # Check that stars() returns exactly five asterisks

def test_stars_length_matches_priority():  # Test that the length of stars() always matches the priority value
    msg = Message("Alice", "Hello", "Bob", "Content", priority=4)  # Create a Message with priority 4
    assert len(msg.stars()) == msg.priority  # Check that the number of asterisks equals the priority number


# --- Tests for the info() method ---

def test_info_contains_sender():  # Test that info() includes the sender name
    msg = Message("Alice", "Hello", "Bob", "Content", priority=2)  # Create a Message with sender "Alice"
    assert "Alice" in msg.info()  # Check that "Alice" appears somewhere in the info string

def test_info_contains_subject():  # Test that info() includes the subject
    msg = Message("Alice", "Hello", "Bob", "Content", priority=2)  # Create a Message with subject "Hello"
    assert "Hello" in msg.info()  # Check that "Hello" appears somewhere in the info string

def test_info_contains_stars():  # Test that info() includes the asterisk priority representation
    msg = Message("Alice", "Hello", "Bob", "Content", priority=3)  # Create a Message with priority 3
    assert "***" in msg.info()  # Check that three asterisks appear in the info string

def test_info_contains_label():  # Test that info() includes the label when one is set
    msg = Message("Alice", "Hello", "Bob", "Content", priority=1)  # Create a Message
    msg.label = "ToDo"  # Manually set the label to "ToDo"
    assert "ToDo" in msg.info()  # Check that "ToDo" appears in the info string

def test_info_returns_string():  # Test that info() returns a string type
    msg = Message("Alice", "Hello", "Bob", "Content")  # Create a basic Message
    assert type(msg.info()) == str  # Check that the return type is a string


# ============================================================
# TESTS FOR: message_manager.py
# ============================================================

# --- Tests for get_sender() ---

def test_get_sender_returns_correct_sender():  # Test that get_sender returns the right sender for a known ID
    assert mm.get_sender(1) == "A.Tutor@grandwich.ac.uk"  # Message 1 should have this sender

def test_get_sender_returns_none_for_invalid_id():  # Test that get_sender returns None for a non-existent message ID
    assert mm.get_sender(999) is None  # ID 999 does not exist so None should be returned


# --- Tests for get_recipient() ---

def test_get_recipient_returns_correct_recipient():  # Test that get_recipient returns the right recipient for a known ID
    assert mm.get_recipient(1) == "B.Tutor@grandwich.ac.uk"  # Message 1 should have this recipient

def test_get_recipient_returns_none_for_invalid_id():  # Test that get_recipient returns None for a non-existent message ID
    assert mm.get_recipient(999) is None  # ID 999 does not exist so None should be returned


# --- Tests for get_priority() and set_priority() ---

def test_get_priority_returns_correct_value():  # Test that get_priority returns the right value for a known ID
    assert mm.get_priority(3) == 5  # Message 3 (coffee) has priority 5

def test_get_priority_returns_minus_one_for_invalid_id():  # Test that get_priority returns -1 for a non-existent ID
    assert mm.get_priority(999) == -1  # ID 999 does not exist so -1 sentinel should be returned

def test_set_priority_updates_correctly():  # Test that set_priority actually changes the stored priority
    mm.set_priority(1, 4)  # Update message 1's priority from 2 to 4
    assert mm.get_priority(1) == 4  # Check the priority has been updated to 4
    mm.set_priority(1, 2)  # Reset message 1's priority back to 2 to avoid affecting other tests


# --- Tests for set_label() ---

def test_set_label_updates_correctly():  # Test that set_label stores the label on the correct message
    mm.set_label(1, "ToDo")  # Set label "ToDo" on message 1
    assert mm.messages[1].label == "ToDo"  # Check the label was stored correctly
    mm.set_label(1, "")  # Reset the label back to empty so other tests are not affected


# --- Tests for new_message() ---

def test_new_message_adds_to_messages():  # Test that new_message() creates a new entry in the messages dictionary
    count_before = len(mm.messages)  # Count how many messages exist before adding
    mm.new_message("Test@test.com", "Recipient@test.com", "Test Subject", "Test Content")  # Add a new message
    assert len(mm.messages) == count_before + 1  # Check the dictionary now has one more message

def test_new_message_stored_with_correct_sender():  # Test that the new message stores the sender correctly
    last_id = max(mm.messages.keys())  # Get the ID of the most recently added message
    assert mm.get_sender(last_id) == "Test@test.com"  # Check the sender matches what was passed in