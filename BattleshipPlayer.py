import BattleshipBoard
class Player:

    #A class for the player

    def __init__(self):

        self.board = BattleshipBoard.Board()
        self.health = 0
        self.victory = False

    def updateHealth(self):
        x = 0
        for ship in self.board.ships:
            x += ship.health
        self.health = x
        if self.health == 0:
            self.victory = True


    def __repr__(self):
        return "".format()