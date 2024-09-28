import pygame
import random
from abc import ABC
from enum import Enum
from itertools import zip_longest
import numpy as np
#import pandas as pd

import BattleshipShip
import BattleshipBoard
import BattleshipPlayer

class Rotation(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @property
    def next(self):
        #text
        return Rotation((self.value + 1) % 4)

    @property
    def prev(self):
        return Rotation((self.value - 1) % 4)


def gameLoop (player: BattleshipPlayer.Player):

    while(not player.victory):

        print(player.board)

        print("====== Remaining Health: {} ======".format(player.health))

        getInput(player)


def getInput(player):
    x = int(input("Enter the Row (vertical axis) to shoot. (-1 to exit and 15 to enable debug printing)"))
    y = int(input("Enter the Column (horizontal axis) to shoot. (-1 to exit and 15 to enable debug printing)"))

    if x == 15 and y == 15:
        #debug
        debug(player)
    elif x == -1 or y == -1:
        #quit
        player.victory = True
    elif x < -1 or x > 9 or y < -1 or y > 9:
        #out of bounds
        print("Invalid coords entered!")
    else:
        shoot (x, y, player)
    
def shoot(x, y, player):
    player.board.shootCell(x, y)
    player.updateHealth()


def debug(player):
    if player.board.cells[0][0].debug:
        player.board.disableDebugView()
    else:
        player.board.enableDebugView()


if __name__ == '__main__':
    #do stuff
    #coords = np.array([np.array([(i, j) for i in range(10)], dtype="i,i") for j in range(10)])
    #print(coords)
    #print(coords[1,3])

    player = BattleshipPlayer.Player()

    player.updateHealth()

    gameLoop(player)




    #ship = BattleshipShip.Ship(3, 3, 'Submarine', Rotation.RIGHT)
    #board = BattleshipBoard.Board()
    #cellrange = BattleshipBoard.CellRange(1, 1, ship.rotation, ship, board)

    #ship2 = BattleshipShip.Ship(3, 3, 'Destroyer', Rotation.DOWN)
    #cellrange2 = BattleshipBoard.CellRange(4, 0, ship2.rotation, ship2, board)


    #print(board)

    #for row in board.cells:
    #   print (row)

    #print ("Debug now")

    #board.enableDebugView()

    #print(board)
    #for row in board.cells:
    #    print (row)
    
    #print(cellrange)
    #print(cellrange2)
    #print(cellrange.checkCollision(cellrange2))