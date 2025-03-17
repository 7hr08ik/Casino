import pygame
import random, os, time
pygame.init()
#constants

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 32)

#variables
var_Running = True
var_Money = 50
var_BetType = 0
var_BetEquals = ""
var_BetValue = 0
var_Bet = 0
var_Ball = 0
var_BallColour = ""


def drawWindow():
    global Window
    table_position = 0, 0
    wheel_position = 57, 50
    WIDTH, HEIGHT = 1280, 720
    Window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roulette")
    script_dir = os.path.dirname(__file__)
    table_path = os.path.join(script_dir, 'Sprites', 'roulettetable.png')
    wheel_path = os.path.join(script_dir, 'Sprites', 'RouletteWheel.png')
    roulette_table = pygame.image.load(table_path)
    roulette_wheel = pygame.image.load(wheel_path)
    Window.blit(roulette_table, dest = table_position)
    Window.blit(roulette_wheel, dest = wheel_position)
    input_box = pygame.Rect(960, 256, 200, 40)
    var_BetEquals = ""  # Stores user input
    active = False  # Tracks whether input box is active
    

def textBox():
    global Window, input_box, font, text, active, color_active, color_inactive, text_color, var_BetEquals
    color = BLUE if active else GREY
    pygame.draw.rect(Window, color, input_box, 2)
    text_surface = font.render(var_BetEquals, True, BLACK)
    Window.blit(text_surface, (input_box.x + 5, input_box.y + 10))

    
def Buttons():
    global number_button_rect, third1_button_rect, third2_button_rect, third3_button_rect, red_button_rect, black_button_rect
    number_button_rect = pygame.Rect(551, 443, 729, 233)
    third1_button_rect = pygame.Rect(627, 371, 216, 62)
    third2_button_rect = pygame.Rect(845, 373, 216, 62)
    third3_button_rect = pygame.Rect(1062, 373, 216, 62)
    red_button_rect = pygame.Rect(844, 666, 108, 53)
    black_button_rect = pygame.Rect(953, 666, 108, 53)

    
def wheelAnimation():
    pass


def betting():
    global var_Money, var_Bet
    if var_Money > 0:
        var_Bet = input("How much would you like to bet?")
        if var_Bet.lower() == "half":
            try:
                var_Bet = int(var_Money) / 2
            except:
                #allows for the bet to be rounded up
                var_Money += 1
                var_Bet = var_Money / 2
            var_Money = int(var_Money) - int(var_Bet)
        elif var_Bet.lower() == "all in":
            var_Bet = var_Money
            var_Money = int(var_Money) - int(var_Bet)
        else:
            try:
                if var_Money < int(var_Bet): #prevents var_Bet from not being an integer
                    print("Insufficient Funds")
                var_Money = var_Money - int(var_Bet)
            except:
                print("Should be a number")
    randomiser()


def randomiser():
    global var_Ball, var_BallColour, var_BallQuarter
    Black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    var_Ball = random.randint(0, 36)
    if var_Ball < 12:
        var_BallQuarter = 1
    elif var_Ball < 24:
        var_BallQuarter = 2
    elif var_Ball <= 36:
        var_BallQuarter = 3
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
    LeaveTable()


def LeaveTable():
    global var_Leave, var_Running
    var_Leave = input("Would you like to leave the table? (Yes or No)")
    if var_Leave.lower() == "yes":
        var_Running = False
        f = open("Payout.txt", "w")
        f.write("You made: ")
        f.write(str(var_Money))
        f.close()
      

#Main Code
drawWindow()
pygame.display.update()
Buttons()
colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('chartreuse4')
active = False
colour = colour_passive
print(type(var_BetEquals))
while var_Running:
    pygame.display.flip()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if number_button_rect.collidepoint(event.pos):
                textBox()
            elif third1_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = 1
            elif third2_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = 2
            elif third3_button_rect.collidepoint(event.pos):
                var_BetType = "third"
                var_BetEquals = 3
            elif black_button_rect.collidepoint(event.pos):
                var_BetType = "colour"
                var_BetEquals = "Black"
            elif red_button_rect.collidepoint(event.pos):
                var_BetType = "colour"
                var_BetEquals = "Red"
            #betting()
                                    #print("Money =",var_Money)
                                    #var_BetType = input("Number, Colour or Third?")
                                    #if var_BetType.lower() == "number":
                                    #    try:                                            #prevents type errors
                                    #        var_BetEquals = int(input("What Number would you like to bet on?"))
                                    #    except:
                                    #        print("You need to bet on a number")
    #    if var_BetEquals < 1:
    #        print("Invalid Selection: Must be between 1 and 36")
    #    elif var_BetEquals > 36:
    #        print("Invalid Selection: Must be between 1 and 36")
    #elif var_BetType.lower() == "colour":
    #   var_BetTemp = input("Which colour: Black, Red or Green?")
    #    if var_BetTemp.lower() == "black":
    #        var_BetEquals = "Black"
    #    elif var_BetTemp.lower() == "red":
    #        var_BetEquals = "Red"
    #    elif var_BetTemp.lower() == "green":
    #        var_BetEquals = "Green"
    #elif var_BetType.lower() == "third":
    #    try:                                             #prevents type errors
    #        var_BetEquals = int(input("Which Third?"))
    #    except:
    #        print("Should be a number.")
    #    if var_BetEquals < 1:
    #       print("Thirds should be between 1 and 3")
    #    elif var_BetEquals > 3:
    #        print("Thirds should be between 1 and 3")
    #betting()  
