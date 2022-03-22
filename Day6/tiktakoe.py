import random
import pygame
import sys
from pygame.locals import *

pygame.init()

# Press r to replay

SCREEN_WIDTH, SCREEN_HEIGHT = 530, 860
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TikTacToe")

Font = pygame.font.Font("LondrinaSolid-Regular.ttf", 70)
info_font = pygame.font.Font("LondrinaSolid-Regular.ttf", 70)

def transform_image(path):
	return pygame.transform.scale(pygame.image.load(path), (150, 150))

tiles = {
	"blank": {
		"normal": transform_image("blank.png"),
		"on_hover": transform_image("blank-hover.png"),
	},
	"X": {
		"normal": transform_image("X.png"),
		"on_hover": transform_image("X-hover.png"),
	},
	"O": {
		"normal": transform_image("O.png"),
		"on_hover": transform_image("O-hover.png"),
	},
}

class Board:
	def __init__(self):
		self.board = [[None for _ in range(3)] for _ in range(3)]
		self.turn = "X"
		self.state = "PLAYING" # PLAYING | GAMEOVER
		self.winner = None
		self.line_params = None
	
	def check_state(self):
		# Check if Winner
		# Horizontals
		if self.board[0][0] == self.board[0][1] == self.board[0][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[0][0]
			self.line_params = (game_surf, (0, 0, 0), (20 + 75, 20 + 75), (2 * 170 + 20 + 75, 20 + 75), 8)
			return
		if self.board[1][0] == self.board[1][1] == self.board[1][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[1][0]
			self.line_params = (game_surf, (0, 0, 0), (20 + 75, 1 * 170 + 20 + 75), (2 * 170 + 20 + 75, 1 * 170 + 20 + 75), 8)
			return
		if self.board[2][0] == self.board[2][1] == self.board[2][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[2][0]
			self.line_params = (game_surf, (0, 0, 0), (20 + 75, 2 * 170 + 20 + 75), (2 * 170 + 20 + 75, 2 * 170 + 20 + 75), 8)
			return
		# Verticals
		if self.board[0][0] == self.board[1][0] == self.board[2][0] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[0][0]
			self.line_params = (game_surf, (0, 0, 0), (20 + 75, 20 + 75), (20 + 75, 2 * 170 + 20 + 75), 8)
			return
		if self.board[0][1] == self.board[1][1] == self.board[2][1] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[0][1]
			self.line_params = (game_surf, (0, 0, 0), (1 * 170 + 20 + 75, 20 + 75), (1 * 170 + 20 + 75, 2 * 170 + 20 + 75), 8)
			return
		if self.board[0][2] == self.board[1][2] == self.board[2][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[0][2]
			self.line_params = (game_surf, (0, 0, 0), (2 * 170 + 20 + 75, 20 + 75), (2 * 170 + 20 + 75, 2 * 170 + 20 + 75), 8)
			return
		# Diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[0][0]
			self.line_params = (game_surf, (0, 0, 0), (20 + 75, 20 + 75), (2 * 170 + 20 + 75, 2 * 170 + 20 + 75), 8)
			return
		if self.board[2][0] == self.board[1][1] == self.board[0][2] != None:
			self.state = "GAMEOVER"
			self.winner = self.board[2][0]
			self.line_params = (game_surf, (0, 0, 0), (2 * 170 + 20 + 75, 20 + 75), (20 + 75, 2 * 170 + 20 + 75), 8)
			return

		# Check if draw
		is_draw = True
		for row in self.board:
			for col in row:
				if col is None:
					is_draw = False
					break
			if not is_draw:
				break
		if is_draw:
			self.state = "GAMEOVER"
	
	def set_tile(self, i, j, current_player):
		self.board[i][j] = current_player
		
		if self.turn == "X":
			self.turn = "O"
		else:
			self.turn = "X"
		
		self.check_state()

board = Board()

def quit_game():
	pygame.quit()
	sys.exit()


def reset():
	pass

screen_shake = False
screen_shake_start = 0
mouse_pressed = False

game_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
	DISPLAY.fill((255, 255, 255))
	game_surf.fill((255, 255, 255))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			mouse_pressed = True
		else:
			mouse_pressed = False
		if event.type == KEYDOWN:
			if event.key == K_r:
				board.reset()
	
	for y_amount, row in enumerate(board.board):
		for x_amount, col in enumerate(row):
			tile_x, tile_y = x_amount * 170 + 20, y_amount * 170 + 20
			rect = pygame.Rect(tile_x, tile_y, 150, 150)
			pos = pygame.mouse.get_pos()
			offset = (pos[0] - tile_x, pos[1] - tile_y)
			touching = rect.collidepoint(*pos)
			
			if col is None:
				if touching:
					game_surf.blit(tiles["blank"]["normal"], (tile_x, tile_y))
					if mouse_pressed and board.state != "GAMEOVER":
						board.set_tile(y_amount, x_amount, board.turn)
						mouse_pressed = False
				else:
					game_surf.blit(tiles["blank"]["on_hover"], (tile_x, tile_y))
			elif col == 'X':
				if touching:
					game_surf.blit(tiles["X"]["normal"], (tile_x, tile_y))
					if mouse_pressed:
						screen_shake = True
						screen_shake_start = pygame.time.get_ticks()
				else:
					game_surf.blit(tiles["X"]["on_hover"], (tile_x, tile_y))
			else:
				if touching:
					game_surf.blit(tiles["O"]["normal"], (tile_x, tile_y))
					if mouse_pressed:
						screen_shake = True
						screen_shake_start = pygame.time.get_ticks()
						mouse_pressed = False
				else:
					game_surf.blit(tiles["O"]["on_hover"], (tile_x, tile_y))
	
	title = Font.render("TikTakToe", False, (0, 0, 0))
	game_surf.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 3 * 170 + 20))

	if board.state == "PLAYING":
		game_surf.blit(tiles[board.turn]["normal"], (SCREEN_WIDTH / 2 - 75, 550 + title.get_height()))
	elif board.winner is not None:
		game_surf.blit(tiles[board.winner]["normal"], (SCREEN_WIDTH / 2 - 75, 550 + title.get_height()))
		if board.line_params is not None:
			pygame.draw.line(*board.line_params)
		
		text = info_font.render("Winner!", False, (0, 0, 0))
		game_surf.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT - 5 - text.get_height()))

	if screen_shake:
		if pygame.time.get_ticks() - screen_shake_start < 200:
			DISPLAY.blit(game_surf, (random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0)))
		else:
			screen_shake = False
	else:
		DISPLAY.blit(game_surf, (0, 0))

	pygame.display.update()
