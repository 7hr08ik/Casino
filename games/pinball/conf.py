# ===========================
# Pinball
#
# Config File
# ===========================
#
# Imports
import os
import sys

import pygame as pg

# ----------------------------------
# Game properties
game_name = "Pinball"
window_size = (650, 1000)
screen = pg.display.set_mode(window_size)
clock = pg.time.Clock()

# Game locations
game_lobby = [sys.executable, os.path.abspath("main.py")]

# Images
bg = pg.image.load("games/pinball/res/blank_background.png")
ball = pg.image.load("games/pinball/res/ball.png")
l_flipper = pg.image.load("games/pinball/res/left_flipper.png")
r_flipper = pg.image.load("games/pinball/res/right_flipper.png")

# Time settings
MAX_DT = 1 / 60  # Prevent spiral of death on slow frames

# ----------------------------------
# Environment Settings
gvty = 0.1
bounce = -0.6
fl_bounce = -0.8

# Ball settings
pos = (300, 600)  # Start Positiion
b_size = 15  # Ball radius.

# Flipper settings
left_start = (130, 850)
right_start = (430, 850)
start_angle = 15
target_angle = -70
fl_offset = 0.9
flipper_speed = 8
