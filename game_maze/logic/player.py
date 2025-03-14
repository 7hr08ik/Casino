# ===========================
# Python game suite
#
# Casino Lobby
# ===========================
#
# Main Imports
import pygame as pg

# Local Imports
import conf


class Player:
    def __init__(self, x, y):
        # Load images once when the program starts.
        # Put them into lists, one for each direction.
        self.pl_idle = [pg.image.load("game_maze/img/Idle/Idle.png").convert_alpha()]
        self.pl_run_up = [pg.image.load(f"game_maze/img/Walk/Up/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_down = [pg.image.load(f"game_maze/img/Walk/Down/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_left = [pg.image.load(f"game_maze/img/Walk/Left/{i}.png").convert_alpha() for i in range(1, 5)]
        self.pl_run_right = [pg.image.load(f"game_maze/img/Walk/Right/{i}.png").convert_alpha() for i in range(1, 5)]
        self.bg_image = conf.BG_IMG.convert_alpha()  # Must stay in main.py Fails if moved to conf.py

        self.images = self.pl_idle
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

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

        self.anim_index = 0
        self.anim_timer = 0

    def can_move(self, new_x, new_y):
        # Check the actual non-transparent pixels of the player's image
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)).a != 0:  # Check if pixel is not transparent
                    # Calculate the new position of this pixel
                    new_pixel_x = new_x + x
                    new_pixel_y = new_y + y
                    # Check boundaries
                    if new_pixel_x >= self.bg_image.get_width() or new_pixel_y >= self.bg_image.get_height():
                        return False
                    # Check collision with walls
                    if self.bg_image.get_at((new_pixel_x, new_pixel_y)) != conf.TRANSPARENT:
                        return False
        return True

    def move_player(self):
        self.keys = pg.key.get_pressed()

        if (
            (self.keys[pg.K_UP] or self.keys[pg.K_w])
            and self.pos_y > 0
            and self.can_move(self.pos_x, self.pos_y - conf.mv_spd)
        ):
            self.pos_y -= conf.mv_spd  # Move the player
            self.images = self.pl_run_up  # player image = up facing
        if (
            (self.keys[pg.K_DOWN] or self.keys[pg.K_s])
            and self.pos_y < conf.WINDOW_SIZE[1]
            and self.can_move(self.pos_x, self.pos_y + conf.mv_spd)
        ):
            self.pos_y += conf.mv_spd  # Move the player
            self.images = self.pl_run_down  # player image = down facing
        if (
            (self.keys[pg.K_LEFT] or self.keys[pg.K_a])
            and (self.pos_x > 0)
            and self.can_move(self.pos_x - conf.mv_spd, self.pos_y)
        ):
            self.pos_x -= conf.mv_spd  # Move the player
            self.images = self.pl_run_left  # player image = left facing
        if (
            (self.keys[pg.K_RIGHT] or self.keys[pg.K_d])
            and self.pos_x < conf.WINDOW_SIZE[0]
            and self.can_move(self.pos_x + conf.mv_spd, self.pos_y)
        ):
            self.pos_x += conf.mv_spd  # Move the player
            self.images = self.pl_run_right  # player image = right facing

        # Check if no movement keys are pressed and set animation to idle
        if not any(self.keys[key] for key in self.key_list):
            self.images = self.pl_idle  # Show idle

        # Update the rect because it's used to blit the image.
        self.rect.topleft = self.pos_x, self.pos_y

    def animate(self, dt):
        # Add the delta time to the anim_timer and rotate through the images
        self.anim_timer += dt
        if self.anim_timer > 0.07:  # After 70 ms.
            self.anim_timer = 0  # Reset the timer.
            self.anim_index += 1  # Increment the image index.
            self.anim_index %= len(self.images)  # Modulo to cycle the index.
            self.image = self.images[self.anim_index]  # And switch the image.

    def update(self, dt):
        self.move_player()
        self.animate(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
