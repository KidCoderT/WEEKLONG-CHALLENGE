import sys
import random
import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 720, 560
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("minesweeper")

GAMEOVER = -1
PLAYING = 1

w = 40
COLUMNS = SCREEN_WIDTH // w
ROWS = SCREEN_HEIGHT // w

FONT = pygame.font.Font("font/Roboto-Regular.ttf", w - 5)

BOMB_COLORS = [
	((72, 133, 237), (47, 86, 154)), # Dark Blue
	((72, 230, 241), (47, 150, 157)), # Light Blue
	((244, 194, 13), (159, 126, 8)), # Yellow
	((0, 135, 58), (0, 88, 44)), # Green
	((244, 132, 13), (159, 86, 8)), # Orange
	((219, 50, 54), (142, 33, 35)), # Red
	((237, 68, 131), (154, 44, 118)), # Pink
	((132, 72, 242), (118, 47, 157)), # Violet
]

GAMESTATE = PLAYING
WINNER = None

class Cell:
	def __init__(self, i, j):
		self.i, self.j = i, j
		self.rect = pygame.Rect(self.i * w, self.j * w, w, w)

		self.revealed = False
		self.is_bomb = False
		self.bomb_color = None

		self.neighboring_bombs = 0

	def render(self):
		if not self.revealed:
			if self.j % 2 == 0:
				if self.i % 2 != 0:
					pygame.draw.rect(DISPLAY, (170, 215, 81), self.rect)
				else:
					pygame.draw.rect(DISPLAY, (162, 209, 73), self.rect)
			else:
				if self.i % 2 == 0:
					pygame.draw.rect(DISPLAY, (170, 215, 81), self.rect)
				else:
					pygame.draw.rect(DISPLAY, (162, 209, 73), self.rect)
		elif self.is_bomb:
			pygame.draw.rect(DISPLAY, self.bomb_color[0], self.rect)
			pygame.draw.circle(DISPLAY, self.bomb_color[1], self.rect.center, w / 4)
			pygame.draw.rect(DISPLAY, (0, 0, 0), (self.rect.x - 1, self.rect.y - 1, w + 1, w + 1), 2)
		else:
			if self.j % 2 == 0:
				if self.i % 2 != 0:
					pygame.draw.rect(DISPLAY, (229, 194, 159), self.rect)
				else:
					pygame.draw.rect(DISPLAY, (215, 184, 153), self.rect)
			else:
				if self.i % 2 == 0:
					pygame.draw.rect(DISPLAY, (229, 194, 159), self.rect)
				else:
					pygame.draw.rect(DISPLAY, (215, 184, 153), self.rect)
			
			# Number
			if self.neighboring_bombs > 0:
				number_color = (123, 31, 162) # 4 or above
				if self.neighboring_bombs == 1:
					number_color = (25, 118, 210)
				elif self.neighboring_bombs == 2:
					number_color = (56, 142, 60)
				elif self.neighboring_bombs == 3:
					number_color = (211, 47, 47)
				num = FONT.render(str(self.neighboring_bombs), False, number_color)
				DISPLAY.blit(num, (self.i * w + w / 2 - num.get_width() / 2, self.j * w + w / 2 - num.get_height() / 2))
	
	def bombify(self):
		self.is_bomb = True
		self.bomb_color = random.choice(BOMB_COLORS)
	
	def check_bombs(self, grid):
		self.neighboring_bombs = 0
		for ci in range(-1, 2):
			for cj in range(-1, 2):
				if self.i + ci < 0 or self.j + cj < 0: continue
				try:
					if grid[self.i + ci][self.j + cj].is_bomb:
						self.neighboring_bombs += 1
				except: continue
	
	def flood_fill(self, grid):
		self.revealed = True
		if self.neighboring_bombs == 0:
			for ci in range(-1, 2):
				for cj in range(-1, 2):
					if ci == cj == 0: continue
					if self.i + ci < 0 or self.j + cj < 0: continue
					try:
						if grid[self.i + ci][self.j + cj].revealed: continue
						grid[self.i + ci][self.j + cj].flood_fill(grid)
					except: continue

number_of_bombs = int(16 / 100 * (COLUMNS * ROWS))

grid = [[Cell(i, j) for j in range(ROWS)] for i in range(COLUMNS)]

# Create The bombs
for new_bomb in range(number_of_bombs):
	i, j = random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1)
	while grid[i][j].is_bomb:
		i, j = random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1)
	grid[i][j].bombify()

# Get the neighboring bombs count
for row in grid:
	for col in row:
		if not col.is_bomb:
			col.check_bombs(grid)


def end_game():
	global grid, GAMESTATE

	# Show Every Bomb
	for row in grid:
		for col in row:
			if col.is_bomb:
				col.revealed = True
	
	# End Game
	GAMESTATE = GAMEOVER

clock = pygame.time.Clock()

while True:
	DISPLAY.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == K_r:
			# Reset board When pressed
			grid = [[Cell(i, j) for j in range(ROWS)] for i in range(COLUMNS)]
	
	for row in grid:
		for col in row:
			col.render()

	if GAMESTATE == PLAYING:	
		mouseX, mouseY = pygame.mouse.get_pos()
		i, j = mouseX // w, mouseY // w
		x, y = i * w, j * w
		pygame.draw.rect(DISPLAY, (255, 255, 255), (x - 1,y - 1, w + 1, w + 1), 2)
		
		if pygame.mouse.get_pressed()[0]:
			grid[i][j].revealed = True
			if grid[i][j].neighboring_bombs == 0 and not grid[i][j].is_bomb:
				grid[i][j].flood_fill(grid)
			if grid[i][j].is_bomb:
				end_game()
			else:
				# Check if won
				won = True
				for row in grid:
					for col in row:
						if not col.is_bomb and not col.revealed:
							won = False
							break
					if not won: break
				if won:
					GAMESTATE = GAMEOVER
					WINNER = 1
	elif WINNER is None:
		# DO a cross
		pygame.draw.line(DISPLAY, (0, 0, 0), (w / 2, w / 2), (SCREEN_WIDTH - w / 2, SCREEN_HEIGHT - w / 2), 20)
		pygame.draw.line(DISPLAY, (0, 0, 0), (SCREEN_WIDTH - w / 2, w / 2), (w / 2, SCREEN_HEIGHT - w / 2), 20)

		# Show Losing Text
		text = pygame.transform.scale2x(FONT.render("GAMEOVER", False, (0, 0, 0), (255, 255, 255)))
		DISPLAY.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
	else:
		# DO a cross
		pygame.draw.line(DISPLAY, (0, 0, 0), (w / 2, w / 2), (SCREEN_WIDTH - w / 2, SCREEN_HEIGHT - w / 2), 20)
		pygame.draw.line(DISPLAY, (0, 0, 0), (SCREEN_WIDTH - w / 2, w / 2), (w / 2, SCREEN_HEIGHT - w / 2), 20)

		# Show WINNING Text
		text = pygame.transform.scale2x(FONT.render("YOU WIN", False, (0, 0, 0), (255, 255, 255)))
		DISPLAY.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))


	pygame.display.update()
	clock.tick(60)

