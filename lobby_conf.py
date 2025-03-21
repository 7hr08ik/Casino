# ===========================
# Casino Lobby
#
# Config File
# ===========================
#
# Main Imports
import os
import sys

import pygame as pg

"""
All, if not most of the games Variables are set here
"""
# ----------------------------------
#
# Game properties
GAME_NAME = "Casino Lobby"
WIN_SIZE = (1280, 720)
CLOCK = pg.time.Clock()
LOAD_SCRN_DLY = 3000  # 3sec

# Images
LOAD_SCR_IMG = pg.image.load("img/loading.png")
BG_IMG = pg.image.load("img/bg.png")
LOSER_IMG = pg.image.load("img/loser.png")

# Shortcuts
GAME_PINBALL = [sys.executable, os.path.abspath("games/pinball/main.py")]
GAME_MAZE = [sys.executable, os.path.abspath("games/maze/main.py")]
GAME_LOTTERY = [sys.executable, os.path.abspath("games/lottery/lottery.py")]
GAME_BLACKJACK = [sys.executable, os.path.abspath("games/blackjack/BlackJack_ICA.py")]
GAME_DICE = [sys.executable, os.path.abspath("games/dice/dice.py")]
GAME_ROULETTE = [sys.executable, os.path.abspath("games/roulette/Roulette.py")]
GAME_SHELL = [sys.executable, os.path.abspath("games/shell/Shell_Game.py")]

# ----------------------------------
# Player / Targets
#
# Define player properties
p_pos = [600, 550]  # Starting position
mv_spd = 7  # Movement speed
starting_cash = 1000

#  Define targets
t_color = (0, 0, 0)  # RGB
# Exit Target
e_pos = [782, 295]
e_size = 20
# Target 1 - Pinball
t_pos = [1099, 569]
t_size = 20
# Target 2 - Maze
t2_pos = [1090, 655]
t2_size = 63
# Target 3 - Lottery
t3_pos = [260, 493]
t3_size = 20
# Target 4 - Blackjack
t4_pos = [124, 594]
t4_size = 26
# Target 5 - Dice Game
t5_pos = [368, 430]
t5_size = 16
# Target 6 - Roulette
t6_pos = [986, 505]
t6_size = 25
# Target 7 - Shell Game
t7_pos = [898, 426]
t7_size = 16

# ----------------------------------
