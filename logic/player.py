# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
# Local Imports
import pygame as pg

import lobby_conf as conf


class Player:
    def __init__(self, x, y):
        """
        Initialize the player object.

        Set the players starting position and load the
        player's images.
        """
        # Load images once when the program starts.
        # Put them into lists, one for each direction.
        pgl = pg.image.load
        self.pl_idle = [pgl("img/Idle/Idle.png").convert_alpha()]
        self.pl_run_up = [pgl(f"img/Walk/Up/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_down = [pgl(f"img/Walk/Down/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_left = [pgl(f"img/Walk/Left/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_right = [pgl(f"img/Walk/Right/{i}.png").convert_alpha() for i in range(1, 5)]
        self.keys = None
        self.key_list = (
            pg.K_UP,
            pg.K_w,
            pg.K_DOWN,
            pg.K_s,
            pg.K_LEFT,
            pg.K_a,
            pg.K_RIGHT,
            pg.K_d,
        )

        self.pos_x = x
        self.pos_y = y

        self.images = self.pl_idle
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.anim_index = 0
        self.anim_timer = 0

    # -------------------------------------------------------------------------
    # Utilities
    #

    def update(self, dt):
        """
        Update the player's movement and image.
        """
        self.move_player()  # Move the player
        self.animate(dt)  # Animate the player using delta time

    def draw(self, screen):
        """
        Draw the player image onto the screen at the player's position.
        """

        screen.blit(self.image, self.rect)

    # -------------------------------------------------------------------------
    # Functions / Methods
    #

    def move_player(self):
        """
        Updates the player's position and image based on the player's input.

        Keys that are checked for player movement are:
            UP, DOWN, LEFT, RIGHT, W, A, S, D

        The player's image list is changed to reflect the direction of movement.
        If no movement keys are pressed, player set to the idle image.
        """
        self.keys = pg.key.get_pressed()

        if (self.keys[pg.K_UP] or self.keys[pg.K_w]) and self.pos_y > 0:
            self.pos_y -= conf.mv_spd
            self.images = self.pl_run_up  # player image ^ up facing
        if (self.keys[pg.K_DOWN] or self.keys[pg.K_s]) and self.pos_y < (conf.WIN_SIZE[1] - 15):
            self.pos_y += conf.mv_spd
            self.images = self.pl_run_down  # player image = down facing
        if (self.keys[pg.K_LEFT] or self.keys[pg.K_a]) and (self.pos_x > 0):
            self.pos_x -= conf.mv_spd
            self.images = self.pl_run_left  # player image < left facing
        if (self.keys[pg.K_RIGHT] or self.keys[pg.K_d]) and self.pos_x < (conf.WIN_SIZE[0] - 15):
            self.pos_x += conf.mv_spd
            self.images = self.pl_run_right  # player image > right facing
        # Check if no movement keys are pressed and set animation to idle
        if not any(self.keys[key] for key in self.key_list):
            self.images = self.pl_idle  # Show idle

        # Update the rect because it's used to blit the image.
        self.rect.center = self.pos_x, self.pos_y

    def animate(self, dt):
        """
        Animate the player character by cycling through images.

        This method rotates through the images in a loop.
        Every 70ms increments to the next image.
        """

        # Add the delta time to the anim_timer
        self.anim_timer += dt
        #  Increment through the index after 70 ms.
        if self.anim_timer > 0.07:  # After 70 ms.
            self.anim_timer = 0  # Reset the timer.
            self.anim_index += 1  # Increment the index.
            self.anim_index %= len(self.images)  # Modulo to cycle the index.
            self.image = self.images[self.anim_index]  # And switch the image.
