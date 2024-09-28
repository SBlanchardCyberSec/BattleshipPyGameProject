import pygame #requires pygame-ce (not regular pygame) for rendering newline chars
import random
from abc import ABC
from enum import Enum
from itertools import zip_longest
import numpy as np
#import pandas as pd

import BattleshipShip
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


SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600

ainoshootflag = True #global bool for ai no shoot flag
gameoverflag = False #global bool for not allowing mouse input after game end

cellsize = 70 
cellbordersize = 2
margin = 25 

textwidth = (SCREEN_WIDTH - margin * 4) // 3

cellbordercolor = pygame.color.Color("black")
watercolor = pygame.color.Color("blue")
hitcolor = pygame.color.Color("darkred")
misscolor = pygame.color.Color("lightcyan")
emptyscannedcolor = pygame.color.Color("cadetblue")
sankshipcolor = pygame.color.Color("fuchsia")
carriercolor = pygame.color.Color("chocolate1")
battleshipcolor = pygame.color.Color("springgreen")
destroyercolor = pygame.color.Color("tomato")
submarinecolor = pygame.color.Color("yellow")
patrolboatcolor = pygame.color.Color("violet")
backgroundcolor = pygame.color.Color(20, 50, 20)
textcolor = pygame.color.Color("white")
combatlog = []

def debug(player: BattleshipPlayer.Player):
    if player.board.cells[0][0].debug:
        player.board.disableDebugView()
    else:
        player.board.enableDebugView()

def addCombatLogMsg (message: str):
    global combatlog
    if len(message) > 1:
        if len(combatlog) > 3:
            combatlog = combatlog[1:]
        combatlog.append(message)

def Logic (ai:BattleshipPlayer.Player, player:BattleshipPlayer.Player, aishootcoords: list, eventlist: list[pygame.Event]):
    #player input here
    global ainoshootflag 
    global gameoverflag
    for event in eventlist:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                
                if not player.board.cells[0][0].debug:
                    addCombatLogMsg("Enabling Debug Mode")
                else:
                    addCombatLogMsg("Disabling Debug Mode")

                debug(player)
                #print("Player (0, 0 and (1, 1) debug is {}, {}".format(player.board.cells[0][0].debug, player.board.cells[1][1].debug))
                debug(aiplayer)
        elif event.type == pygame.MOUSEBUTTONUP:
            if not gameoverflag:
                #player shoot here
                x, y = pygame.mouse.get_pos()
                for row in player.board.cells:
                    for cell in row:
                        if (cell.rect.collidepoint(x, y)):
                            #cell collision
                            if cell.hitable:
                                #print ("Shooting Cell at ({}, {})".format(cell.x, cell.y))
                                result = player.board.shootCell(cell.x, cell.y)
                                addCombatLogMsg(result)
                                player.updateHealth()
                                ainoshootflag = False
                        



    if not ainoshootflag:
        #ai shoot here
        (x,y) = random.choice(aishootcoords)
        #print ("AI Randomly Shoots ({}, {})".format(x, y))
        aishootcoords.remove((x, y))
        #print ("Size of AI Shoot Coords is now : {}".format(len(aishootcoords)))
        result = ai.board.shootCell(x, y)
        addCombatLogMsg(result)
        ai.updateHealth()
        ainoshootflag = True

    #end of Logic()
    pass

def Render(screen: pygame.display.set_mode, font: pygame.font.SysFont, ai: BattleshipPlayer.Player, player: BattleshipPlayer.Player):

    #first background color
    screen.fill(backgroundcolor)


    #next text for AI board
    aiboardtitle = "AI Board: \nHealth Remaining: {}\nShips Left: \n".format(ai.health)
    for ship in ai.board.ships:
        #aiboardtitle += repr(ship)
        aiboardtitle += "{}, ".format(ship.model)
    aiboardtitle = aiboardtitle[0:len(aiboardtitle) - 2]

    aiboardtitletext = font.render(aiboardtitle, True, textcolor, None, textwidth)

    aiboardtitlerect = aiboardtitletext.get_rect(midtop = (margin + (textwidth // 2), margin))

    #midtop = (margin + textwidth + margin + (textwidth // 2), margin)

    aiboardtitlesurface = pygame.surface.Surface(aiboardtitlerect.size)
    #aiboardtitlesurface.fill("darkorange")
    aiboardtitlesurface.fill(backgroundcolor)
    aiboardtitlesurface.blit(aiboardtitletext, (0, 0))

    aiboardtitletext = aiboardtitlesurface

    screen.blit(aiboardtitletext, aiboardtitlerect)

    #next the ai board rendering

    #aiboardtest = pygame.rect.Rect(25, SCREEN_HEIGHT - margin - cellsize * 10, cellsize * 10, cellsize * 10)
    #pygame.draw.rect(screen, watercolor, aiboardtest)


    celloffsetx = 0
    celloffsety = 0
    tempcolor = watercolor
    for row in ai.board.cells:
        for cell in row:
            x = repr(cell)[1:2]
            if x == "0": #empty and hit
                tempcolor = misscolor
            elif x == "_": #empty and not hit (known empty) 
                tempcolor = emptyscannedcolor
            elif x == "-": #empty and not known (unknown)
                tempcolor = watercolor
            elif x == "X": #hit ship (not debug)
                tempcolor = hitcolor
            elif x == "*": #sank ship
                tempcolor = sankshipcolor
            elif x == "C": #debug
                tempcolor = carriercolor
            elif x == "B": #debug
                tempcolor = battleshipcolor
            elif x == "D": #debug
                tempcolor = destroyercolor
            elif x == "S": #debug
                tempcolor = submarinecolor
            elif x == "P": #debug
                tempcolor = patrolboatcolor
            
            #cell
            cell.rect = pygame.rect.Rect(margin + celloffsetx, 
            SCREEN_HEIGHT - margin - cellsize * 10 + celloffsety, cellsize, cellsize)

            pygame.draw.rect(screen, tempcolor, cell.rect)

            #cell border
            pygame.draw.rect(screen, cellbordercolor, cell.rect, cellbordersize)

            celloffsetx += cellsize
        celloffsetx = 0
        celloffsety += cellsize




    #next the combat log text

    combatlogtemp = "Combat Log: \n"
    for log in combatlog:
        combatlogtemp += str(log) + "\n"

    combatlogtext = font.render(combatlogtemp, True, textcolor, None, textwidth)
    combatlogrect = combatlogtext.get_rect(midtop = (margin + textwidth + margin + (textwidth // 2), margin))

    combatlogsurface = pygame.surface.Surface(combatlogrect.size)
    #combatlogsurface.fill("darkorange")
    combatlogsurface.fill(backgroundcolor)
    combatlogsurface.blit(combatlogtext, (0, 0))

    combatlogtext = combatlogsurface


    screen.blit(combatlogtext, combatlogrect)




    #next the player board text

    playertitle = "Player Board: \nHealth Remaining: {}\nShips Left: \n".format(player.health)
    for ship in player.board.ships:
        #playertitle += repr(ship)
        playertitle += "{}, ".format(ship.model)
    playertitle = playertitle[0:len(playertitle) - 2]

    playertitletext = font.render(playertitle, True, textcolor, None, textwidth)

    playertitlerect = playertitletext.get_rect()
    #playertitlerect.center = 
    playertitlerect.midtop = (SCREEN_WIDTH - margin - (textwidth // 2), margin)

    playertitlesurface = pygame.surface.Surface(playertitlerect.size)
    #playertitlesurface.fill("darkorange")
    playertitlesurface.fill(backgroundcolor)
    playertitlesurface.blit(playertitletext, (0, 0))

    playertitletext = playertitlesurface

    screen.blit(playertitletext, playertitlerect)




    #next the player board

    #playerboardtest = pygame.rect.Rect(SCREEN_WIDTH - 25 - cellsize * 10, SCREEN_HEIGHT - margin - cellsize * 10, cellsize * 10, cellsize * 10)
    #pygame.draw.rect(screen, watercolor, playerboardtest)

    celloffsetx = 0
    celloffsety = 0
    tempcolor = watercolor
    for row in player.board.cells:
        for cell in row:
            x = repr(cell)[1:2]
            if x == "0": #empty and hit
                tempcolor = misscolor
            elif x == "_": #empty and not hit (known empty) 
                tempcolor = emptyscannedcolor
            elif x == "-": #empty and not known (unknown)
                tempcolor = watercolor
            elif x == "X": #hit ship (not debug)
                tempcolor = hitcolor
            elif x == "*": #sank ship
                tempcolor = sankshipcolor
            elif x == "C": #debug
                tempcolor = carriercolor
            elif x == "B": #debug
                tempcolor = battleshipcolor
            elif x == "D": #debug
                tempcolor = destroyercolor
            elif x == "S": #debug
                tempcolor = submarinecolor
            elif x == "P": #debug
                tempcolor = patrolboatcolor
            
            #cell
            cell.rect = pygame.rect.Rect(SCREEN_WIDTH - 25 - cellsize * 10 + celloffsetx, 
            SCREEN_HEIGHT - margin - cellsize * 10 + celloffsety, cellsize, cellsize)
            pygame.draw.rect(screen, tempcolor, cell.rect)

            #cell border
            pygame.draw.rect(screen, cellbordercolor, cell.rect, cellbordersize)

            celloffsetx += cellsize
        celloffsetx = 0
        celloffsety += cellsize

    #end of Render()



if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
    font.align = pygame.FONT_CENTER
    clock = pygame.time.Clock()
    pygame.display.set_caption("Battleship")

    player = BattleshipPlayer.Player()

    player.updateHealth()

    aiplayer = BattleshipPlayer.Player()

    aiplayer.board.aiplayer = True

    aiplayer.updateHealth()

    aishootcoords = []
    for x in range(10):
        for y in range(10):
            aishootcoords.append((x, y))

    #game loop here
    run = True
    #debug = True
    while run:
        #Check for poll events
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
        #Game Logic here
        Logic(aiplayer, player, aishootcoords, eventlist)
        
        
        #Rendering Here
        Render(screen, font, aiplayer, player)

        if aiplayer.health < 1 or player.health < 1:
            if not gameoverflag:
                if aiplayer.health < 1:
                    addCombatLogMsg("Game Over, You Lose!")
                    addCombatLogMsg("Game Over, You Lose!")
                    addCombatLogMsg("Game Over, You Lose!")
                    addCombatLogMsg("Game Over, You Lose!")
                else:
                    addCombatLogMsg("Game Over, You Win!")
                    addCombatLogMsg("Game Over, You Win!")
                    addCombatLogMsg("Game Over, You Win!")
                    addCombatLogMsg("Game Over, You Win!")

                gameoverflag = True


        #Update Display Here

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

