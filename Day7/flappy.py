import random
import sys
import pygame
from pygame.locals import *

pygame.init()

SCALE_AMOUNT = 1.5
SCREEN_WIDTH, SCREEN_HEIGHT = 288, 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH * SCALE_AMOUNT, SCREEN_HEIGHT * SCALE_AMOUNT))
DISPLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

SPEED = 2

class BG_Elements:
	def __init__(self, img, y=0):
		self.img = pygame.image.load(img).convert()
		self.item_1 = pygame.Rect(0, y, self.img.get_width(), self.img.get_height())
		self.item_2 = pygame.Rect(self.img.get_width(), y, self.img.get_width(), self.img.get_height())
	
	def update(self):
		self.item_1.x -= SPEED
		self.item_2.x -= SPEED

		if self.item_1.x <= -self.img.get_width():
			self.item_1.x = self.img.get_width()
		if self.item_2.x <= -self.img.get_width():
			self.item_2.x = self.img.get_width()

	def render(self):
		DISPLAY.blit(self.img, self.item_1)
		DISPLAY.blit(self.img, self.item_2)
	
	def reset(self):
		self.item_1.x = 0
		self.item_2.x = self.img.get_width()

class Background(BG_Elements):
	def __init__(self):
		super().__init__("assets/background-day.png", 0)

class Base(BG_Elements):
	def __init__(self):
		super().__init__("assets/base.png", SCREEN_HEIGHT - 112)

BIRD_FRAMES = [
	pygame.image.load("assets/yellowbird-downflap.png").convert(),
	pygame.image.load("assets/yellowbird-midflap.png").convert(),
	pygame.image.load("assets/yellowbird-upflap.png").convert()
]

STARTED = False
GRAV = 1 # Gravity
FLAP_FORCE = -12

class Bird(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = BIRD_FRAMES[1]
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 3)
		self.vel_y = 0
		self.current_frame = 1
		self.score = 0
	
	def update(self):
		if STARTED:
			self.vel_y += GRAV
			self.rect.y += self.vel_y

			self.current_frame += 0.2
			if int(self.current_frame) > 2:
				self.current_frame = 0
			self.image = BIRD_FRAMES[int(self.current_frame)]
	
	def reset(self):
		self.rect.centerx = SCREEN_WIDTH / 2 - 50
		self.rect.centery = SCREEN_HEIGHT / 3
		self.current_frame = 0
		self.vel_y = 0
		self.score = 0

	def flap(self):
		self.vel_y = FLAP_FORCE

BOTTOM_PIPE_IMG = pygame.image.load("assets/pipe-green.png")
TOP_PIPE_IMG = pygame.transform.flip(BOTTOM_PIPE_IMG, False, True)

class Pipe(pygame.sprite.Sprite):
	def __init__(self, img, top_left):
		super().__init__()
		self.image = img
		self.rect = self.image.get_rect(topleft = top_left)
	
	def update(self):
		self.rect.x -= SPEED

class TopPipe(Pipe):
	def __init__(self):
		super().__init__(TOP_PIPE_IMG, (SCREEN_WIDTH, random.randint(-300, -100)))

class BottomPipe(Pipe):
	def __init__(self, top_pipe_y):
		super().__init__(BOTTOM_PIPE_IMG, (SCREEN_WIDTH, top_pipe_y + 130))

bird = Bird()

pipes = []
top_pipes_group = pygame.sprite.Group()
bottom_pipes_group = pygame.sprite.Group()

bird_group = pygame.sprite.Group()
bird_group.add(bird)

BG = Background()
BASE = Base()

pipe_creation_wait_time = 80
pipe_wait = 0

font = pygame.font.Font("font/04B_19.TTF", 30)

def reset():
	global BG, BASE, bird, STARTED, pipes, pipe_wait

	BG.reset()
	BASE.reset()
	bird.reset()
	pipes.clear()
	top_pipes_group.empty()
	bottom_pipes_group.empty()
	pipe_wait = 0

	STARTED = False

clock = pygame.time.Clock()
while True:
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				bird.flap()
				if not STARTED:
					STARTED = True
	
	DISPLAY.fill((0, 0, 0))

	BG.update()
	BG.render()

	if STARTED:
		top_pipes_group.draw(DISPLAY)
		top_pipes_group.update()
		bottom_pipes_group.draw(DISPLAY)
		bottom_pipes_group.update()
		for pipe in pipes:
			if pipe[0].rect.topright[0] < -5:
				pipes.remove(pipe)
				top_pipes_group.remove(pipe[0])
				bottom_pipes_group.remove(pipe[1])
			elif pipe[0].rect.centerx == bird.rect.centerx:
				bird.score += 1
			else:
				if pygame.sprite.collide_mask(bird, pipe[0]):
					reset()
				elif pygame.sprite.collide_mask(bird, pipe[0]):
					reset()
		
		if pipe_wait > pipe_creation_wait_time:
			pipe_wait = 0
			top = TopPipe()
			bottom = BottomPipe(top.rect.bottom)
			pipes.append([top, bottom])
			top_pipes_group.add(top)
			bottom_pipes_group.add(bottom)

		pipe_wait += 1

	BASE.update()
	BASE.render()

	bird_group.draw(DISPLAY)
	bird_group.update()

	if bird.rect.centery > SCREEN_HEIGHT - 112:
		reset()
	
	if STARTED:
		if pygame.sprite.groupcollide(bird_group, top_pipes_group, False, False):
			reset()
		elif pygame.sprite.groupcollide(bird_group, bottom_pipes_group, False, False):
			reset()
	
	score_text = font.render(str(bird.score), False, (255, 255, 255))
	x, y = (SCREEN_WIDTH / 2 - score_text.get_width() / 2, SCREEN_HEIGHT - 50)
	mask = pygame.mask.from_surface(score_text)
	outline = mask.outline()
	n = 0
	for point in outline:
		outline[n] = (point[0] + x, point[1] + y)
		n += 1
	pygame.draw.polygon(DISPLAY, (0, 0, 0), outline, 6)
	DISPLAY.blit(score_text, (x, y))
	
	SCREEN.blit(pygame.transform.scale(DISPLAY, (SCREEN_WIDTH * SCALE_AMOUNT, SCREEN_HEIGHT * SCALE_AMOUNT)), (0, 0))
	pygame.display.update()
	clock.tick(60)

