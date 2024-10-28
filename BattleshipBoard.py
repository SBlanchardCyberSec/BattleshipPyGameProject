from __future__ import annotations
#this is for a forward reference issue on checkCollision method (thanks PEP 563)
#PEP 673 adds a better way in Python 3.11 (but my venv is 3.10)

import BattleshipShip
import BattleshipApp
import pygame
import random
import numpy as np
import pandas as pd

class Board:

    def __init__(self, size=10):
        self.size = size
        self.cells = [[Cell("None") for i in range(self.size)] for y in range(self.size)]

        x = 0
        y = 0
        for row in self.cells:
            for cell in row:
                cell.x = y
                cell.y = x
                x += 1
            x = 0
            y += 1
        x = 0
        y = 0


        #coords = np.array([np.array([(i, j) for i in x_grid], dtype="i,i") for j in y_grid])
        self.health = 0
        self.ships = []
        self.aiplayer = False

        self.emptycells = []
        for x in range(self.size):
            for y in range(self.size):
                self.emptycells.append((x,y))

        self.filledcells = []

        self.genShips()


    def genShips(self):

        self.genShip(random.choice(list(BattleshipApp.Rotation)), 5, "Carrier")
        self.genShip(random.choice(list(BattleshipApp.Rotation)), 4, "Battleship")
        self.genShip(random.choice(list(BattleshipApp.Rotation)), 3, "Destroyer")
        self.genShip(random.choice(list(BattleshipApp.Rotation)), 3, "Submarine")
        self.genShip(random.choice(list(BattleshipApp.Rotation)), 2, "Patrol Boat")


    def genShip(self, rotation, length, model):

        flag = False
        if rotation.value == 0:
            #UP
            randomx = random.choice(range(self.size))
            randomy = random.choice(range(length, self.size))
        elif rotation.value == 1:
            #RIGHT
            randomx = random.choice(range(self.size - length))
            randomy = random.choice(range(self.size))
        elif rotation.value == 2:
            #DOWN
            randomx = random.choice(range(self.size))
            randomy = random.choice(range(self.size - length))            
        else:# rotation.value == 3:
            #LEFT
            randomx = random.choice(range(length, self.size))
            randomy = random.choice(range(self.size))

        tempship = BattleshipShip.Ship(length, length, model, rotation)
        temprange = CellRange(randomx, randomy, rotation, tempship)

        for coord in temprange.coords:
            if coord[0] > self.size - 1 or coord[1] > self.size - 1:
                #too big
                flag = True

            elif coord[0] < 0 or coord[1] < 0:
                #too small
                flag = True

        if not flag:
            for cr in self.filledcells:
                if temprange.checkCollision(cr):
                    #print ("Collision while placing ship {} and range: {}".format(model, temprange))
                    flag = True

            if not flag:
                self.filledcells.append(temprange)
                tempship.createShipCellRange(temprange)
                self.ships.append(tempship)
                self.health += length
                for coord in temprange.coords:
                    self.cells[coord[0]][coord[1]].containsship = True
                    self.cells[coord[0]][coord[1]].ship = model

            else:
                self.genShip(rotation, length, model)
        else:
            self.genShip(rotation, length, model)


    def shootCell(self, x, y) -> Tuple[str, BattleshipShip.Ship]:
        flag = False
        tempship = 0
        result = ""

        for ship in self.ships:
            for coord in ship.cellrange.coords:
                if coord[0] == x and coord[1] == y:
                    #ship hit here
                    ship.health -= 1
                    if ship.health == 0:
                        ship.alive = False
                        flag = True
                        tempship = ship

                        #ship.cellrange.coords.remove(coord)
                        if not self.aiplayer:
                            result = "You sank the enemy {}!".format(ship.model)
                        else:
                            result = "The AI sank your {}!".format(ship.model)
                        
                        

                    else:
                        #ship.cellrange.coords.remove(coord)
                        if not self.aiplayer:
                            result = "You hit the enemy {}!".format(ship.model)
                        else:
                            result = "The AI hit your {}!".format(ship.model)
                        




        self.cells[x][y].hitCell()

        if flag:
            for coord in tempship.cellrange.coords:
                self.cells[coord[0]][coord[1]].sankship = True

            self.ships.remove(tempship)

        return (result, tempship)


        

    def enableDebugView(self):
        for row in self.cells:
            for col in row:
                col.debug = True


    def disableDebugView(self):
        for row in self.cells:
            for col in row:
                col.debug = False

    def __repr__(self):

        result = ""
        x = 0
        
        #for x in range(10):
        #    result += " {} ".format(x)
        #result += "\n"
        #x = 0
        result += "   "
        #ASCII A = 65
        for x in range(10):
            result += " {} ".format(chr(x+65))
        result += "\n"
        x = 1

        for row in self.cells:
            result += "{} ".format(x)
            if x < 10:
                result += " " #adding additional space for 10 (due to there being an extra digit)
            for col in row:
                result += str(col)
            result += "\n"
            x += 1

        
        
        return result


class CellRange:

    def __init__(self, startx, starty, rotation: BattleshipApp.Rotation, ship: BattleshipShip.Ship):
        self.startx = startx
        self.starty = starty
        self.rotation = rotation
        self.coords = []
        self.ship = ship

        self.createRange(startx, starty, rotation, ship)


    def createRange(self, startx, starty, rotation: BattleshipApp.Rotation, ship: BattleshipShip.Ship):
        if (rotation.value == BattleshipApp.Rotation.UP.value):
            self.createRangeUp(startx, starty, ship)

        elif (rotation.value == BattleshipApp.Rotation.RIGHT.value):
            self.createRangeRight(startx, starty, ship)

        elif (rotation.value == BattleshipApp.Rotation.DOWN.value):
            self.createRangeDown(startx, starty, ship)

        else: #(rotation.value == BattleshipApp.Rotation.LEFT.value):
            self.createRangeLeft(startx, starty, ship)

    def createRangeUp(self, startx, starty, ship: BattleshipShip.Ship):
        for x in range(self.ship.length):
            self.coords.append((startx - x, starty))

    def createRangeRight(self, startx, starty, ship: BattleshipShip.Ship):
        for x in range(self.ship.length):
            self.coords.append((startx, starty + x))

    def createRangeDown(self, startx, starty, ship: BattleshipShip.Ship):
        for x in range(self.ship.length):
            self.coords.append((startx + x, starty))

    def createRangeLeft(self, startx, starty, ship: BattleshipShip.Ship):
        for x in range(self.ship.length):
            self.coords.append((startx, starty - x))

    def checkCollision(self, range2: CellRange) -> bool:
        #check somments at top import statement for type hinting here
        for coord in self.coords:
            for coord2 in range2.coords:
                if coord == coord2:
                    return True
        return False

    def __repr__(self):
        return "CellRange: startx: {}, starty: {}, coords: {}, rotation: {}, ship: {}".format(self.startx, self.starty, self.coords, self.rotation, self.ship.model)




class Cell:

    def __init__(self, ship, containsship: bool=False, discovered: bool=False, sankShip: bool=False, hitable: bool=True, debug: bool=False):
        #
        self.ship = ship
        self.containsship = False
        self.discovered = False
        self.sankship = False
        self.hitable = True
        self.debug = False
        self.rect = pygame.rect.Rect(0,0,0,0)
        self.x = 0
        self.y = 0

    def hitCell(self):
        self.discovered = True
        self.hitable = False
        return self.containsship

    def __repr__(self):
        if self.debug:
            if self.sankship:
                return " * " #already sank ship
            elif self.containsship and self.hitable:
                return " {} ".format(self.ship[0]) #not hit yet but visible to debug
            elif self.containsship:
                return " X " #has been hit
            else:
                if self.hitable:
                    return " _ " #empty and not hit yet
                else:
                    return " 0 " #empty and already hit

        elif self.discovered:
            if (self.sankship):
                return " * "
            elif (self.containsship):
                return " X "
            else:
                return " 0 "
        else:
            return " - "
