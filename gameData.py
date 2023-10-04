class GameData:
    def __init__(self, chessboard, currentTurn, castlingStates, lastDouble, users):
        self.chessboard = chessboard
        self.currentTurn = currentTurn
        self.castlingStates = castlingStates
        self.lastDouble = lastDouble
        self.users = users
