import random

class TTTMinimaxAI:


    def __init__(self, heroPlayer, boardSize):

        self.heroPlayer = heroPlayer.lower()

        self.evilPlayer = ""
        if(self.heroPlayer.lower() == "x"):
            self.evilPlayer = "o"
        elif(self.heroPlayer.lower() == "o"):
            self.evilPlayer = "x"

        self.boardSize = boardSize

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
    
    #checks for draw
    def checkForDraw(self, moveCount):
        if(moveCount == self.boardSize ** 2):
            return True
        return False

    # check if win.
    def checkForWin(self, boardState):


        # check rows
        for row in range(0, self.boardSize):
            if(boardState[row][0] == boardState[row][1] == boardState[row][2] and boardState[row][0] != "-"):
                return True

        #check cols
        for col in range(0, self.boardSize):
            if(boardState[0][col] == boardState[1][col] == boardState[2][col] and boardState[0][col] != "-"):
                return True

        #check diagonals
        # TL -> BR
        if(boardState[0][0] == boardState[1][1] == boardState[2][2] and boardState[0][0] != "-"):
                return True

        # TR -> BL
        if(boardState[0][2] == boardState[1][1] == boardState[2][0] and boardState[0][2] != "-"):
                return True
        
        return False

    # goes through all possible moves, and returns the best result
    def getBestMove(self, player, boardState, moveCount):
        
        # end conditions
        if(self.checkForWin(boardState) and player == self.evilPlayer):
            finalState = [-1, -1, 1] # heroPlayer's move created a win state. +1 for hero
            return finalState
        elif(self.checkForWin(boardState) and player == self.heroPlayer):
            finalState = [-1, -1, -1]
            return finalState
        elif(self.checkForDraw(moveCount)):
            finalState = [-1, -1, 0] # no win state and out of moves. Draw! 0
            return finalState

        # make alist of all unplayed moves
        unplayedMoves = []
        for row in range(0, self.boardSize):
            for col in range(0, self.boardSize):
                if(boardState[row][col] == "-"):
                    unplayedMoves.append([row, col])

        # goes through all possible moves, and assigns a score to them.
        calculatedMoves = []
        for move in unplayedMoves:
            newBoardState = self.getBoardState(boardState)
            
            newBoardState[move[0]][move[1]] = player

            if(player == self.heroPlayer):
                result = self.getBestMove(self.evilPlayer, newBoardState, moveCount + 1)
                calculatedMoves.append([move[0], move[1], result[2]])

            else:
                result = self.getBestMove(self.heroPlayer, newBoardState, moveCount + 1)
                calculatedMoves.append([move[0], move[1], result[2]])

        # shuffles the list of moves, so AI vs AI doesn't play the same game every time
        random.shuffle(calculatedMoves)

        # if player is hero, return the higest scoring move
        # if player is evil, return the lowest scoring move
        bestMove = []
        if(player == self.heroPlayer):
            bestScore = -1000
            for move in calculatedMoves:
                if(move[2] > bestScore):
                    bestScore = move[2]
                    bestMove = [move[0], move[1], move[2]]
        else:
            bestScore = 1000
            for move in calculatedMoves:
                if(move[2] < bestScore):
                    bestScore = move[2]
                    bestMove = [move[0], move[1], move[2]]

        return bestMove
