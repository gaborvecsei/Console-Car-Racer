# Windows OS specific:
import msvcrt
import sys
import time

import numpy as np

from Cars.cars import EnemyCar, Player
from Court.court import Court


# Asks whether a key has been acquired
def userKeyboardInput():
    x = msvcrt.kbhit()
    if x:
        ret = msvcrt.getch()
    else:
        ret = None
    return ret


def createNewEnemy(minSpeed, maxSpeed, court):
    newEnemy = EnemyCar(np.random.randint(2, 15))
    rndXPosNewEnemy = court.generateRandomXPos()
    newEnemy.setPosition((rndXPosNewEnemy, ENEMY_START_Y_POS))
    return newEnemy


COURT_WIDTH = 20
COURT_HEIGHT = 10
PLAYER_Y_POS = COURT_HEIGHT - 2
ENEMY_START_Y_POS = 0 + 2

court = Court(COURT_WIDTH, COURT_HEIGHT)

player = Player()
rndXPosPlayer = court.generateRandomXPos()
player.setPosition((rndXPosPlayer, PLAYER_Y_POS))

enemy1 = createNewEnemy(5, 10, court)
enemy2 = createNewEnemy(5, 10, court)

ENEMIES = [enemy1, enemy2]

time_delta = 1. / 33

while True:
    time.sleep(time_delta)
    # Detect user input
    keyPressed = userKeyboardInput()
    if keyPressed is not None:
        player.controllPlayer(keyPressed)

    for enemy in ENEMIES:
        enemy.moveOneStep()
        if enemy.detectWallCollision(court):
            ENEMIES.remove(enemy)

            player.increaseScore()

            playerScore = player.getScore()

            # Increase speed of the newborn enemies
            if playerScore < 10:
                newEnemy = createNewEnemy(2, 10, court)
            elif 10 < playerScore < 20:
                newEnemy = createNewEnemy(5, 15, court)
            elif 20 < playerScore < 30:
                newEnemy = createNewEnemy(10, 20, court)
            else:
                newEnemy = createNewEnemy(15, 25, court)
            ENEMIES.append(newEnemy)

            # Increase the number of enemies
            if player.getScore() % 10 == 0:
                newEnemy = createNewEnemy(5, 20, court)
                ENEMIES.append(newEnemy)

    # Detect if the player collided with an enemy
    if player.detectCarCollision(ENEMIES):
        print "\nCar Collision!"
        sys.exit(0)

    if player.detectWallCollision(court):
        print "\nWall Collision!"
        sys.exit(0)

    # Draw the players and enemies on the court
    court.putPlayersOnCourt([player])
    court.putEnemiesOnCourt(ENEMIES)
    # Show the court in the console
    court.printCourt()
    print "\nPlayerScore: {0}".format(player.getScore())
