# ===========================
# Roulette
#
# Author: James Young
# 03/02/2025
# ===========================
#
import os
import random

import pygame

# Constants
pygame.init()
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = pygame.Color("dodgerblue2")
WIDTH, HEIGHT = 1280, 720
Window = pygame.display.set_mode((WIDTH, HEIGHT))
mouse = pygame.mouse.get_pos()

# variables
var_Running = True
var_Money = 50
var_BetType = ""
var_BetEquals = ""
var_BetValue = 0
var_Bet = ""
var_Ball = 0
var_BallColour = ""
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
    global var_Money, var_Bet, active_2
    active_2 = False
    if var_Bet.lower() == "half":
        try:
            var_Bet = int(var_Money) / 2
        except:
            # allows for the bet to be rounded up
            var_Money += 1
            var_Bet = var_Money / 2
        var_Money = int(var_Money) - int(var_Bet)
    elif var_Bet.lower() == "all in":
        var_Bet = var_Money
        var_Money = int(var_Money) - int(var_Bet)
    else:
        if var_Money < int(var_Bet):  # prevents var_Bet from not being an integer
            print("Insufficient Funds")
        var_Money = var_Money - int(var_Bet)
    randomiser()


def randomiser():
    global var_Ball, var_BallColour, var_BallQuarter
    Black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    var_Ball = random.randint(0, 36)
    if var_Ball < 12:
        var_BallQuarter = "1st Third"
    elif var_Ball < 24:
        var_BallQuarter = "2nd Third"
    elif var_Ball <= 36:
        var_BallQuarter = "3rd Third"
    else:
        print("wtf")
    if var_Ball == 0:
        var_BallColour = "Green"
    elif var_Ball in Black:
        var_BallColour = "Black"
    else:
        var_BallColour = "Red"
    print("The ball landed on", var_Ball, var_BallColour)
    wincheck()


def wincheck():
    global var_Bet, var_Money, var_BetType, var_BetEquals, var_Ball, var_BallColour, var_BallQuarter
    if var_BetType.lower() == "number":
        if var_BetEquals == var_Ball:
            var_Money = int(var_Money) + (int(var_Bet) * 28)
    elif var_BetType.lower() == "colour":
        if var_BetEquals == var_BallColour:
            if var_BallColour == "Green" and var_BetEquals == "Green":
                var_Money = int(var_Money) + (int(var_Bet) * 50)
            else:
                var_Money = int(var_Money) + (int(var_Bet) * 2)
    elif var_BetType.lower() == "third":
        if var_BallQuarter == var_BetEquals:
            var_Money = int(var_Money) + (int(var_Bet) * 12)
    else:
        print("You didnt win :(")
    return ()


# Close the game and save the money value
def LeaveTable():
    global var_Leave, var_Running, var_Money
    var_Money = str(var_Money)
    file = open("Payout.txt", "w")
    file.write("You Made: ")
    file.write(var_Money)
    file.close()
    var_Running = False
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def drawWindow():
    Window.blit(roulette_table, (0, 0))
    Window.blit(roulette_wheel, (57, 50))


def drawTextBoxBetEquals():
    color = BLUE if active_1 else GREY
    pygame.draw.rect(Window, color, input_box_1, 2)
    text_surface = font.render(var_BetEquals, True, BLACK)
    Window.blit(text_surface, (input_box_1.x + 5, input_box_1.y))


def drawTextBoxBet():
    color = BLUE if active_2 else GREY
    pygame.draw.rect(Window, color, input_box_2, 2)
    text_surface_1 = font.render(var_Bet, True, BLACK)
    Window.blit(text_surface_1, (input_box_2.x + 5, input_box_2.y))


def drawLeaveTable():
    color = BLUE if active_3 else GREY
    pygame.draw.rect(Window, color, leave_table_button, 2)
    text_surface_2 = font1.render("Leave Table", True, BLACK)
    Window.blit(text_surface_2, (leave_table_button.x + 10, leave_table_button.y + 7))


# Main Game Loop
while var_Running == True:
    drawWindow()
    drawTextBoxBetEquals()
    drawTextBoxBet()
    drawLeaveTable()
    money_surface = font.render(f"Money: £{var_Money}", True, (BLACK))
    ball_display = font.render(f"Counter: {var_Ball}", True, (BLACK))
    Window.blit(money_surface, (950, 10))
    Window.blit(input_box_1_text, (600, 306))
    Window.blit(input_box_2_text, (550, 670))
    Window.blit(ball_display, (150, 500))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var_Running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if number_button_rect.collidepoint(event.pos):
                active_1 = True
            elif third1_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = "1st Third"
                active_2 = True
            elif third2_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = "2nd Third"
                active_2 = True
            elif third3_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = "3rd Third"
                active_2 = True
            elif black_button_rect.collidepoint(event.pos):
                var_BetType = "colour"
                var_BetEquals = "Black"
                active_2 = True
            elif red_button_rect.collidepoint(event.pos):
                var_BetType = "colour"
                var_BetEquals = "Red"
                active_2 = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            LeaveTable()
        if event.type == pygame.KEYDOWN and active_1:
            if event.key == pygame.K_BACKSPACE:
                var_BetEquals = var_BetEquals[:-1]
            elif event.key == pygame.K_RETURN:
                print("Entered:", var_BetEquals)
                active_1 = False
                enter_pressed = True
                active_2 = True
            else:
                var_BetEquals += event.unicode
        if var_Money > 0:
            if event.type == pygame.KEYDOWN and active_2:
                if event.key == pygame.K_BACKSPACE:
                    var_Bet = var_Bet[:-1]
                    enter_pressed = False
                elif event.key == pygame.K_RETURN and enter_pressed == False:
                    print("Entered:", var_Bet)
                    betting()
                else:
                    var_Bet += event.unicode
        else:
            print("Insufficient Funds!")
            LeaveTable()
        pygame.display.flip()
