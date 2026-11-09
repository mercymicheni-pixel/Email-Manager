# Email Manager Desktop Application

A Python-based desktop email management application developed using Tkinter and Object-Oriented Programming (OOP).

## Overview

The Email Manager is a desktop application that allows users to manage sample email messages through a graphical user interface. It was developed as an academic programming project to demonstrate object-oriented programming, application design and basic message-management functionality.

## Features

- View and search stored messages.
- Compose new messages.
- Read individual messages.
- Assign priority levels to messages.
- Add labels to messages.
- Filter messages by labels.
- Delete messages.
- Graphical user interface with interactive panels.

## Technologies Used

- Python
- Tkinter
- Object-Oriented Programming (OOP)
- Pytest for automated testing

## Project Structure

- `email_manager.py` – Main application interface.
- `message.py` – Message class and message attributes.
- `message_manager.py` – Message-management operations.
- `new_message.py` – Message composition interface.
- `read_message.py` – Message reading interface.
- `label_message.py` – Message labelling functionality.
- `font_manager.py` – Font configuration.
- `test_message.py` – Automated tests.

## Running the Application

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Run:

```bash
python email_manager.py
```

## Running Tests

Install pytest:

```bash
python -m pip install pytest
```

Run the automated tests:

```bash
python -m pytest -q
```

## Testing

The project includes 28 automated tests, which passed during the recovered project's initial test run.

## Learning Outcomes

This project provided practical experience in:

- Implementing classes, objects and methods.
- Organising a Python application into multiple modules.
- Developing graphical interfaces using Tkinter.
- Managing application data and user interactions.
- Writing and running automated tests.

## Limitations

This is an educational email-management simulation. It uses sample messages stored in memory and does not connect to external email services or provide actual email transmission or persistent storage.

---

Developed as an academic computing project.
