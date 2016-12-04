"""
/*****************************************************
 *
 *              Gabor Vecsei
 * Email:       vecseigabor.x@gmail.com
 * Blog:        https://gaborvecsei.wordpress.com/
 * LinkedIn:    www.linkedin.com/in/vecsei-gabor
 * Github:      https://github.com/gaborvecsei
 *
 *****************************************************
 """

import sys

import numpy as np


class Court():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.court = []
        self.buildCourt()

    def buildCourt(self):
        # Build the court
        for i in range(self.height):
            court_row = []
            for k in range(self.width):
                if i == 0:
                    court_row.append('-')
                elif i == self.height - 1:
                    court_row.append('-')
                elif k == 0 and i != 0:
                    court_row.append('|')
                elif k == self.width - 1:
                    court_row.append('|')
                else:
                    court_row.append(' ')
            if len(court_row) > 0:
                self.court.append(court_row)

    def printCourt(self):
        # Prepare a string that represents the court
        screen = "\n".join(''.join(line) for line in self.court)
        # Print the court
        sys.stdout.write(screen)
        sys.stdout.flush()
        self.clearCourt()

    def putOnCourt(self, position, char):
        x, y = position
        self.court[y][x] = char

    def clearCourt(self):
        self.court = []
        self.buildCourt()

    def getCourt(self):
        return self.court

    def getWidthHeight(self):
        return self.width, self.height

    def putPlayersOnCourt(self, players):
        # i is the index in the players array
        for i, player in enumerate(players):
            self.putOnCourt(player.getPosition(), player.getCharacter())

    def putEnemiesOnCourt(self, enemies):
        # i is the index in the players array
        for i, enemy in enumerate(enemies):
            self.putOnCourt(enemy.getPosition(), enemy.getCharacter())

    # Generates a random position on the court
    # We can define a box for the generation (Xmin, Xmax, Ymin, Ymax)
    def generateRndPosOnCourt(self, box=None):
        if box is None:
            box = (1, self.width - 2, 1, self.height - 2)
        xMin, xMax, yMin, yMax = box
        return np.random.randint(xMin, xMax), np.random.randint(yMin, yMax)

    def generateRandomXPos(self):
        return np.random.randint(1, self.width - 2)
