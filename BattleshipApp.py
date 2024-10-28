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

aihitshots = [] #track the recent hit shots
aipossibleshotsafterhit = [] #saves possible shots for AI that make sense

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
    global aihitshots
    global aipossibleshotsafterhit


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
                                (result, resultship) = player.board.shootCell(cell.x, cell.y)
                                addCombatLogMsg(result)
                                player.updateHealth()
                                ainoshootflag = False




    if not ainoshootflag:
        #ai shoot here
        # #Better AI aiming here
        #Take into account previous ship hits

        if len(aihitshots) < 1:
            #no saved hits - choose random
            (x,y) = random.choice(aishootcoords)


        elif len(aihitshots) == 1: #1 hit without sink
            aipossibleshotsafterhit = []


            for (x, y) in aishootcoords: #all cells not hit yet
                for (xx, yy) in aihitshots: #cells hit and point of interest
                    if ((abs(x - xx) <= 1) and (abs(y - yy) <= 1)): #if adjacent (includes diagonals)
                        if ((x == xx) ^ (y == yy)): #exclude diagonals here as only checking for orthogonal 
                            #(this could be an or as the already hit cell was removed previously) but xor is cleaner and safer

                            #print("Coord ({}, {}) added to temp with hitshot coord ({}, {})".format(x, y, xx, yy))
                            aipossibleshotsafterhit.append((x, y)) #add shot to possible list

            
            (x, y) = random.choice(aipossibleshotsafterhit)

        else: #greater than 1 hits without a sink
            aipossibleshotsafterhit = []
            tempcoord = aihitshots[0]
            orientation = 0 #vertical or horizontal with a fail condition

            for coord in aihitshots:
                if coord != tempcoord:
                    if coord[0] == tempcoord[0]: #x's are matching horizontal (my axises are switched)
                        orientation = 1
                    
                    elif coord[1] == tempcoord[1]: #y's match vertical (my axises are switched)
                        orientation = 2

                    else: #coord is not adjacent to tempcoord
                        tempcoord = coord
                else: #do nothing (matching coords)
                    pass

            if orientation == 1: #horizontal
                for (x, y) in aishootcoords: #all cells not hit yet
                    for (xx, yy) in aihitshots:
                            if ((x == xx) and (abs(y - yy) <= 1)): #adjacent to coord and horizontal only
                                #print("Coord ({}, {}) added to temp with hitshot coord ({}, {}) known only horizontal".format(x, y, xx, yy))
                                aipossibleshotsafterhit.append((x, y)) #add shot to possible list


            elif orientation == 2: #vertical
                for (x, y) in aishootcoords: #all cells not hit yet
                    for (xx, yy) in aihitshots:
                            if ((abs(x - xx) <= 1) and (y == yy)): #adjacent to coord and vertical only ((abs(x - xx) <= 1) and (y == yy))
                                #print("Coord ({}, {}) added to temp with hitshot coord ({}, {}) known only vertical".format(x, y, xx, yy))
                                aipossibleshotsafterhit.append((x, y)) #add shot to possible list

            
            else: #unknown direction
                #print("ERROR: Direction for AI shot focus unknown (this should not be possible) Congrats, you found the impossible bug! I never found this in testing.")
                pass #actually need this here as the print is commented          


            if len(aipossibleshotsafterhit) > 0:
                (x, y) = random.choice(aipossibleshotsafterhit) #raises index error if empty

            else: #failsafe here in case direction unknown
                (x, y) = random.choice(aishootcoords)
            
            
        #print("Aipossibleshotsafterhit -> {}".format(aipossibleshotsafterhit))
        #print("AI shooting ({}, {})".format(x, y))


        #print("Aishootcoords -> {}".format(aishootcoords))
        aishootcoords.remove((x, y))
        #print ("Size of AI Shoot Coords is now : {}".format(len(aishootcoords)))
        (result, resultship) = ai.board.shootCell(x, y)

        

        #keep track of previous hits here
        #The AI sank - 11 characters
        if 'hit' in result[:12]:
            #hit but not sank
            #add current coords to list of hits
            aihitshots.append((x, y))


        elif 'sank' in result[:12]:
            #sank ship
            
            aihitshots.append((x, y)) #have to add this to remove it after

            #print("Clearing this Cellrange from aihitshots -> {}".format(resultship.cellrange.coords))
            #print("Aihitshots is this before removing -> {}".format(aihitshots))

            #need to do this to preserve hits for other ships as opposed to clearing list
            for coord in resultship.cellrange.coords:
                aihitshots.remove(coord)

        addCombatLogMsg(result)
        ai.updateHealth()
        ainoshootflag = True

    #end of Logic()
    pass

def Render(screen: pygame.display.set_mode, font: pygame.font.SysFont, ai: BattleshipPlayer.Player, player: BattleshipPlayer.Player):

    #first background color
    screen.fill(backgroundcolor)


    #next text for AI board
    renderBoardText(screen, font, ai, True)


    #next the ai board rendering

    renderPlayerBoard(ai, True)



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

    renderBoardText(screen, font, player, False)


    #next the player board
    renderPlayerBoard(player, False)

    #end of Render()




#move text rendering to function to reduce duplicate code
def renderBoardText(screen: pygame.display.set_mode, font: pygame.font.SysFont, player: BattleshipPlayer.Player, ai: bool):

    if ai:
        playertitle = "AI "
        
    else:
        playertitle = "Player "



    playertitle += "Board: \nHealth Remaining: {}\nShips Left: \n".format(player.health)

    for ship in player.board.ships:
        #playertitle += repr(ship)
        playertitle += "{}, ".format(ship.model)
    playertitle = playertitle[0:len(playertitle) - 2] #cut off last , and space at end of string (see line above)

    playertitletext = font.render(playertitle, True, textcolor, None, textwidth)

    if ai:
        playertitlerect = playertitletext.get_rect(midtop = (margin + (textwidth // 2), margin))
        
    else:
        playertitlerect = playertitletext.get_rect(midtop = (SCREEN_WIDTH - margin - (textwidth // 2), margin))
        #playertitlerect.center = 
        #playertitlerect.midtop = (SCREEN_WIDTH - margin - (textwidth // 2), margin)



    playertitlesurface = pygame.surface.Surface(playertitlerect.size)
    #playertitlesurface.fill("darkorange")
    playertitlesurface.fill(backgroundcolor)
    playertitlesurface.blit(playertitletext, (0, 0))

    playertitletext = playertitlesurface

    screen.blit(playertitletext, playertitlerect)
    





#move board rendering to function to reduce duplicate code
def renderPlayerBoard(player: BattleshipPlayer.Player, ai: bool):
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

            if (ai): #ai player board
                cell.rect = pygame.rect.Rect(margin + celloffsetx, 
                SCREEN_HEIGHT - margin - cellsize * 10 + celloffsety, cellsize, cellsize)

            else: #player board
                cell.rect = pygame.rect.Rect(SCREEN_WIDTH - 25 - cellsize * 10 + celloffsetx, 
                SCREEN_HEIGHT - margin - cellsize * 10 + celloffsety, cellsize, cellsize)


            pygame.draw.rect(screen, tempcolor, cell.rect)

            #cell border
            pygame.draw.rect(screen, cellbordercolor, cell.rect, cellbordersize)

            celloffsetx += cellsize
        celloffsetx = 0
        celloffsety += cellsize



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

