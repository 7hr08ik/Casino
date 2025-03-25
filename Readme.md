Teesside Casino - Game Suite
============================

Authors: R Hickling, 
         P Leanca, 
         S Sofronov, 
         J Young, 
         V Anghel

Product Description
-------------------

This is Teesside Casino. It is a suite of 7 games.
The games themselves are in differing stages of completion. Each game was created by a seperate devleoper, and the code is commented with the name of the developer responsible for its creation.
Each game folder, contains its own 'docs' folder with the relevant readme and testing documentation.

The player will be created with a starting balance of £1000. The player can walk around the lobby, and choose which game they wish to play. Upon entering the game, the player can gamble away at will. Upon exiting the game, the player will return to the lobby, with an updated player balance. 

The lobby is modular in the mini games available. In the 'integration_module' folder, is a .py file that contains functions required to bring an independantly created python game/program into the lobby and its save/load system, allowing a user to have continuous gameplay across all games, with one cash balance.



Development Environment
-----------------------

    Operating System : Manjaro Linux 

    Python Version : 3.12.3

    IDE : Visual Studio Code
        Plugins
            Codeium. Coding Autocomplete assistant.
            Ruff Extension. Formatting and error highlighting.


Requirements
------------

    Python >= 3.6
    Pygame >= 2.6.1


Install Instructions
--------------------

    PyGame: in a terminal run 'pip install pygame'

    Download the project. Unpack/place the folder 'Casino' in the required location.
    Run Casino/main.py

Usage Instructions
------------------

Windows:

    Run the 'Casino/main.py'

Linux:

    CD inside the /Casino directory
    
    Check file permissions:        
        -: chmod +x

    Run game:        
        -: python3 -m main


Online Resources Used
(Non-exhaustive)
---------------------

Guide found through simple Google search
    https://medium.com/tomtalkspython/creating-your-first-game-in-pygame-865325b59df7

Guide used to get initial animation settings
    https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

Background image generated with free online AI image generator.

Image Files
    https://aske4.itch.io/antihero-character
    https://gamebetweenthelines.itch.io/2d-top-down-pixel-art-tileset-casino

Animation Help
    https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

UI Help
    Asked codiing assistant to prepare a framework for the UI module.
        Used the following links to help me fill out the methods.
    https://www.geeksforgeeks.org/save-load-game-function-in-pygame/
    https://coderslegacy.com/python/create-menu-screens-in-pygame-tutorial/

Json save Files
    https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/


 
Noted Bugs and missing features
-------------------------------

    For the lobby i would like to have the main lobby stay open in the background, and reload the players data when the window becomes active. Currently the only feature implemented is, the ability for each game to return to the lobby, but this simplly closes the game, then runs the main.py again.

    Audio would have been nice to get in, but due to deadline constraints it was not done.

