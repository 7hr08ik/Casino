Pinball
=======

Author: Rob Hickling

Product Description
-------------------

This game, unfortunately was shelved half way through development. Due to time constraints, it was not possible to complete this game. It is kept here for posperity, as proof of work, but is functionally dead. The ball drops, but does nto react correctly. The flippers work, they rotate, but do not puch the ball away as expected. The current background image is a placeholder intended to be replaced.

The game was to be a typical game of pinball. Fire the ball with the space bar, use the arrow keys to control the flippers. I was intending on integrating gambling into the game, by having a simple 3 bar slot machine built into the game, that would give results based on the user score.

Unfortunately too much time was spent fixing collision, and even more so, trying to figure out how to implement gravity was rturning out to be a very large problem. My implementation was to move the ball ndownwards at a constant rate, but in order to get the ball to react to the flippers and the vame world correctly, I think i would have to replace my simple gravity with a velocity calculation that constantly pulled the ball downwards, depending on its speed, fall distance, angle of attack, surface it has bounced off etc.

I was also responsible for 2 other parts of this project, so the decision was made to shelf this game and concentrate on the other parts.


Development Environment
-----------------------

    VSCode
    Linux
    Python version 3.12

Requirements
------------

    Python >= 3.6
    Pygame >= 2.6.1

Install Instructions
--------------------

    This game is now integrated into the lobby system, and as such requires no special installation, outside of the lobby.

Usage Instructions
------------------

    Launch the lobby, and activate the target for Pinball.

Resources used
--------------
    
    Guide for gravity implementation
        https://www.pygame.org/project/1964/3488
        https://stackoverflow.com/questions/62720811/how-to-make-gravity-function-in-pygame
        
    Character Files
        https://aske4.itch.io/antihero-character

    Help found for rotating the flippers:
        https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

    Collisions Help
        https://stackoverflow.com/questions/55817422/collision-between-masks-in-pygame
        https://toxigon.com/implementing-collision-detection-in-pygame

    Pivot point helper
        https://stackoverflow.com/questions/15098900/how-to-set-the-pivot-point-center-of-rotation-for-pygame-transform-rotate/49413006#49413006

    Physics Simulation
        https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/
    
Noted Bugs and missing features
-------------------------------

    Ants everywhere...

