Teesside Casino - Game Suite
============================

Authors: 
    
    Rob Hickling

Product Description
-------------------

    This si the Maze game. Early in development i realised that the Maze would be perfect candidate for the exit of the Casino. Everybody understands that a Casino is designed to keep people in, and spending money. They accomplish this by creating a floor plan akin to a maze, making it hard for customers to leave without the temptation to spend more money. 
    
    The Maze will load the players data, and begin counting on a timer. The longer it takes the player to leave the maze, the more money they will spend. So you'd better be quick. Upon reaching the end of the maze the player is presented with the Exit/Goodbye screen exressing thanks for their custom. If, however, the players cash reaches zero. Then they are presented with the loser screen, and seremoniously kicked out of the casino, and thier account ifno (player database entry) is removed.


Development Environment
-----------------------

    Operating System : Manjaro Linux 

    Python Version : 3.12.3

    IDE : Visual Studio Code
        Plugins
            Qodo Gen. Coding Autocomplete assistant.
            Ruff Extension. Linter + Formatter.


Requirements
------------

    Python >= 3.6
    Pygame >= 2.6.1


Install Instructions
--------------------

Install Requirements:

Python

    https://www.python.org/downloads/

Pygame (In terminal)
    
    pip install pygame

Git:
    
    git clone https://github.com/7hr08ik/Casino.git

Manual

    Download the project. 
    Unpack/place the folder 'Casino' in the required location.
    Run Casino/main.py


Usage Instructions
------------------

Windows:

    Open terminal in game folder
    python -m main
    -----------------------
    Open main.py in Idle
    Run
    -----------------------

Linux (in terminal):
    
    cd Casino
    python3 -m main


Online Resources Used (Non-exhaustive)
--------------------------------------

https://yofreesamples.com/mazes/

Character Files
    https://aske4.itch.io/antihero-character

Maze assets
    https://gamebetweenthelines.itch.io/2d-top-down-pixel-art-tileset-casino?download

Animation Help
    https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

    
 
Noted Bugs and missing features
-------------------------------

    It is possible for thwe player to get caught on some of the scenery. This could be fixed by editing the image used for collision.
    
