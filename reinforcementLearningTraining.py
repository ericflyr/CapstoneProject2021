import numpy as np
import itertools
import random

from minimaxAI import TTTMinimaxAI


# 3x3 board
boardSize = 3

loadfilename_trainedStateValues_X = ""
loadfilename_trainedStateValues_O = ""
savefilename_trainedStateValues_X = ""
savefilename_trainedStateValues_O = ""
createNewStateValuesFiles = False
loadStateValuesFiles = False


# scenarios are used to switch between different sets of load / save files.
# commen / uncomment as needed


scenario = "rl vs rl"
#scenario = "rl vs rl, multigen 1"
#scenario = "rl vs rl, multigen 2"
#scenario = "rl vs rl, multigen 3"
#scenario = "rl_x vs mm_o"
#scenario = "mm_x vs rl_o"

# basic training, 1 generation
if(scenario == "rl vs rl"):
    createNewStateValuesFiles = True
    loadStateValuesFiles = False

    savefilename_trainedStateValues_X = "tictactoe\\training_data\\trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\trainedStateValues_O.txt"

#beginning of multi-generation training
elif(scenario =="rl vs rl, multigen 1"):
    createNewStateValuesFiles = True
    loadStateValuesFiles = False

    savefilename_trainedStateValues_X = "tictactoe\\training_data\\gen1_trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\gen1_trainedStateValues_O.txt"

elif(scenario =="rl vs rl, multigen 2"):
    createNewStateValuesFiles = False
    loadStateValuesFiles = True

    loadfilename_trainedStateValues_X = "tictactoe\\training_data\\gen1_trainedStateValues_X.txt"
    loadfilename_trainedStateValues_O = "tictactoe\\training_data\\gen1_trainedStateValues_O.txt"
    savefilename_trainedStateValues_X = "tictactoe\\training_data\\gen2_trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\gen2_trainedStateValues_O.txt"

elif(scenario =="rl vs rl, multigen 3"):
    createNewStateValuesFiles = False
    loadStateValuesFiles = True

    loadfilename_trainedStateValues_X = "tictactoe\\training_data\\gen2_trainedStateValues_X.txt"
    loadfilename_trainedStateValues_O = "tictactoe\\training_data\\gen2_trainedStateValues_O.txt"
    savefilename_trainedStateValues_X = "tictactoe\\training_data\\gen3_trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\gen3_trainedStateValues_O.txt"

# for training against MiniMax AI (very slow....)
elif(scenario =="rl_x vs mm_o"):
    mmAI = TTTMinimaxAI("o", 3)

    createNewStateValuesFiles = True
    loadStateValuesFiles = False

    savefilename_trainedStateValues_X = "tictactoe\\training_data\\mmO_trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\mmO_trainedStateValues_O.txt"

elif(scenario =="mm_x vs rl_o"):
    mmAI = TTTMinimaxAI("x", 3)

    createNewStateValuesFiles = True
    loadStateValuesFiles = False

    savefilename_trainedStateValues_X = "tictactoe\\training_data\\mmX_trainedStateValues_X.txt"
    savefilename_trainedStateValues_O = "tictactoe\\training_data\\mmX_trainedStateValues_O.txt"



# create empty Board
def createEmptyBoard():
    newBoard = []

    for _ in range(0, boardSize):
        rowList = []
        for _ in range(0, boardSize):
            rowList.append("-")
        newBoard.append(rowList)

    return newBoard

# copy boardState
def getBoardState(boardState):
    newBoard = createEmptyBoard()

    for row in range(0, boardSize):
        for col in range(0, boardSize):
            newBoard[row][col] = boardState[row][col]

    return newBoard

# check if win. only work for 3x3 boards
def checkForWin(player, boardState):


    # check rows
    for row in range(0, boardSize):
        if(boardState[row][0] == boardState[row][1] == boardState[row][2] and boardState[row][0] == player):
            return True

    #check cols
    for col in range(0, boardSize):
        if(boardState[0][col] == boardState[1][col] == boardState[2][col] and boardState[0][col] == player):
            return True

    #check diagonals
    # TL -> BR
    if(boardState[0][0] == boardState[1][1] == boardState[2][2] and boardState[0][0] == player):
            return True

    # TR -> BL
    if(boardState[0][2] == boardState[1][1] == boardState[2][0] and boardState[0][2] == player):
            return True
    
    return False


# calculates all possible states and saves them to a list
allPossibleStates = []
for i in itertools.product(["x", "o", "-"], repeat = boardSize ** 2):
    allPossibleStates.append([list(i[0:3]),list(i[3:6]),list(i[6:10])])

# write allStates to a file
"""
with open('tictactoe\\allPossibleStates.txt', 'w') as file:
    for state in allPossibleStates:
        file.write('%s\n' % state)
file.close()
"""

numStates = len(allPossibleStates)
numActions = boardSize ** 2

print("Number of States:", numStates)
print("Number of Actions:", numActions)

# variables for saving values for each state
trainedStateValues_X = None
trainedStateValues_O = None

# start a fresh training file
if(createNewStateValuesFiles):

    # fill with 0s to start
    trainedStateValues_X = np.full(numStates, 0.0)
    trainedStateValues_O = np.full(numStates, 0.0)

    # fill in values for wins / losses (+1 / - 1)
    for i in range(0, numStates):

        xWins = checkForWin("x", allPossibleStates[i])
        oWins = checkForWin("o", allPossibleStates[i])

        if(xWins):
            trainedStateValues_X[i] = 1
            trainedStateValues_O[i] = -1
        elif(oWins):
            trainedStateValues_X[i] = -1
            trainedStateValues_O[i] = 1




# updates state value for x
def updateStateValue_X(currentIndex, nextIndex, learningRate):
    # curValue = curValue + (nextValue - curValue) * learningRate
    newValue = trainedStateValues_X[currentIndex] + learningRate * (trainedStateValues_X[nextIndex] - trainedStateValues_X[currentIndex])
    trainedStateValues_X[currentIndex] = newValue

# updates state value for o
def updateStateValue_O(currentIndex, nextIndex, learningRate):
    newValue = trainedStateValues_O[currentIndex] + learningRate * (trainedStateValues_O[nextIndex] - trainedStateValues_O[currentIndex])
    trainedStateValues_O[currentIndex] = newValue

# gets the best move
def getBestMove(player, boardState, exploreNextMove):
    
    # make alist of all unplayed moves
    availableMoves = []
    for row in range(0, boardSize):
        for col in range(0, boardSize):
            if(boardState[row][col] == "-"):
                availableMoves.append([row, col])


    # looks up the values for all possible moves
    # saves their associated values
    availableMovesAndValues = []
    for move in availableMoves:

        # get copy of boardState, play move
        nextBoardState = getBoardState(boardState)
        nextBoardState[move[0]][move[1]] = player

        # get index of new Board state
        nextBoardStateIndex = allPossibleStates.index(nextBoardState)

        # grabs the value the AI has for the nextBoardState
        if(player == "x"):
            availableMovesAndValues.append([move[0], move[1], trainedStateValues_X[nextBoardStateIndex]])
        else:
            availableMovesAndValues.append([move[0], move[1], trainedStateValues_O[nextBoardStateIndex]])

    # shuffles list to add variety when moves have equal value
    random.shuffle(availableMovesAndValues)

    # finds best move index
    bestValue = availableMovesAndValues[0][2]
    bestMoveIndex = 0
    for move in availableMovesAndValues:
        if(move[2] > bestValue):
            bestValue = move[2]
            bestMoveIndex = availableMovesAndValues.index(move)

    # check if AI is Exploring or Exploiting
    bestMove = []
    if(exploreNextMove): # exploring
        randomMove = random.choice(availableMovesAndValues) # randomly picks a move
        bestMove = [randomMove[0], randomMove[1]]

    else: # exploiting
        bestMove = [availableMovesAndValues[bestMoveIndex][0], availableMovesAndValues[bestMoveIndex][1]]

    return bestMove

# explore or exploit
def decideToExploreOrExploit(epsilon):
    if(np.random.uniform(0, 1) <= epsilon): # exploring
        return True
    return False


# training AI

# load previous data, if needed
if(loadStateValuesFiles):
    trainedStateValues_X = np.loadtxt(loadfilename_trainedStateValues_X, dtype=np.float64)
    trainedStateValues_O = np.loadtxt(loadfilename_trainedStateValues_O, dtype=np.float64)


learningRate = 0.2
epsilon = 0.3
numIterations = 10000

totalMoves = 0
countExplore = 0
countExploit = 0

for iteration in range(0, numIterations):

    moveCount = 0
    boardState = createEmptyBoard()

    gameOver = False
    currentPlayer = "o" # X plays first, so we initialize it to o

    while(not gameOver):

        currentBoardStateIndex = allPossibleStates.index(boardState)
        moveCount += 1

        # switches the current player
        if(currentPlayer == "o"):
            currentPlayer = "x"
        elif(currentPlayer == "x"):
            currentPlayer = "o"

        exploreNextMove = decideToExploreOrExploit(epsilon)
        if(exploreNextMove):
            epsilon *= 0.99999
            countExplore += 1
        else:
            countExploit += 1

        if(currentPlayer == "x"):
            # able to switch from getting move from RL or MM ai, depending on scenario
            if(scenario =="mm_x vs rl_o"):
                getResult = mmAI.getBestMove(currentPlayer, boardState, moveCount)
                aiMove = [getResult[0], getResult[1]]
            else:
                aiMove = getBestMove(currentPlayer, boardState, exploreNextMove)
            boardState[aiMove[0]][aiMove[1]] = currentPlayer
            nextBoardStateIndex = allPossibleStates.index(boardState)
        else:
            if(scenario =="rl_x vs mm_o"):
                getResult = mmAI.getBestMove(currentPlayer, boardState, moveCount)
                aiMove = [getResult[0], getResult[1]]
            else:
                aiMove = getBestMove(currentPlayer, boardState, exploreNextMove)
            boardState[aiMove[0]][aiMove[1]] = currentPlayer
            nextBoardStateIndex = allPossibleStates.index(boardState)

        # update currentState values
        updateStateValue_X(currentBoardStateIndex, nextBoardStateIndex, learningRate)
        updateStateValue_O(currentBoardStateIndex, nextBoardStateIndex, learningRate)

        if(checkForWin(currentPlayer, boardState)):
            gameOver = True

        # checks for draws
        if(moveCount == boardSize ** 2):
            gameOver = True
    
    totalMoves += moveCount

    # prints updates to screen
    if(iteration % 100 == 0):
        print("---")
        print("Iteration Number:", iteration, "out of", numIterations)
        print("Move Count:", totalMoves, "Current Epsilon:", epsilon)
        print("Explore Count:", countExplore, "Exploit Count:", countExploit)


print("---")
print(numIterations,"Complete")
print("Total Move Count:", totalMoves, "Final Epsilon:", epsilon)
print("Total Explore Count:", countExplore, "Total Exploit Count:", countExploit)


# save training values once done
np.savetxt(savefilename_trainedStateValues_X, trainedStateValues_X, fmt = '%.6f')
np.savetxt(savefilename_trainedStateValues_O, trainedStateValues_O, fmt = '%.6f')

