import math, sys
import pyglet, random
from pyglet.window import key, mouse

window = pyglet.window.Window(width=800, height=800, caption="CANYON BOMBER!")

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
bullets = pyglet.graphics.OrderedGroup(1)
player = pyglet.graphics.OrderedGroup(2)

bg = pyglet.shapes.Rectangle(0, 0, window.width, window.height, (115,113, 236), batch=batch, group=background)

class Canyon:
	def __init__(self):
		self.canyons = []
		self.column_number = window.width//20

		for i in range(self.column_number):
			column = []
			for j in range(15):
				column.append(pyglet.shapes.Rectangle(i*20, j*20, 20, 20, color=self.get_color(j), batch=batch, group=background))
			self.canyons.append(column)
		print(len(self.canyons))
	
	def get_color(self, index):
		if index < 5: return (255, 255, 0)
		elif index < 10: return (8, 4, 191)
		else: return (255, 100, 100)
	
	def update(self, red_bullets, yellow_bullets, radius):
		red_score = 0
		to_remove = []
		for bullet in red_bullets:
			if self.remove_block(bullet["self"].x, bullet["self"].y, radius):
				bullet["resistance"] -= 1
				red_score += 10
				if bullet["resistance"] == 0:
					to_remove.append(bullet)
		for i in to_remove:
			red_bullets.remove(i)

		yellow_score = 0
		to_remove.clear()
		for bullet in yellow_bullets:
			if self.remove_block(bullet["self"].x, bullet["self"].y, radius):
				bullet["resistance"] -= 1
				yellow_score += 10
				if bullet["resistance"] == 0:
					to_remove.append(bullet)
		for i in to_remove:
			yellow_bullets.remove(i)
		self.update_positions()
		return red_score, yellow_score
	
	def update_positions(self):
		for i in range(self.column_number):
			for j in reversed(range(len(self.canyons[i]))):
				if j == 0:
					if self.canyons[i][j].y > 0:
						self.canyons[i][j].y -= 4
				else:
					if self.canyons[i][j].y > self.canyons[i][j-1].y + 20:
						self.canyons[i][j].y -= 4
	
	def remove_block(self, x, y, max_dist=20):
		yes = False
		for i in range(self.column_number):
			for j in reversed(range(len(self.canyons[i]))):
				if math.dist((x, y), (self.canyons[i][j].x + 10, self.canyons[i][j].y + 10)) < max_dist:
					self.canyons[i].pop(j)
					yes = True
		self.update_positions()
		return yes


class Plane():
	red_bomber = pyglet.image.load("playerone.png")
	yellow_bomber = pyglet.image.load("playertwo.png")

	def __init__(self, direction):
		self.move_x = -3
		self.start_x = window.width + 25
		image = self.yellow_bomber
		if direction == 1:
			self.move_x = 3.2
			self.start_x = -100
			image = self.red_bomber
		y = random.randint(15*20, window.height - 50)
		self.charector = pyglet.sprite.Sprite(image, x=self.start_x, y = y, batch=batch, group=player)
		self.charector.scale = 4
		self.bomb_radius = 5
		self.score = 0
		self.time_till_next_shot = 0
		self.bombs = []
		self.shoot = False
	
	def update(self):
		self.charector.x += self.move_x
		if self.move_x > 0 and self.charector.x > window.width + 200:
			self.charector.x = self.start_x
			self.charector.y = random.randint(15*20, window.height - 50)
		elif self.move_x < 0 and self.charector.x < -200:
			self.charector.x = self.start_x
			self.charector.y = random.randint(15*20, window.height - 50)
		
		if self.shoot:
			if self.time_till_next_shot <= 0:
				self.bombs.append(
					{
						"resistance": 8,
						"self": pyglet.shapes.Circle(self.charector.x + 35, self.charector.y + 20, self.bomb_radius, batch=batch, group=bullets)
					}
				)
				self.time_till_next_shot = 25
			self.time_till_next_shot -= 1
		
		for bomb in self.bombs:
			bomb["self"].y -= 3
			bomb["self"].x += self.move_x
			

canyon = Canyon()
red_guy = Plane(1)
yellow_guy = Plane(-1)

def update(dt):
	r_s, y_s = canyon.update(red_guy.bombs, yellow_guy.bombs, yellow_guy.bomb_radius)
	red_guy.score += r_s
	yellow_guy.score += y_s
	red_guy.update()
	yellow_guy.update()

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.SPACE:
		red_guy.shoot = True
	if symbol == key.L:
		yellow_guy.shoot = True

@window.event
def on_key_release(symbol, modifier):
	if symbol == key.SPACE:
		red_guy.shoot = False
	if symbol == key.L:
		yellow_guy.shoot = False

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		canyon.remove_block(x, y)

red_guy_score_label = pyglet.text.Label(str(red_guy.score),
						  font_name = 'monospace',
						  font_size = 36, color=(255,59,60, 255),
						  x = window.width//4, y = (window.height//10)*9.5,
						  anchor_x = 'center', anchor_y = 'center', batch=batch, group=player)
yellow_guy_score_label = pyglet.text.Label(str(yellow_guy.score),
						  font_name = 'monospace',
						  font_size = 36, color=(194,176,67, 255),
						  x = window.width//4 * 3, y = (window.height//10)*9.5,
						  anchor_x = 'center', anchor_y = 'center', batch=batch, group=player)

@window.event
def on_draw():
	window.clear()
	batch.draw()
	red_guy_score_label.text = str(red_guy.score)
	yellow_guy_score_label.text = str(yellow_guy.score)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
