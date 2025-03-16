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
GAME_NAME = "Maze Exit"
CLOCK = pg.time.Clock()

WINDOW_SIZE = (1280, 720)
FLOOR_IMG = pg.image.load("game_maze/img/maze_floor.png")
BG_IMG = pg.image.load("game_maze/img/maze.png")
LOAD_SCR_IMG = pg.image.load("game_maze/img/loading.png")
LOAD_SCRN_DLY = 3000  # 15sec

GAME_LOBBY = [sys.executable, os.path.abspath("main.py")]

# Game cost configuration
cost_per_second = 3  # Cost per second (configurable)

# Colours
TRANSPARENT = (0, 0, 0, 0)

# ----------------------------------
# Define player properties
p_pos = [50, 62]  # Starting position
mv_spd = 7  # Movement speed

# Define Target properties
t_colour = (0, 0, 0)
t_pos = [1080, 492]
t_size = 85
