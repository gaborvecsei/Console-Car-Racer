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

# Windows OS specific:
import msvcrt
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd

from Cars.cars import EnemyCar, Player
from Court.court import Court

COURT_WIDTH = 20
COURT_HEIGHT = 10
PLAYER_Y_POS = COURT_HEIGHT - 2
ENEMY_START_Y_POS = 0 + 2

SCORES_PATH = "data/scores.csv"


def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def main(playerName, highScore = 0):
    court = Court(COURT_WIDTH, COURT_HEIGHT)

    player = Player()
    rndXPosPlayer = court.generateRandomXPos()
    player.setPosition((rndXPosPlayer, PLAYER_Y_POS))

    enemy1 = createNewEnemy(5, 10, court)
    enemy2 = createNewEnemy(5, 10, court)

    enemies = [enemy1, enemy2]

    time_delta = 1. / 33

    while True:
        time.sleep(time_delta)
        # Detect user input
        keyPressed = userKeyboardInput()
        if keyPressed is not None:
            player.controllPlayer(keyPressed)

        for enemy in enemies:
            enemy.moveOneStep()
            if enemy.detectWallCollision(court):
                enemies.remove(enemy)

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
                enemies.append(newEnemy)

                # Increase the number of enemies
                if player.getScore() % 10 == 0:
                    newEnemy = createNewEnemy(5, 20, court)
                    enemies.append(newEnemy)

        # Detect if the player collided with an enemy
        if player.detectCarCollision(enemies) or player.detectWallCollision(court):
            print "\nCollision!"
            break

        # Draw the players and enemies on the court
        court.putPlayersOnCourt([player])
        court.putEnemiesOnCourt(enemies)
        # Show the court in the console
        court.printCourt()
        print "\nPlayerScore: {0}".format(player.getScore())

    newRow = ','.join([playerName, str(player.getScore()), str(datetime.now())])
    print newRow
    with open(SCORES_PATH, "a") as f:
        f.write("\n" + newRow)

    if player.getScore() > highScore:
        print "You beat the high score!"


def showHighScore():
    scoresTable = pd.read_csv(SCORES_PATH, header=0)

    names = scoresTable["name"].values
    scores = scoresTable["score"].values
    times = scoresTable["time"].values

    if len(names) > 0:

        highScoreRowIndex = np.argmax(scores)

        highScore = scores[highScoreRowIndex]
        highScoreName = names[highScoreRowIndex]
        highScoreTime = times[highScoreRowIndex]

        print "High score reached by {0}:\n\tscore: {1}\n\tdate: {2}".format(highScoreName, highScore, highScoreTime)
        return highScore
    else:
        return 0


if __name__ == '__main__':
    print "Car racer by Gabor Vecsei\n"
    highScore = showHighScore()
    playerName = raw_input("Enter your name: ")
    cleanScreen()
    main(playerName, highScore)