from json import load
import math
import pyglet
import random
from pyglet import window
from pyglet.window import key

window = pyglet.window.Window(width=800, height=800, caption="SPACE RACE")
batch = pyglet.graphics.Batch()

class Ship:
	
	def __init__(self, x, color):
		self.score = 0
		self.radius = 25
		self.charector = pyglet.shapes.Circle(x, 40, self.radius, batch=batch, color=color)
		# self.charector = pyglet.sprite.Sprite(self.IMAGE, x=x, y=40, batch=batch)
		self.move_up = False
		self.move_down = False
	
	def up(self):
		self.charector.y += 2
	
	def down(self):
		self.charector.y -= 2
	
	def update(self):
		if self.scored_point():
			self.score += 1
			self.charector.y = 0
		
		if self.move_up:
			self.up()
		if self.move_down:
			self.down()
	
	def scored_point(self):
		if self.charector.y - self.radius > window.height:
			return True
		return False

class Debris:
	def __init__(self):
		self.radius = 10
		self.charector = pyglet.shapes.Circle(0, 0, self.radius, batch=batch)
		self.reset()
	
	def reset(self):
		self.speed_x = 0
		self.charector.y = random.randint(100, window.height - 25)

		if random.random() > 0.5:
			self.speed_x = -random.randint(1, 10)
			self.charector.x = window.width + 30
		else:
			self.speed_x = random.randint(1, 10)
			self.charector.x = -30
	
	def update(self):
		self.charector.x += self.speed_x
		if self.off_screen():
			self.reset()
	
	def off_screen(self):
		return self.charector.x < -40 or self.charector.x > window.width + 40
	
	def hit_ship(self, ship : Ship):
		if math.dist([ship.charector.x, ship.charector.y], [self.charector.x, self.charector.y]) < self.radius + ship.radius:
			return True
		return False

left_ship = Ship(window.width * 0.33, (233, 117, 144))
right_ship = Ship(window.width * 0.66, (97, 189, 208))

number_of_debris = 25

debris = []
for i in range(number_of_debris):
	debris.append(Debris())

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.W:
		left_ship.move_up = True
	if symbol == key.S:
		left_ship.move_down = True
	
	if symbol == key.UP:
		right_ship.move_up = True
	if symbol == key.DOWN:
		right_ship.move_down = True

@window.event
def on_key_release(symbol, modifier):
	if symbol == key.W:
		left_ship.move_up = False
	if symbol == key.S:
		left_ship.move_down = False
	
	if symbol == key.UP:
		right_ship.move_up = False
	if symbol == key.DOWN:
		right_ship.move_down = False

left_ship_score = pyglet.text.Label(str(left_ship.score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

right_ship_score = pyglet.text.Label(str(right_ship.score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4 * 3, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

def update(dt):
	left_ship.update()
	right_ship.update()

	for rock in debris:
		rock.update()
		if rock.hit_ship(left_ship):
			left_ship.charector.y = 40
		if rock.hit_ship(right_ship):
			right_ship.charector.y = 40
	
	right_ship_score.text = str(right_ship.score)
	left_ship_score.text = str(left_ship.score)

@window.event
def on_draw():
	window.clear()
	batch.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()