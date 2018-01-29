# threes simulator
# oliver chen

#play NUMBER_OF_GAMES game of threes
NUMBER_OF_GAMES = 100000

#save rolls below num when you have [0, 1, 2, 3, 4, 5] die left
SAVE_IF_BELOW = [-1, -1, 2, 1, 1, 0]

import random

#roll the dice and adjust so it rolls: 0 1 2 4 5 6
def rollSingleDice():
    numRolled = random.randrange(6)
    if(numRolled > 2):
        return numRolled+1
    return numRolled

#roll numDie die and return an array of all the rolls
def rollDie(numDie):
    diceRolls = []
    for i in range(numDie):
        diceRolls.append(rollSingleDice())
    return diceRolls

#roll numDie die, take the lowewst, then take any die that are under saveIfBelowOrEqual
#return the number of points that are taken and the number of die left after the roll
def rollandSaveDie(numDie, saveIfBelowOrEqual):
    dice = rollDie(numDie)
    pointsTaken = 0

    pointsTaken += min(dice)
    dice.remove(min(dice))

    while(dice and min(dice) <= saveIfBelowOrEqual):
        pointsTaken += min(dice)
        dice.remove(min(dice))

    return pointsTaken, len(dice)

#play NUMBER_OF_GAMES games of threes. record results in an array of length 37
def playThrees():
    pointArray = [0]*37
    for i in range(NUMBER_OF_GAMES):
        currentPoints = 0
        pointsTaken = 0
        numDie = 5
        
        while numDie > 0:
            pointsTaken, numDie = rollandSaveDie(numDie,SAVE_IF_BELOW[numDie])
            currentPoints += pointsTaken
        
        pointArray[currentPoints] += 1
    return pointArray

points = playThrees()

average = 0
for i in range(37):
    average += points[i]*i/NUMBER_OF_GAMES
    print("%2d"%i + "  " + "%5.2f"%(points[i]*100/NUMBER_OF_GAMES))
print(average)
