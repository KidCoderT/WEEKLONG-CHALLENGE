from math import cos, radians, sin, dist
import pyglet
from pyglet.window import key, mouse

window = pyglet.window.Window(width=800, height=800, caption="BLOCKADE")
batch = pyglet.graphics.Batch()

GRID_SIZE = 10
COL_NUM = window.width // GRID_SIZE
ROW_NUM = window.height // GRID_SIZE

class Snake:
	UP = 8
	DOWN = 2
	RIGHT = 6
	LEFT = 4

	def __init__(self, i, j, DIRECTION):
		self.i, self.j = int(i), int(j)
		self.rect = pyglet.shapes.Rectangle(0, 0, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
		self.direction = DIRECTION
		self.start_data = (i, j, DIRECTION)
		self.score = 0
		self.position_rect()
	
	def position_rect(self):
		self.rect.x, self.rect.y = self.i * GRID_SIZE, self.j * GRID_SIZE
	
	def get_real_pos(self):
		return self.i * GRID_SIZE, self.j * GRID_SIZE
	
	def update(self):
		old_i, old_j = self.i, self.j
		if self.direction == self.UP:
			self.j += 1
		elif self.direction == self.DOWN:
			self.j -= 1
		elif self.direction == self.RIGHT:
			self.i += 1
		elif self.direction == self.LEFT:
			self.i -= 1
		
		self.position_rect()
		return old_i, old_j
	
	def reset(self):
		self.i, self.j, self.direction = self.start_data

snake_1 = Snake(2, 2, Snake.UP)
snake_2 = Snake(COL_NUM - 3, ROW_NUM - 3, Snake.DOWN)

wall = []

def create_walls():
	global wall

	for i in range(COL_NUM):
		wall.append(
			pyglet.shapes.Rectangle(i*GRID_SIZE, 0, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
		)

	for j in range(ROW_NUM):
		wall.append(
			pyglet.shapes.Rectangle(0, j*GRID_SIZE, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
		)

	for i in range(COL_NUM):
		wall.append(
			pyglet.shapes.Rectangle(i*GRID_SIZE, (ROW_NUM-1)*GRID_SIZE, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
		)

	for j in range(ROW_NUM):
		wall.append(
			pyglet.shapes.Rectangle((COL_NUM-1)*GRID_SIZE, j*GRID_SIZE, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
		)

create_walls()

def update(dt):
	i1, j1 = snake_1.update()
	wall.append(
		pyglet.shapes.Rectangle(i1*GRID_SIZE, j1*GRID_SIZE, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
	)

	i2, j2 = snake_2.update()
	wall.append(
		pyglet.shapes.Rectangle(i2*GRID_SIZE, j2*GRID_SIZE, GRID_SIZE, GRID_SIZE, color=(0, 255, 0), batch=batch)
	)

	for brick in wall:
		i, j = brick.x // GRID_SIZE, brick.y // GRID_SIZE
		if i == snake_1.i and j == snake_1.j:
			snake_1.reset()
			snake_2.reset()
			snake_2.score += 1
			wall.clear()
			create_walls()
			return

		elif i == snake_2.i and j == snake_2.j:
			snake_2.reset()
			snake_1.reset()
			snake_1.score += 1
			wall.clear()
			create_walls()
			return

snake_1_score = pyglet.text.Label(str(snake_1.score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4, y = (window.height//10)*1.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

snake_2_score = pyglet.text.Label(str(snake_2.score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4 * 3, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

@window.event
def on_draw():
	window.clear()
	batch.draw()

	snake_1_score.text = str(snake_1.score)
	snake_2_score.text = str(snake_2.score)

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.A and snake_1.direction != Snake.RIGHT:
		snake_1.direction = Snake.LEFT
	elif symbol == key.D and snake_1.direction != Snake.LEFT:
		snake_1.direction = Snake.RIGHT
	elif symbol == key.W and snake_1.direction != Snake.DOWN:
		snake_1.direction = Snake.UP
	elif symbol == key.S and snake_1.direction != Snake.UP:
		snake_1.direction = Snake.DOWN
	
	if symbol == key.LEFT and snake_2.direction != Snake.RIGHT:
		snake_2.direction = Snake.LEFT
	elif symbol == key.RIGHT and snake_2.direction != Snake.LEFT:
		snake_2.direction = Snake.RIGHT
	elif symbol == key.UP and snake_2.direction != Snake.DOWN:
		snake_2.direction = Snake.UP
	elif symbol == key.DOWN and snake_2.direction != Snake.UP:
		snake_2.direction = Snake.DOWN

pyglet.clock.schedule_interval(update, 1/16)
pyglet.app.run()