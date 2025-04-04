Exit Maze
=========

Authors: 
- Rob Hickling

Product Description
-------------------

This is the Maze game. Early in development I realised that the Maze would be perfect candidate for the exit of the Casino. Everybody understands that a Casino is designed to keep people in, and spending money. They accomplish this by creating a floor plan akin to a maze, making it hard for customers to leave without the temptation to spend more money. 

The Maze will load the players data, and begin counting on a timer. The longer it takes the player to leave the maze, the more money they will spend. So you'd better be quick. Upon reaching the end of the maze the player is presented with the Exit/Goodbye screen exressing thanks for their custom. If, however, the players cash reaches zero. Then they are presented with the loser screen, and seremoniously kicked out of the casino, and thier account ifno (player database entry) is removed.


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

This game has been fully integrated into the lobby suite.
Installation is handled as part of the full project

Usage Instructions
------------------

Game is run from the main lobby. 
Open the lobby, and walk to the `Exit` target to begin this game.


Online Resources Used (Non-exhaustive)
--------------------------------------

- Maze layout
    - https://yofreesamples.com/mazes/

- Character Files
    - https://aske4.itch.io/antihero-character

- Maze assets
    - https://gamebetweenthelines.itch.io/2d-top-down-pixel-art-tileset-casino?download

- Animation Help
    - https://stackoverflow.com/questions/49352990/how-do-i-get-my-images-to-work-as-an-animation-in-pygame

    
 
Noted Bugs and missing features
-------------------------------

- It is possible for the player to get caught on some of the scenery. This could be fixed by editing the image used for collision.
    
