Teesside Casino - Game Suite
============================

https://github.com/7hr08ik/Casino

Authors:

- Rob Hickling
- Paul Leanca
- Sorin Sofronov
- James Young
- Viorica Anghel

Product Description
-------------------

This is Teesside Casino. It is a suite of 6 mini-games. 
1 unfinished project; Pinball.

The games themselves are in differing stages of completion. Each game was created by a separate developer, and the code is commented with the name of the developer responsible for its creation. Each game contains its own readme, whereas testing documentation is collected together in the testing folder.

Currently, Pinball, and Roulette are both considered proof-of-concept.

The player will be created with a starting balance of £1000. The player can walk around the lobby, and choose which game they wish to play. Upon entering the game, the player can gamble away at will. Upon exiting the game, the player will return to the lobby, with an updated player balance. 

The lobby is modular in the mini games available. In the 'integration_module' folder, is a .py file that contains functions required to bring an independently created python game/program into the lobby and its save/load system, allowing a user to have continuous gameplay across all games, with one cash balance.


Development Environment
-----------------------

- Operating System : Manjaro Linux 
- Python Version : 3.12.3
- IDE : Visual Studio Code
    - Plugins
        - Qodo Gen. Coding Autocomplete assistant.
        - Ruff Extension. Linter + Formatter.


Requirements
------------

- Python >= 3.6
- Pygame >= 2.6.1


Install Instructions
--------------------

Install Requirements:

- Python
    - https://www.python.org/downloads/

- Pygame (In terminal)
    - pip install pygame

- Git
    - git clone https://github.com/7hr08ik/Casino.git

- Manual
    - Download the project. 
    - Unpack/place the folder 'Casino' in the required location.
    - Run Casino/main.py


Usage Instructions
------------------

    These games were all created using VSCode, so it may be possible that some file path bugs occur.
    If this is the case, please open the Casino folder in VSCode, and run the main.py from there.

- Windows:
    - Open terminal in game folder
    - python -m main

- Linux (in terminal):
    - cd Casino
    - python3 -m main

- Platform agnostic
    - VSCode
        - Open Casino folder
        - Run main.py
    - IDLE
        - Open main.py in Idle
        - Run


Online Resources Used (Non-exhaustive)
--------------------------------------

Guide found through simple Google search
- https://medium.com/tomtalkspython/creating-your-first-game-in-pygame-865325b59df7

Guide used to get initial animation settings
- https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

Background image generated with free online AI image generator.

Image Files
- https://aske4.itch.io/antihero-character
- https://gamebetweenthelines.itch.io/2d-top-down-pixel-art-tileset-casino

Animation Help
- https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

UI Help
- Asked codiing assistant to prepare a framework for the UI module.
    - A basic menu system, with 2 buttons was created, and I expanded from there.
- Used the following links to help me fill out the methods.
    - https://www.geeksforgeeks.org/save-load-game-function-in-pygame/
    - https://coderslegacy.com/python/create-menu-screens-in-pygame-tutorial/

Json save Files
- https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

Delete aged files
- https://stackoverflow.com/questions/3345953/python-deleting-files-of-a-certain-age

 
Noted Bugs and missing features
-------------------------------

- For the lobby I would like to have the main lobby stay open in the background, and reload the players data when the window becomes active. 

- Currently the only feature implemented is the ability for each game to return to the lobby, but this simply closes the game, then runs the main.py again. It would have been good to have the player return to their last known postion, to keep the flow of the game.

- Audio would have been nice to get in, but due to deadline constraints it was not done.

- Mini-games are currently, unable to be played seperately. They must be launched through the Lobby. If we had more time, it would have been good to add lots of try/else blocks to make the games individually playable.
