# ===========================
# Maze Game
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
GAME_NAME = "Maze Game"
CLOCK = pg.time.Clock()

WINDOW_SIZE = (1280, 720)
FLOOR_IMG = pg.image.load("game_maze/img/maze_floor.png")  # Background image
BG_IMG = pg.image.load("game_maze/img/maze.png")  # Background image
LOAD_SCR_IMG = pg.image.load("game_maze/img/loading.png")
LOAD_SCRN_DLY = 15000  # 15sec

GAME_LOBBY = [sys.executable, os.path.abspath("main.py")]

# Game cost configuration
cost_per_second = 10  # Cost per second (configurable)
total_cost = 0  # Total accumulated cost

# Colours
TRANSPARENT = (0, 0, 0, 0)

# ----------------------------------
# Define player properties
p_pos = [50, 62]  # Starting position
mv_spd = 5  # Movement speed

# Define exit
t_colour = (0, 255, 0)  # Green colour
t_pos = [1060, 520]
t_size = 30
