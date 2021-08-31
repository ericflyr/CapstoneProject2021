import numpy as np
import itertools
import random


class TTTReinforcementLearningAI:


    def __init__(self, heroPlayer, boardSize):

        self.heroPlayer = heroPlayer.lower()

        self.evilPlayer = ""
        if(self.heroPlayer.lower() == "x"):
            self.evilPlayer = "o"
        elif(self.heroPlayer.lower() == "o"):
            self.evilPlayer = "x"

        self.boardSize = boardSize

        # creates a lit of all possible TTT states
        self.allPossibleStates = []
        for i in itertools.product(["x", "o", "-"], repeat = boardSize ** 2):
            self.allPossibleStates.append([list(i[0:3]),list(i[3:6]),list(i[6:10])])

        # variables for loading different datasets

        #loadfilename_trainedStateValues_X = "tictactoe\\training_data\\trainedStateValues_X.txt"
        #loadfilename_trainedStateValues_O = "tictactoe\\training_data\\trainedStateValues_O.txt"

        #loadfilename_trainedStateValues_X = "tictactoe\\training_data\\long_trainedStateValues_X.txt"
        #loadfilename_trainedStateValues_O = "tictactoe\\training_data\\long_trainedStateValues_O.txt"

        loadfilename_trainedStateValues_X = "tictactoe\\training_data\\gen3_trainedStateValues_X.txt"
        loadfilename_trainedStateValues_O = "tictactoe\\training_data\\gen3_trainedStateValues_O.txt"

        self.trainedStateValues_X = np.loadtxt(loadfilename_trainedStateValues_X, dtype=np.float64)
        self.trainedStateValues_O = np.loadtxt(loadfilename_trainedStateValues_O, dtype=np.float64)


    # create empty Board
    def createEmptyBoard(self):
        newBoard = []

        for _ in range(0, self.boardSize):
            rowList = []
            for _ in range(0, self.boardSize):
                rowList.append("-")
            newBoard.append(rowList)

        return newBoard

    # copy boardState
    def getBoardState(self, boardState):
        newBoard = self.createEmptyBoard()

        for row in range(0, self.boardSize):
            for col in range(0, self.boardSize):
                newBoard[row][col] = boardState[row][col]

        return newBoard
    
    def getBestMove(self, player, boardState):
        
        # make alist of all unplayed moves
        availableMoves = []
        for row in range(0, self.boardSize):
            for col in range(0, self.boardSize):
                if(boardState[row][col] == "-"):
                    availableMoves.append([row, col])


        # looks up the values for all possible moves
        # pairs them with their associated values
        availableMovesAndValues = []
        for move in availableMoves:

            # get copy of boardState, play move
            nextBoardState = self.getBoardState(boardState)
            nextBoardState[move[0]][move[1]] = player

            # get index of new Board state
            nextBoardStateIndex = self.allPossibleStates.index(nextBoardState)

            # grabs the value the AI has for the nextBoardState
            if(player == "x"):
                availableMovesAndValues.append([move[0], move[1], self.trainedStateValues_X[nextBoardStateIndex]])
            else:
                availableMovesAndValues.append([move[0], move[1], self.trainedStateValues_X[nextBoardStateIndex]])

        #print(availableMovesAndValues)

        # shuffles to add variety when there are moves with equal values
        random.shuffle(availableMovesAndValues)

        # finds the best move available
        bestValue = availableMovesAndValues[0][2]
        bestMoveIndex = 0
        for move in availableMovesAndValues:
            if(move[2] > bestValue):
                bestValue = move[2]
                bestMoveIndex = availableMovesAndValues.index(move)


        bestMove = [availableMovesAndValues[bestMoveIndex][0], availableMovesAndValues[bestMoveIndex][1]]

        return bestMove


    