import sys, math
import pygame, random
from pygame.locals import *

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'
DIRECTIONS = ['N', 'E', 'S', 'W']

size = 5
rows = HEIGHT // size
columns = WIDTH // size

LIGHT = 0
DARK = 1

def create_grid():
	return [[1 for j in range(rows)] for i in range(columns)]

# LIGHT = 0, DARK = 1
grid = create_grid()

clock = pygame.time.Clock()

# On light square turn right
# On dark square turn left
# On Leave square privios square changes from white to black or black to white

ant = { "i": columns//2, "j": rows//2, "d": SOUTH }

def mod(n, m):
	remain = n % m
	return math.floor(remain if remain >= 0 else remain + m)

while True:
	clock.tick(120)
	screen.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			pygame.quit()
			sys.exit()
	
	for i in range(columns):
		for j in range(rows):
			if grid[i][j] == LIGHT:
				pygame.draw.rect(screen, (255, 255, 255), (i*size, j*size, size, size))
	
	pygame.draw.rect(screen, (100, 100, 100), (ant["i"]*size, ant["j"]*size, size, size))

	current_square = grid[ant["i"]][ant["j"]]
	if current_square == LIGHT:
		grid[ant["i"]][ant["j"]] = DARK
		new_direction_index = mod(DIRECTIONS.index(ant["d"]) + 1, 4)
		new_direction = DIRECTIONS[new_direction_index]
	else:
		grid[ant["i"]][ant["j"]] = LIGHT
		new_direction_index = mod(DIRECTIONS.index(ant["d"]) - 1, 4)
		new_direction = DIRECTIONS[new_direction_index]
	
	if new_direction == NORTH:
		ant["j"] = mod(ant["j"] - 1, rows)
	elif new_direction == EAST:
		ant["i"] = mod(ant["i"] + 1, columns)
	elif new_direction == WEST:
		ant["i"] = mod(ant["i"] - 1, columns)
	elif new_direction == SOUTH:
		ant["j"] = mod(ant["j"] + 1, rows)
	ant["d"] = new_direction

	pygame.display.update()
