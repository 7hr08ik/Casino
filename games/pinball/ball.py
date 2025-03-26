# ===========================
# Pinball
#
# Author: Rob Hickling
# ===========================
#
# Imports
import conf


class PlayerBall:
    def __init__(self, size, pos):
        # Create Alpha of images
        self.ball_image = conf.ball.convert_alpha()

        # Initialize variables
        self.sizeX = size
        self.x = pos[0]
        self.y = pos[1]
        self.moveX = 1
        self.moveY = 1
        # Gravity force to be applied every frame
        self.gravity = conf.gvty
        # Bounce factors for board and flipper collisions
        self.bounce_factor = conf.bounce
        self.fl_bounce_factor = conf.fl_bounce
        self.fl_offset = conf.fl_offset

    def update_position(self, board, flippers):
        """
        Updates the ball's position based on its velocity, board collisions,
        and collisions with flippers.

        The function applies gravity, then checks if the new position is
        valid on the game board. If a collision is detected on the board,
        the appropriate velocity component is reversed by multiplying by
        the bounce factor. Additionally, if a collision with any of the
        flippers is detected, a separate bounce with additional offset
        is applied, and the ball is repositioned to avoid slipping through
        the flipper.
        """
        # Apply gravity to vertical movement.
        self.moveY += self.gravity

        # Calculate the new position.
        new_x = self.x + self.moveX
        new_y = self.y + self.moveY

        # First, check for collision with the board.
        if board.can_move(new_x, new_y, self.sizeX):
            # No board collision: update ball position normally.
            self.x = new_x
            self.y = new_y
        else:
            # Handle board collision by reversing velocity.
            if not board.can_move(self.x + self.moveX, self.y, self.sizeX):
                self.moveX *= self.bounce_factor
            if not board.can_move(self.x, self.y + self.moveY, self.sizeX):
                self.moveY *= self.bounce_factor

        # Detect when ball and flipper collide
        # and increase bounce factor by adding fl_bounce_factor
        if board.ball_fl_collision(self.x, self.y, self.sizeX):
            self.moveX *= self.fl_bounce_factor
            self.moveY *= self.fl_bounce_factor

        # Ensure the ball does not fall below the bottom boundary.
        if self.y + self.moveY > conf.window_size[1]:
            self.moveY = 0
            # TODO: Add code to remove ball and restart game

    def draw(self, screen):
        """
        Draws the player ball on the screen at its current position.
        """
        screen.blit(self.ball_image, (self.x - self.sizeX, self.y - self.sizeX))
