# Teesside Lottery

**Author:** Viorica Anghel

## Product Description

Teesside Lottery is an interactive lottery game built with Python and Pygame. Players can manually select their numbers, use a Lucky Dip for a random selection, save favorite number sets, and view the results of their draws. The game features a clean, intuitive interface and includes a history of recent draws, a rules screen, and a money pot to track winnings.

## Development Environment

- **IDE:** Visual Studio Code (VSCode)
- **OS:** Windows 10
- **Python Version:** 3.12

## Requirements

- **Python:** 3.12
- **Pygame:** 2.6.1

## Install Instructions

To set up the Teesside Lottery game in Visual Studio Code, follow these steps:

1. **Install Python 3.12**: Download and install Python 3.12 from [https://www.python.org/downloads/](https://www.python.org/downloads/). Ensure you check the box to add Python to your system’s PATH during installation.
2. **Install Visual Studio Code**: If you don’t already have VSCode, download and install it from [https://code.visualstudio.com/](https://code.visualstudio.com/).
3. **Add Python Extension**: Open VSCode, go to the Extensions view (Ctrl+Shift+X), search for "Python" by Microsoft, and install it for IntelliSense and debugging support.
4. **Install Pygame**: Open a terminal in VSCode (View > Terminal) and run the following command:
5. **Get the Project Files**: Clone this repository or download the ZIP file and extract it to a folder on your machine.
6. **Open in VSCode**: In VSCode, go to `File > Open Folder` and select the project folder.

## Usage Instructions

To run the Teesside Lottery game in Visual Studio Code, follow these steps:

1. **Open the Project**: Open the project folder in VSCode (File > Open Folder).
2. **Set Python Interpreter**: Ensure the Python interpreter is set to version 3.12. Click the Python version in the bottom-left corner of VSCode and select the 3.12 interpreter from the list.
3. **Open the Main Script**: In the VSCode editor, open the `main.py` file.
4. **Run the Game**: 
- Option 1: Click the green "Run" button in the top-right corner of VSCode.
- Option 2: Open the terminal in VSCode (View > Terminal) and type:
5. **Play the Game**: Use the on-screen buttons to navigate, select numbers, and enjoy the lottery experience.

## Resources Used

- **Background Image**: Sourced from Google Images https://images.google.com

- **Tutorials**:
- **W3Schools Python Tutorial**: A comprehensive guide to Python basics ([https://www.w3schools.com/python/](https://www.w3schools.com/python/)).
- **Pygame Documentation**: Official documentation for Pygame, covering its functions and features ([https://www.pygame.org/docs/](https://www.pygame.org/docs/)).
- **Real Python - Pygame: A Primer on Game Programming in Python**: A detailed tutorial on building games with Pygame ([https://realpython.com/pygame-a-primer/](https://realpython.com/pygame-a-primer/)).
- **Pygame Tutorials**: https://www.pygame.org/wiki/tutorials

## Noted Bugs and Missing Features

- The game may crash after playing over 350 times due to a memory issue. Restarting the game resolves this.
- When editing favorite number sets, players must reset all numbers instead of editing them individually.
- If the `favs.txt` file contains invalid data (e.g., non-numeric entries), the game may crash. Ensure the file is correctly formatted.
- A confirmation dialogue for deleting favorites is missing, which could lead to accidental deletions.