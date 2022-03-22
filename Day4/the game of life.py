import sys
import pygame, random
from pygame.locals import *

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

grid_size = 10
row_size = HEIGHT // grid_size
column_size = WIDTH // grid_size

def create_grid():
	return [[random.randint(0, 1) for j in range(row_size)] for i in range(column_size)]

def count_neighbors(i, j, gen):
	sum = 0
	for _i in range(-1, 2):
		for _j in range(-1, 2):
			col = (i + _i + column_size) % column_size
			row = (j + _j + row_size) % row_size
			sum += gen[col][row]
	sum -= gen[i][j]
	return sum

def new_generation(old_gen):
	new_generation = create_grid()
	for i in range(column_size):
		for j in range(row_size):
			current_state = old_gen[i][j]
			neighbors = count_neighbors(i, j, old_gen)
			if current_state == 1 and (neighbors == 2 or neighbors == 3):
				new_generation[i][j] = 1
			elif current_state == 0 and neighbors == 3:
				new_generation[i][j] = 1
			else:
				new_generation[i][j] = 0
	return new_generation

# LIVE = 1, DEAD = 0
grid = create_grid()

clock = pygame.time.Clock()

while True:
	clock.tick(30)
	screen.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			pygame.quit()
			sys.exit()
	
	for i in range(column_size):
		for j in range(row_size):
			if grid[i][j] == 1:
				pygame.draw.rect(screen, (0, 255, 255), (i*grid_size, j*grid_size, grid_size, grid_size))
	
	grid = new_generation(grid)

	pygame.display.update()
