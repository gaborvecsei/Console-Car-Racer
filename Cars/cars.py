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


class Car(object):
    def __init__(self, startPosition=(0, 0), character='#', direction=0):
        # Character that represents the car in the court
        self.character = character
        # The direction where it is going (left = 0, right = 1)
        self.direction = direction
        self.position = startPosition

    def changeDirection(self, dir):
        self.direction = dir

    def getDirection(self):
        return self.direction

    def getPosition(self):
        return self.position

    def getCharacter(self):
        return self.character

    def setPosition(self, position):
        self.position = position


class Player(Car):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.score = 0
        self.character = "O"

    def increaseScore(self):
        self.score += 1

    def getScore(self):
        return self.score

    # Changes the position of the Player based on the direction
    def move(self):
        # Left
        if self.getDirection() == 0:
            self.setPosition((self.position[0] - 1, self.position[1]))
        # Right
        elif self.getDirection() == 1:
            self.setPosition((self.position[0] + 1, self.position[1]))

    def controlPlayer(self, keyboardInput):
        # Left
        if keyboardInput == 'a':
            self.changeDirection(0)
            self.move()
        # Right
        elif keyboardInput == 'd':
            self.changeDirection(1)
            self.move()

    def detectCarCollision(self, enemies):
        for enemy in enemies:
            if enemy.getPosition() == self.getPosition():
                return True
        return False

    def detectWallCollision(self, court):
        x, y = self.position
        if x >= court.getWidthHeight()[0] - 1:
            return True
        elif x < 1:
            return True
        elif y >= court.getWidthHeight()[1] - 1:
            return True
        elif y < 1:
            return True
        else:
            return False


class EnemyCar(Car):
    def __init__(self, speed):
        super(self.__class__, self).__init__()
        self.speed = speed
        self.character = "X"
        # We use this to determine the "speed" of the enemy car
        self.timeCount = 0

    # speed: the larger the number the slower the car
    def moveOneStep(self):
        if self.timeCount > self.speed:
            self.setPosition((self.position[0], self.position[1] + 1))
            self.timeCount = 0
        else:
            self.timeCount += 1

    def detectWallCollision(self, court):
        if self.position[0] >= court.getWidthHeight()[0]:
            return True
        elif self.position[1] >= court.getWidthHeight()[1]:
            return True
        else:
            return False
