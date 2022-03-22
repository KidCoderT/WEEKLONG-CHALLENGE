import random
import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

cell_size = 40
cell_number = 20
SCREEN_WIDTH, SCREEN_HEIGHT = cell_number * cell_size, cell_number * cell_size
DISPLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

def shrink(img): return pygame.transform.scale(img, (cell_size, cell_size))	

class Snake:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0, 0)
		self.ate_food = False

		self.head_up = shrink(pygame.image.load('assets/head_up.png').convert_alpha())
		self.head_down = shrink(pygame.image.load('assets/head_down.png').convert_alpha())
		self.head_right = shrink(pygame.image.load('assets/head_right.png').convert_alpha())
		self.head_left = shrink(pygame.image.load('assets/head_left.png').convert_alpha())
		
		self.tail_up = shrink(pygame.image.load('assets/tail_up.png').convert_alpha())
		self.tail_down = shrink(pygame.image.load('assets/tail_down.png').convert_alpha())
		self.tail_right = shrink(pygame.image.load('assets/tail_right.png').convert_alpha())
		self.tail_left = shrink(pygame.image.load('assets/tail_left.png').convert_alpha())

		self.body_vertical = shrink(pygame.image.load('assets/body_vertical.png').convert_alpha())
		self.body_horizontal = shrink(pygame.image.load('assets/body_horizontal.png').convert_alpha())

		self.body_tr = shrink(pygame.image.load('assets/body_tr.png').convert_alpha())
		self.body_tl = shrink(pygame.image.load('assets/body_tl.png').convert_alpha())
		self.body_br = shrink(pygame.image.load('assets/body_br.png').convert_alpha())
		self.body_bl = shrink(pygame.image.load('assets/body_bl.png').convert_alpha())
	
	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0, 0)
		self.ate_food = False
	
	def draw(self):
		for i, segment in enumerate(self.body[1:-1]):
			direction = self.body[i-1] - segment
			x_pos = int(segment.x * cell_size)
			y_pos = int(segment.y * cell_size)
			segment_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			previous_block = self.body[i + 1] - segment
			next_block = self.body[i - 1] - segment
			if previous_block.x == next_block.x:
				DISPLAY.blit(self.body_vertical,segment_rect)
			elif previous_block.y == next_block.y:
				DISPLAY.blit(self.body_horizontal,segment_rect)
			else:
				if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
					DISPLAY.blit(self.body_tl,segment_rect)
				elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
					DISPLAY.blit(self.body_bl,segment_rect)
				elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
					DISPLAY.blit(self.body_tr,segment_rect)
				elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
					DISPLAY.blit(self.body_br,segment_rect)

		self.draw_head()
		self.draw_tail()
	
	def draw_head(self):
		img = self.head_right

		x_pos = int(self.body[0].x * cell_size)
		y_pos = int(self.body[0].y * cell_size)
		segment_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

		if self.direction.x == -1:
			img = self.head_left
		elif self.direction.y == 1:
			img = self.head_down
		elif self.direction.y == -1:
			img = self.head_up
		
		DISPLAY.blit(img, segment_rect.topleft)
	
	def draw_tail(self):
		direction = self.body[-2] - self.body[-1]
		img = self.tail_right

		x_pos = int(self.body[-1].x * cell_size)
		y_pos = int(self.body[-1].y * cell_size)
		segment_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

		if direction.x == 1:
			img = self.tail_left
		elif direction.y == -1:
			img = self.tail_down
		elif direction.y == 1:
			img = self.tail_up
		
		DISPLAY.blit(img, segment_rect.topleft)
	
	def update(self):
		if self.direction != pygame.Vector2(0, 0):
			if self.ate_food:
				body_copy = self.body[:]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
				self.ate_food = False
			else:
				body_copy = self.body[:-1]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]

class Food:
	img = shrink(pygame.image.load('assets/apple.png').convert_alpha())

	def __init__(self):
		self.randomize()

	def draw(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
		DISPLAY.blit(self.img, fruit_rect.topleft)

	def randomize(self):
		self.x = random.randint(0, cell_number - 1)
		self.y = random.randint(0, cell_number - 1)
		self.pos = Vector2(self.x, self.y)

def draw_grass():
	grass_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size, cell_size)
	pygame.draw.rect(DISPLAY, (167, 209, 61), grass_rect)

food = Food()
snake = Snake()

font = pygame.font.Font('font/PoetsenOne-Regular.ttf', cell_size - 2)

while True:
	DISPLAY.fill((175, 215, 70))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT and snake.direction.x != -1:
				snake.direction = Vector2(1, 0)
			if event.key == K_LEFT and snake.direction.x != 1:
				snake.direction = Vector2(-1, 0)
			if event.key == K_UP and snake.direction.y != 1:
				snake.direction = Vector2(0, -1)
			if event.key == K_DOWN and snake.direction.y != -1:
				snake.direction = Vector2(0, 1)
	
	for row in range(cell_number):
		if row % 2 == 0: 
			for col in range(cell_number):
				if col % 2 == 0: draw_grass()
		else:
			for col in range(cell_number):
				if col % 2 != 0: draw_grass()
	
	food.draw()
	snake.update()
	snake.draw()

	# Check if ate food
	if snake.body[0] == food.pos:
		food.randomize()
		snake.ate_food = True

	# Check if went out of border
	if snake.body[0][0] > cell_number - 1 or snake.body[0][1] > cell_number - 1:
		snake.reset()
	elif snake.body[0][0] < 0 or snake.body[0][1] < 0:
		snake.reset()
	
	# Check if head hit body
	for segment in snake.body[1:]:
		if segment == snake.body[0]:
			snake.reset()

	# Draw Score
	score_text = str(len(snake.body) - 3)
	score_surface = font.render(score_text, True, (56, 74, 12))
	score_x = int(cell_size * cell_number - 60)
	score_y = int(cell_size * cell_number - 40)
	score_rect = score_surface.get_rect(center=(score_x, score_y))
	apple_rect = Food.img.get_rect(midright=(score_rect.left, score_rect.centery))
	bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
	                      apple_rect.width + score_rect.width + 6, apple_rect.height)

	pygame.draw.rect(DISPLAY, (167, 209, 61), bg_rect)
	DISPLAY.blit(score_surface, score_rect)
	DISPLAY.blit(Food.img, apple_rect)
	pygame.draw.rect(DISPLAY, (56, 74, 12), bg_rect, 2)

	screen.blit(pygame.transform.scale(DISPLAY, (500, 500)), (0, 0))

	pygame.display.update()
	clock.tick(4)
