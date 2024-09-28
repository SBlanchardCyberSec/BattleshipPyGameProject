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


def gameLoop (player: BattleshipPlayer.Player, aiplayer: BattleshipPlayer.Player, aishootcoords: list):

    while(not player.victory and not aiplayer.victory):

        print(aiplayer.board)

        print("====== Remaining Health: {} ======".format(aiplayer.health))

        print(player.board)

        print("====== Remaining Health: {} ======".format(player.health))

        getInput(player)

        if not player.victory:
            if len(aishootcoords) > 0:
                aiPlayerShoot(aiplayer, aishootcoords)
            else:
                print("AI Player has shot every cell in the board but hasn't won yet. Congrats on finding this easter egg.")
                aiplayer.victory = True


def getInput(player):

    test = input("Enter the space to shoot. Format it like D9(K to exit and L to debug AI Board and M to Debug your Board)")

    if len(test) == 1:
        x = 1 #test for quitting
    else:
        x = int(test[1:]) - 1 #valid values 0-9
    #A is 65
    y = ord(test[:1].upper()) - 65 #vaild values 0-9, 10, 11, 12

    if y == 12:
        #debug
        debug(player)
    elif y == 11:
        debug(aiplayer)
    elif y == 10:
        #quit
        player.victory = True
    elif x < 0 or x > 9 or y < 0 or y > 12:
        #out of bounds
        print("Invalid coords entered!")
    else:
        shoot (x, y, player)
    
def shoot(x, y, player):
    player.board.shootCell(x, y)
    player.updateHealth()

def aiPlayerShoot(aiplayer: BattleshipPlayer.Player, aishootcoords: list):
    (x, y) = aiPlayerRandomShot(aishootcoords)
    aiplayer.board.shootCell(x, y)
    aiplayer.updateHealth()

def aiPlayerRandomShot(aishootcoords: list) -> tuple:
    (x,y) = random.choice(aishootcoords)
    #print ("AI Randomly Shoots ({}, {})".format(x, y))
    aishootcoords.remove((x, y))
    #print ("Size of AI Shoot Coords is now : {}".format(len(aishootcoords)))
    return (x, y)


def debug(player):
    if player.board.cells[0][0].debug:
        player.board.disableDebugView()
    else:
        player.board.enableDebugView()


if __name__ == '__main__':
    #do stuff
    #aishootcoords = np.array([np.array([(i, j) for i in range(10)], dtype="i,i") for j in range(10)])
    aishootcoords = []
    for x in range(10):
        for y in range(10):
            aishootcoords.append((x, y))

    #print(aishootcoords)
    #print(coords[1,3])

    #aishootcoords.remove((1,1))

    #aishootcoords = np.delete(aishootcoords, np.where(aishootcoords == (1,1)))

    print(aishootcoords)

    player = BattleshipPlayer.Player()

    player.updateHealth()

    aiplayer = BattleshipPlayer.Player()

    aiplayer.board.aiplayer = True

    aiplayer.updateHealth()

    gameLoop(player, aiplayer, aishootcoords)