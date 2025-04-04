Teesside Lottery
================

Author:    
- Viorica Anghel

Product Description
----------------------

Teesside Lottery is an interactive lottery game built with Python and Pygame. Players can manually select their numbers, use a Lucky Dip for a random selection, save favorite number sets, and view the results of their draws. The game features a clean, intuitive interface and includes a history of recent draws, a rules screen, and a money pot to track winnings.

Development Environment
-----------------------

- **IDE:** Visual Studio Code (VSCode)
- **OS:** Windows 10
- **Python Version:** 3.12

Requirements
------------

- Python >= 3.6
- Pygame >= 2.6.1

Install Instructions
--------------------

This game has been fully integrated into the lobby suite.
Installation is handled as part of the full project

Usage Instructions
------------------

Game is run from the main lobby. 
Open the lobby, and walk to the `Lottery` target to begin this game.

Resources Used
--------------

- **Background Image**: Sourced from Google Images https://images.google.com

- **Tutorials**:
    - **W3Schools Python Tutorial**: A comprehensive guide to Python basics ([https://www.w3schools.com/python/](https://www.w3schools.com/python/)).
    - **Pygame Documentation**: Official documentation for Pygame, covering its functions and features ([https://www.pygame.org/docs/](https://www.pygame.org/docs/)).
    - **Real Python - Pygame: A Primer on Game Programming in Python**: A detailed tutorial on building games with Pygame ([https://realpython.com/pygame-a-primer/](https://realpython.com/pygame-a-primer/)).
    - **Pygame Tutorials**: https://www.pygame.org/wiki/tutorials

Noted Bugs and Missing Features
-------------------------------

- The game may crash after playing over 350 times due to a memory issue. Restarting the game resolves this.
- When editing favorite number sets, players must reset all numbers instead of editing them individually.
- If the `favs.txt` file contains invalid data (e.g., non-numeric entries), the game may crash. Ensure the file is correctly formatted.
- A confirmation dialogue for deleting favorites is missing, which could lead to accidental deletions.