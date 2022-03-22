from math import cos, radians, sin, dist
import pyglet
from pyglet.window import key, mouse
from boundary_pos import pos

window = pyglet.window.Window(width=800, height=800, caption="GRAN TANK")
batch = pyglet.graphics.Batch()

class Player:
	gear_speeds = [2, 3, 4, 6]
	ROTATE_AMOUNT = 3

	def __init__(self):
		self.car = pyglet.shapes.Circle(392, 730, radius=20, batch=batch)
		self.angle = 180
		self.gear_index = 0
		self.speed = 1
		self.turn_amount = 0
	
	def turn(self):
		self.angle += self.turn_amount
	
	def update(self):
		if self.speed < self.gear_speeds[self.gear_index]:
			self.speed += 0.2
		elif self.speed > self.gear_speeds[self.gear_index]:
			self.speed -= 0.2
		
		self.car.rotation = self.angle
		self.turn()
		self.move()
	
	def move(self):
		self.car.x += self.speed * cos(radians(self.angle))
		self.car.y -= self.speed * sin(radians(self.angle))
	
	def increase_gear(self):
		self.gear_index += 1
		if self.gear_index >= len(self.gear_speeds):
			self.gear_index = len(self.gear_speeds)-1
	
	def reduce_gear(self):
		self.gear_index -= 1
		if self.gear_index <= 0:
			self.gear_index = 0

class Boundary:
	def __init__(self, x, y):
		self.shape = pyglet.shapes.Circle(x, y, radius=10, batch=batch)
	
	def __str__(self):
		return f"{self.shape.x}, {self.shape.y}"
	
	def hit_player(self, car : Player):
		if dist([car.car.x, car.car.y], [self.shape.x, self.shape.y]) < 30:
			return True
		return False

car = Player()
boundaries = []

for x, y in pos:
	boundaries.append(Boundary(x, y))

def update(dt):
	car.update()
	for boundary in boundaries:
		if boundary.hit_player(car):
			car.car.x, car.car.y = 392, 730
			car.angle = 180

@window.event
def on_draw():
	window.clear()
	batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		print(x, y)

@window.event
def on_key_release(symbol, modifier):
	if symbol == key.A or symbol == key.LEFT:
		car.turn_amount += car.ROTATE_AMOUNT
	if symbol == key.D or symbol == key.RIGHT:
		car.turn_amount -= car.ROTATE_AMOUNT
	
	if symbol == key.W or symbol == key.UP:
		car.increase_gear()
	if symbol == key.S or symbol == key.DOWN:
		car.reduce_gear()
	
	if symbol == key.ENTER:
		for boundary in boundaries:
			print(boundary)

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.A or symbol == key.LEFT:
		car.turn_amount -= car.ROTATE_AMOUNT
	if symbol == key.D or symbol == key.RIGHT:
		car.turn_amount += car.ROTATE_AMOUNT

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
