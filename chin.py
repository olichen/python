# chin simulator

import random

#play NUMBER_OF_GAMES game of chin
NUMBER_OF_GAMES = 100000

#roll 3 die and return an array of all the rolls
def rollDie():
    diceRolls = []
    for i in range(3):
        diceRolls.append(random.randrange(6) +1)
    diceRolls.sort()
    return diceRolls

def checkIf123(diceRolls):
    if diceRolls==[1,2,3]:
        return True
    return False

def checkIf456(diceRolls):
    if diceRolls==[4,5,6]:
        return True
    return False

def checkIfTriples(diceRolls):
    if len(set(diceRolls))==1:
        return True
    return False

def checkIfDoubles(diceRolls):
    if len(set(diceRolls))==2:
        return True
    return False

#get the third number from a doubles roll
def getThirdNumber(diceRolls):
    return sum(diceRolls) - sum(set(diceRolls))

def checkIfAutoWin(diceRolls):
    if checkIf456(diceRolls):
        return True
    if checkIfTriples(diceRolls):
        return True
    if checkIfDoubles(diceRolls):
        if getThirdNumber(diceRolls)==6:
            return True
    return False

def checkIfAutoLose(diceRolls):
    if checkIf123(diceRolls):
        return True
    if checkIfDoubles(diceRolls):
        if getThirdNumber(diceRolls)==1:
            return True
    return False

#roll the die. return 1 on self win, 0 on self lose, -num on doubles
def rollChin():
    diceRolls = rollDie()
    if checkIfAutoWin(diceRolls):
        return 1
    if checkIfAutoLose(diceRolls):
        return 0
    if checkIfDoubles(diceRolls):
        return -(getThirdNumber(diceRolls))

#dealer rolls til they get a result. return 1 on player win, 0 on player loss, -num if doubles
def dealerRollChin():
    while True:
        roll = rollChin()
        #reverse wins; player wins if dealer loses and vice versa
        if roll==1:
            return 0
        if roll==0:
            return 1
        if roll is not None:
            return roll

#player rolls til they get a result. return 1 on player win, 0 on player loss, -num if player rolls a double
def playerRollChin():
    while True:
        #drops die
        if random.randrange(100)<2:
            return 0
        roll = rollChin()
        if roll is not None:
            return roll

#compare rolls. return 1 on player win, 0 on player loss, -1 on tie
def compareRolls(dealerRoll, playerRoll):
    dealerRoll = -(dealerRoll)
    playerRoll = -(playerRoll)
    if playerRoll > dealerRoll:
        return 1
    if dealerRoll > playerRoll:
        return 0
    if dealerRoll == playerRoll:
        return -1

#play a game of chin. return 1 on win, 0 on lose, keep rolling if we tie
def chin():
    while True:
        dealerRoll = dealerRollChin()
        if dealerRoll>=0:
            return dealerRoll

        playerRoll = playerRollChin()
        if playerRoll>=0:
            return playerRoll

        comparison = compareRolls(dealerRoll, playerRoll)
        if comparison>=0:
            return comparison

numberOfWins=0
for i in range(NUMBER_OF_GAMES):
    numberOfWins += chin()

print("Win%:")
print(numberOfWins/NUMBER_OF_GAMES)
print("Number of games:")
print(NUMBER_OF_GAMES)
