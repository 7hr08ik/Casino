import random
#constants

var_Running = True

#variables
var_Money = 50
var_BetType = 0
var_BetEquals = 0
var_BetValue = 0
var_Bet = 0
var_Ball = 0
var_BallColour = ""


def debug():
    global var_Money, var_Multiplier, var_BetType, var_BetEquals, var_BetValue, var_Bet, var_Running, var_Ball, var_BallColour, var_BallQuarter
    print("Debug:", var_Money, var_BetType, var_BetEquals, var_BetValue, var_Bet, var_Running, var_Ball, var_BallColour, var_BallQuarter) #prints every variable
    return()


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
    elif var_BetType.lower() == "quarter":
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
while var_Running == True:
    var_BetType = 0
    var_BetEquals = 0
    var_BetValue = 0
    var_Bet = 0
    var_Ball = 0
    var_BallColour = ""
    print("Money =",var_Money)
    var_BetType = input("Number, Colour or Third?")
    if var_BetType.lower() == "number":
        try:                                            #prevents type errors
            var_BetEquals = int(input("What Number would you like to bet on?"))
        except:
            print("You need to bet on a number")
        if var_BetEquals < 1:
            print("Invalid Selection: Must be between 1 and 36")
        elif var_BetEquals > 36:
            print("Invalid Selection: Must be between 1 and 36")
    elif var_BetType.lower() == "colour":
        var_BetTemp = input("Which colour: Black, Red or Green?")
        if var_BetTemp.lower() == "black":
            var_BetEquals = "Black"
        elif var_BetTemp.lower() == "red":
            var_BetEquals = "Red"
        elif var_BetTemp.lower() == "green":
            var_BetEquals = "Green"
    elif var_BetType.lower() == "third":
        try:                                             #prevents type errors
            var_BetEquals = int(input("Which Third?"))
        except:
            print("Should be a number.")
        if var_BetEquals < 1:
            print("Thirds should be between 1 and 3")
        elif var_BetEquals > 3:
            print("Thirds should be between 1 and 3")
    betting()  
