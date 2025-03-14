import pygame as pg

import conf


class Flipper:
    def __init__(self, is_left=True):
        self.is_left = is_left
        self.rotation_speed = conf.flipper_speed

        # Load flipper images
        if is_left:
            self.rotated_image = conf.l_flipper
            self.original_image = conf.l_flipper.convert_alpha()
            self.pivot = pg.math.Vector2(20, 20)  # Is (20, 20) but offset from the center
            self.pivot_world = conf.left_start
            self.angle = conf.start_angle
            self.target_angle = conf.target_angle
        else:
            self.rotated_image = conf.r_flipper
            self.original_image = conf.r_flipper.convert_alpha()
            self.pivot = pg.math.Vector2(112, 20)  # Is (112, 20) but offset from the center
            self.pivot_world = conf.right_start
            # Mirror angles for right flipper
            self.angle = -conf.start_angle
            self.target_angle = -conf.target_angle

        # Base image and rect
        self.image = self.original_image
        self.rect = self.image.get_rect()

    # Stolen from SOF, refactored for my setup
    def rotate(self, surface, angle, pivot, offset):
        """
        Rotate the surface around the pivot point.

        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): The rotation angle in degrees.
            pivot (tuple, list, or pygame.math.Vector2): The pivot point in world space.
            offset (pygame.math.Vector2): The pivot point within the surface (local coordinates).
        Returns:
            A tuple of (rotated_image, new_rect) where new_rect is adjusted so that
            the rotation occurs around the pivot point.
        """
        # Get the rect of the original surface
        original_rect = surface.get_rect()
        # Compute the offset vector from the image center to the pivot point (within the image)
        pivot_vector = pg.math.Vector2(offset) - pg.math.Vector2(original_rect.center)
        # Rotate the image
        rotated_image = pg.transform.rotozoom(surface, -angle, 1)
        # Rotate the pivot vector by the given angle
        rotated_vector = pivot_vector.rotate(angle)
        # Compute the new center so that the pivot remains in the same location
        new_center = pg.math.Vector2(pivot) - rotated_vector
        # Get the rect of the rotated image and set its center to the new center
        new_rect = rotated_image.get_rect(center=new_center)
        return rotated_image, new_rect

    def set_position(self, pos):
        """
        Sets the flipper's top-left position.
        Also calculates pivot_world so that the flipper can rotate
        around a fixed point on the board.
        """
        self.x = pos[0]
        self.y = pos[1]

    def update(self):
        """
        Update the flipper's angle, image, and rect.
        """
        # Approach target angle smoothly
        if self.angle < self.target_angle:
            self.angle = min(self.angle + self.rotation_speed, self.target_angle)
        elif self.angle > self.target_angle:
            self.angle = max(self.angle - self.rotation_speed, self.target_angle)

        # Create a new rect with the rotated image and adjust it to keep the pivot point fixed
        rotated_image, new_rect = self.rotate(
            self.original_image,  # Thing to get rotated
            self.angle,  # Angle to rotate to
            self.pivot_world,  # Pivot point in the world space
            self.pivot,  # Pivot point within the image
        )

        self.image = rotated_image
        self.rect = new_rect
