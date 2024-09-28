import BattleshipBoard
class Ship:

    #A class for the ships
    #each has a health, model, location, direction, length, and alive state

    def __init__(self, l, h, m, r, a=True):

        self.length = l
        self.health = h
        self.model = m
        self.rotation = r
        self.alive = a
        self.cellrange = 0

    def createShipCellRange(self, cellrange: BattleshipBoard.CellRange):
        self.cellrange = cellrange

    def rotateClockwise(self):
        self.rotation = self.rotation.next

    def rotateCounterClockwise(self):
        self.rotation = self.rotation.prev

    def hitShip(self):
        this.health -= 1

        if (this.health <= 0):
            this.alive = False

    def __repr__(self):
        return "{} class Ship with Length: {}, Health: {}, Rotation: {}, IsAlive: {}, and Cell Range: {}".format(self.model, self.length, self.health, self.rotation, self.alive, self.cellrange)