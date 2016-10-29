# Windows OS specific:
import msvcrt
import sys
import numpy as np
import time
import threading

class Car(object):

	def __init__(self, startPosition = (0,0), character = '#', direction = 0):
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

	def controllPlayer(self, keyboardInput):
		# Left
		if keyboardInput.decode() == 'a':
			self.changeDirection(0)
			self.move()
		# Right
		elif keyboardInput.decode() == 'd':
			self.changeDirection(1)
			self.move()


	def detectCarCollision(self, enemies):
		for enemy in enemies:
			if enemy.getPosition() == self.getPosition():
				return True
		return False

	def detectWallCollision(self, court):
		return self.getPosition() in court.getCourt()


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
		return self.position in court.getCourt()


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
				elif i == self.height-1:
					court_row.append('-')
				elif k == 0 and i != 0:
					court_row.append('|')
				elif k == self.width-1:
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
	def generateRndPosOnCourt(self, box = None):
		if box is None:
			box = (1, self.width-2, 1, self.height-2)
		xMin, xMax, yMin, yMax = box
		return (np.random.randint(xMin, xMax), np.random.randint(yMin, yMax))



# Asks whether a key has been acquired
def kbfunc():
	x = msvcrt.kbhit()
	if x:
		ret = msvcrt.getch()
	else:
		ret = False
	return ret



court = Court(40, 20)
player = Player()
player.setPosition((20,17))
enemy1 = EnemyCar(10)
enemy1.setPosition((10,5))
enemy2 = EnemyCar(5)
enemy2.setPosition((20,2))

time_delta = 1./33

while True:
	time.sleep(time_delta)

	enemies = [enemy1, enemy2]

	# Detect user input
	keyPressed = kbfunc()
	if keyPressed != False:
		player.controllPlayer(keyPressed)

	for enemy in enemies:
		enemy.moveOneStep()
		if enemy.detectWallCollision(court):
			print "\nEnemy wall collision!"

	# Detect if the player collided with an enemy
	if player.detectCarCollision(enemies):
		print "\nCar Collision!"
		sys.exit(0)

	if player.detectWallCollision(court):
		print "\nWall Collision!"
		sys.exit(0)

	# Draw the players and enemies on the court
	court.putPlayersOnCourt([player])
	court.putEnemiesOnCourt(enemies)
	# Show the court in the console
	court.printCourt()