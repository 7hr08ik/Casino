# ===========================
# Roulette
#
# Author: James Young
# 07/02/2025
#
# Modified by: Rob Hickling
# 23/03/2025
#   Added functionality for saving and loading player data
#   required for integration into the lobby
#   all commented with;
#        # For game_integration
# 25/03/2025
#   Renamed all variables and functions
#   to make sure code is PEP8 compliant
# ===========================

import os
import random

import pygame

# For game_integration
from game_integration import check_balance, load_player_data, save_and_exit

# Constants
pygame.init()
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = pygame.Color("dodgerblue2")
WIDTH, HEIGHT = 1280, 720
Window = pygame.display.set_mode((WIDTH, HEIGHT))
mouse = pygame.mouse.get_pos()
rotations = [
    0,
    224.872,
    58.184,
    341.24,
    39.456,
    185.916,
    97.64,
    302.784,
    155.824,
    262.728,
    175.552,
    138.096,
    321.512,
    118.368,
    243.6,
    19.728,
    205.144,
    78.912,
    283.056,
    26.592,
    234.736,
    49.32,
    272.192,
    166.688,
    195.68,
    69.048,
    350.104,
    108.504,
    311.648,
    291.92,
    147.96,
    252.664,
    9.864,
    214.508,
    88.776,
    330.376,
    128.232,
]

# variables
var_running = True

# For game_integration
# var_Money = 50 # Original
# Replace original cash variable:
player_data = load_player_data()  # Load the data
var_money = player_data["cash_balance"]

var_bettype = ""
var_betequals = ""
var_betvalue = 0
var_bet = ""
var_ball = 0
var_ballcolour = ""
enter_pressed = False

# Fonts
font = pygame.font.Font(None, 60)
font1 = pygame.font.Font(None, 45)

# Input Boxes
input_box_1 = pygame.Rect(850, 306, 200, 40)
input_box_2 = pygame.Rect(640, 670, 200, 40)
input_box_1_text = font.render("Bet Number:", True, (BLACK))
input_box_2_text = font.render("Bet:", True, (BLACK))
active_1 = False
active_2 = False
active_3 = False

# Window setup
pygame.display.set_caption("Roulette")
script_dir = os.path.dirname(__file__)
table_path = os.path.join(script_dir, "Sprites", "roulettetable.png")
wheel_path = os.path.join(script_dir, "Sprites", "RouletteWheel.png")
roulette_table = pygame.image.load(table_path)
roulette_wheel = pygame.image.load(wheel_path)


# Button Creation
number_button_rect = pygame.Rect(551, 443, 729, 233)
third1_button_rect = pygame.Rect(627, 371, 216, 62)
third2_button_rect = pygame.Rect(845, 373, 216, 62)
third3_button_rect = pygame.Rect(1062, 373, 216, 62)
red_button_rect = pygame.Rect(844, 666, 108, 53)
black_button_rect = pygame.Rect(953, 666, 108, 53)
leave_table_button = pygame.Rect(1070, 670, 200, 40)


def betting():
    global var_money, var_bet, active_2

    # For game_integration
    player_data = load_player_data()  # Load the data

    active_2 = False
    if var_bet.lower() == "half":
        try:
            var_bet = int(var_money) / 2
        except:
            # allows for the bet to be rounded up
            var_money += 1
            player_data["cash_balance"] += 1  # For game_integration
            var_bet = var_money / 2
        var_money = int(var_money) - int(var_bet)
    elif var_bet.lower() == "all in":
        var_bet = var_money
        var_money = int(var_money) - int(var_bet)
    else:
        if var_money < int(
            var_bet
        ):  # prevents var_Bet from not being an integer
            print("Insufficient Funds")
        var_money = var_money - int(var_bet)
    roulettewheelspin()


def randomiser():
    global var_ball, var_ballcolour, var_ballquarter
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    var_ball = random.randint(0, 36)
    if var_ball < 12:
        var_ballquarter = "1st Third"
    elif var_ball < 24:
        var_ballquarter = "2nd Third"
    elif var_ball <= 36:
        var_ballquarter = "3rd Third"
    else:
        print("wtf")
    if var_ball == 0:
        var_ballcolour = "Green"
    elif var_ball in black:
        var_ballcolour = "Black"
    else:
        var_ballcolour = "Red"
    wincheck()


def wincheck():
    global \
        var_bet, \
        var_money, \
        var_bettype, \
        var_betequals, \
        var_ball, \
        var_ballcolour, \
        var_ballquarter

    # For game_integration
    player_data = load_player_data()  # Load the data

    if var_bettype.lower() == "number":
        if var_betequals == var_ball:
            var_money = int(var_money) + (int(var_bet) * 28)
            # For game_integration
            player_data["cash_balance"] = int(var_money) + (int(var_bet) * 28)
    elif var_bettype.lower() == "colour":
        if var_betequals == var_ballcolour:
            if var_ballcolour == "Green" and var_betequals == "Green":
                var_money = int(var_money) + (int(var_bet) * 50)
                # For game_integration
                player_data["cash_balance"] = int(var_money) + (
                    int(var_bet) * 50
                )
            else:
                var_money = int(var_money) + (int(var_bet) * 2)
                # For game_integration
                player_data["cash_balance"] = int(var_money) + (
                    int(var_bet) * 2
                )
    elif var_bettype.lower() == "third" and var_ballquarter == var_betequals:
        var_money = int(var_money) + (int(var_bet) * 12)
        # For game_integration
        player_data["cash_balance"] = int(var_money) + (int(var_bet) * 12)
    var_betequals = ""
    var_bet = ""
    return ()


# Close the game and save the money value
def leavetable():
    global var_Leave, var_running, var_money
    var_money = str(var_money)
    file = open("games/roulette/Payout.txt", "w")
    file.write("You Made: ")
    file.write(var_money)
    file.close()

    # For game_integration
    player_data = load_player_data()  # Load the data
    player_data["cash_balance"] = var_money
    save_and_exit(Window, player_data)

    var_running = False
    pygame.display.quit()
    pygame.quit()


def roulettewheelspin():
    global var_ball
    var_ball = 0
    var_rouletteSpin = 38
    while var_ball < var_rouletteSpin:
        var_ball += 1
        drawwindow()
        pygame.display.update()
        pygame.time.delay(1)
    randomiser()


def drawwindow():
    Window.blit(roulette_table, (0, 0))
    global roulette_wheel, var_ball, rotations
    topleft = [57, 50]
    try:
        rotated_wheel = pygame.transform.rotate(
            roulette_wheel, rotations[var_ball]
        )
    except:
        rotated_wheel = pygame.transform.rotate(roulette_wheel, rotations[0])
    new_rect = rotated_wheel.get_rect(
        center=roulette_wheel.get_rect(topleft=topleft).center
    )
    Window.blit(rotated_wheel, new_rect)
    drawtextboxbetequals()
    drawtextboxbet()
    drawleavetable()
    money_surface = font.render(f"Money: £{var_money}", True, (BLACK))
    Window.blit(money_surface, (950, 10))
    Window.blit(input_box_1_text, (600, 306))
    Window.blit(input_box_2_text, (550, 670))


def drawtextboxbetequals():
    color = BLUE if active_1 else GREY
    pygame.draw.rect(Window, color, input_box_1, 2)
    text_surface = font.render(var_betequals, True, BLACK)
    Window.blit(text_surface, (input_box_1.x + 5, input_box_1.y))


def drawtextboxbet():
    color = BLUE if active_2 else GREY
    pygame.draw.rect(Window, color, input_box_2, 2)
    text_surface_1 = font.render(var_bet, True, BLACK)
    Window.blit(text_surface_1, (input_box_2.x + 5, input_box_2.y))


def drawleavetable():
    color = BLUE
    pygame.draw.rect(Window, color, leave_table_button, 2)
    text_surface_2 = font1.render("Leave Table", True, BLACK)
    Window.blit(
        text_surface_2, (leave_table_button.x + 10, leave_table_button.y + 7)
    )


# Main Game Loop
while var_running is True:
    drawwindow()

    # For game_integration
    player_data = load_player_data()  # Load the data
    player_data["cash_balance"] = var_money
    check_balance(Window, player_data)  # check for no money

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if number_button_rect.collidepoint(event.pos):
                active_1 = True
            elif third1_button_rect.collidepoint(event.pos):
                var_bettype = "third"
                var_betequals = "1st Third"
                active_1 = False
                active_2 = True
            elif third2_button_rect.collidepoint(event.pos):
                var_bettype = "third"
                var_betequals = "2nd Third"
                active_1 = False
                active_2 = True
            elif third3_button_rect.collidepoint(event.pos):
                var_bettype = "third"
                var_betequals = "3rd Third"
                active_1 = False
                active_2 = True
            elif black_button_rect.collidepoint(event.pos):
                var_bettype = "colour"
                var_betequals = "Black"
                active_1 = False
                active_2 = True
            elif red_button_rect.collidepoint(event.pos):
                var_bettype = "colour"
                var_betequals = "Red"
                active_1 = False
                active_2 = True
            elif leave_table_button.collidepoint(event.pos):
                active_3 = True
            else:
                active_3 = False
        if event.type == pygame.MOUSEBUTTONDOWN and active_3:
            leavetable()
        if event.type == pygame.KEYDOWN and active_1:
            if event.key == pygame.K_BACKSPACE:
                var_betequals = var_betequals[:-1]
            elif event.key == pygame.K_RETURN:
                active_1 = False
                enter_pressed = True
                active_2 = True
            else:
                var_betequals += event.unicode
        if var_money > 0:
            if event.type == pygame.KEYDOWN and active_2:
                if event.key == pygame.K_BACKSPACE:
                    var_bet = var_bet[:-1]
                    enter_pressed = False
                elif event.key == pygame.K_RETURN and enter_pressed is False:
                    betting()
                else:
                    var_bet += event.unicode
        else:
            print("Insufficient Funds!")
            leavetable()
        pygame.display.flip()
