# ===========================
# Pinball

# Author: Rob Hickling
# ===========================

# Imports
import pygame as pg
from ball import PlayerBall
from flipper import Flipper

import conf


class GameBoard:
    def __init__(self):
        # Setup images and masks
        self.bg_image = conf.bg.convert_alpha()
        self.bg_mask = pg.mask.from_surface(self.bg_image)
        # Initialize flippers
        self.left_flipper = Flipper(is_left=True)
        self.right_flipper = Flipper(is_left=False)
        # Initialize ball
        self.ball = PlayerBall(conf.b_size, conf.pos)

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

    def ball_fl_mask_overlap(self, flipper, new_x, new_y, radius, ball_mask):
        """
        Helper to check if the ball_mask overlaps with a particular flipper.
        """
        # Ensure the flipper's mask is updated to its freshly rotated image
        flipper_mask = pg.mask.from_surface(flipper.image)

        # Calculate offset for ball vs. the flipper’s top-left rect
        offset = (int(new_x - radius - flipper.rect.x), int(new_y - radius - flipper.rect.y))

        return flipper_mask.overlap(ball_mask, offset) is not None

    def ball_fl_collision(self, new_x, new_y, radius):
        """
        Returns True if the ball overlaps either the left or right flipper.
        """
        # Temporary ball surface and mask
        ball_surface = pg.Surface((radius * 2, radius * 2))
        pg.draw.circle(ball_surface, (255, 255, 255, 255), (radius, radius), radius)
        ball_mask = pg.mask.from_surface(ball_surface)

        # TODO: If the ball collides with the flipper increase bounce factor by variable
        # Check overlap with the left flipper
        return bool(
            self.ball_fl_mask_overlap(self.left_flipper, new_x, new_y, radius, ball_mask)
            or self.ball_fl_mask_overlap(self.right_flipper, new_x, new_y, radius, ball_mask)
        )

    def ball_bg_collision(self, new_x, new_y, radius):
        """
        Returns False if there's a collision with the background.
        """
        ball_surface = pg.Surface((radius * 2, radius * 2))
        pg.draw.circle(ball_surface, (255, 255, 255, 255), (radius, radius), radius)
        ball_mask = pg.mask.from_surface(ball_surface)

        offset = (int(new_x - radius), int(new_y - radius))
        overlap = self.bg_mask.overlap(ball_mask, offset)
        return overlap is None

    def can_move(self, new_x, new_y, radius):
        """
        Determines if the ball can move to (new_x, new_y) without colliding
        with the background or the flippers. Returns True if no collision.
        """
        # First, check background collision using mask
        return not (not self.ball_bg_collision(new_x, new_y, radius) or self.ball_fl_collision(new_x, new_y, radius))

    def key_input(self):
        """
        Updates the angle of the flippers.
        Only need to set the target angle for the Flipper class to handle the rest.

        Left Flipper - Clockwise
        Right Flipper - Counter-clockwise
        """
        self.keys = pg.key.get_pressed()

        if self.keys[pg.K_LEFT] or self.keys[pg.K_a]:
            self.left_flipper.target_angle = conf.target_angle
        elif self.keys[pg.K_RIGHT] or self.keys[pg.K_d]:
            self.right_flipper.target_angle = -conf.target_angle
        elif self.keys[pg.K_UP] or self.keys[pg.K_w]:
            self.left_flipper.target_angle = conf.target_angle
            self.right_flipper.target_angle = -conf.target_angle
        elif self.keys[pg.K_DOWN] or self.keys[pg.K_s] or self.keys[pg.K_SPACE]:
            # TODO: Handle ball launch here
            pass
        else:
            # Revert to resting positions
            self.left_flipper.target_angle = conf.start_angle
            self.right_flipper.target_angle = -conf.start_angle

        self.left_flipper.update()
        self.right_flipper.update()

    def update_board(self):
        """
        Updates the game board.
        """
        # Update flipper positions from configuration.
        self.left_flipper.set_position(conf.left_start)
        self.right_flipper.set_position(conf.right_start)

        # Update the flippers to compute their rotated images and rects.
        self.left_flipper.update()
        self.right_flipper.update()

    def draw_background(self, screen):
        screen.blit(self.bg_image, (0, 0))

    def draw_flippers(self, screen):
        """
        Draws the flippers on the board using their rotated image and anchored rect.
        This ensures the rotation happens around the fixed pivot point.
        """
        screen.blit(self.left_flipper.image, self.left_flipper.rect)
        screen.blit(self.right_flipper.image, self.right_flipper.rect)
