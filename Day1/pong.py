import random
import sys
import pyglet
from pyglet.window import key

window = pyglet.window.Window(624, 475, visible=True)
window.set_caption('PONG')

# Batched rendering
batch = pyglet.graphics.Batch()

class Paddle:
	def __init__(self, x):
		self.height = 80
		self.width = 20
		self.paddle = pyglet.shapes.Rectangle(x, window.width/2, self.width, self.height, batch=batch)
		self.is_up = False
		self.is_down = False
	
	def up(self):
		if self.paddle.y + self.height < window.height: 
			self.paddle.y += 2
	
	def down(self):
		if self.paddle.y > 0: 
			self.paddle.y -= 2
	
	def update(self):
		if self.is_up:
			self.up()
		if self.is_down:
			self.down()

class Ball:
	def __init__(self):
		self.radius = 10
		self.circle = pyglet.shapes.Circle(window.width/2, window.height/2, self.radius, batch=batch)
		self.reset()

	def reset(self):
		self.circle.x, self.circle.y = window.width/2, window.height/2

		self.x_speed = random.randint(4, 8)
		if random.random() > 0.5:
			self.x_speed = -self.x_speed
		
		self.y_speed = random.randint(-3, 3)
	
	def update(self):
		if self.circle.y < self.radius or self.circle.y > window.height - self.radius:
			self.y_speed = -self.y_speed + random.uniform(-0.5, 0.5)
		
		self.circle.x += self.x_speed
		self.circle.y += self.y_speed

	def ai_scored(self):
		return self.circle.x < self.radius

	def player_scored(self):
		return self.circle.x > window.width - self.radius
	
	def has_hit_ai(self, ai : Paddle):
		if self.circle.x + self.radius >= ai.paddle.x and self.circle.x <= ai.paddle.x + ai.width:
			if self.is_same_height(ai):
				self.x_speed = -self.x_speed + random.uniform(-1.5, 1.5)
				self.y_speed += random.uniform(-1.5, 1.5)
	
	def has_hit_player(self, player : Paddle):
		if self.circle.x - self.radius <= player.paddle.x + player.width and self.circle.x > player.paddle.x:
			if self.is_same_height(player):
				self.x_speed = -self.x_speed + random.uniform(-1.5, 1.5)
				self.y_speed += random.uniform(-1.5, 1.5)
	
	def is_same_height(self, paddle : Paddle):
		return self.circle.y >= paddle.paddle.y and self.circle.y <= paddle.paddle.y + paddle.height

player_paddle = Paddle(26)
ai_paddle = Paddle(window.width - 48)
ball = Ball()
center_line = pyglet.shapes.Line(window.width/2, window.height + 5, window.width/2, -5, 3, batch=batch)

def process_ai():
	middle_of_paddle = ai_paddle.paddle.y + ai_paddle.height/2

	if middle_of_paddle > ball.circle.y:
		ai_paddle.is_up = False
		ai_paddle.is_down = True
	else:
		ai_paddle.is_up = True
		ai_paddle.is_down = False

def update(dt):
	player_paddle.update()
	ai_paddle.update()

	process_ai()

	ball.update()

	ball.has_hit_player(player_paddle)
	ball.has_hit_ai(ai_paddle)

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.W or symbol == key.UP:
		player_paddle.is_up = True
	if symbol == key.S or symbol == key.DOWN:
		player_paddle.is_down = True

@window.event
def on_key_release(symbol, modifier):
	if symbol == key.W or symbol == key.UP:
		player_paddle.is_up = False
	if symbol == key.S or symbol == key.DOWN:
		player_paddle.is_down = False

ai_score = 0
player_score = 0

player_score_label = pyglet.text.Label(str(player_score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

ai_score_label = pyglet.text.Label(str(ai_score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//4 * 3, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

@window.event
def on_draw():
	global ai_score, player_score
	window.clear()
	batch.draw()
	if ball.player_scored():
		player_score += 1
		player_score_label.text = str(player_score)
		ball.reset()
	elif ball.ai_scored():
		ai_score += 1
		ai_score_label.text = str(ai_score)
		ball.reset()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()