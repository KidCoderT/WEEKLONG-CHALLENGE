import math, sys
import pyglet, random
from pyglet.window import key, mouse

window = pyglet.window.Window(width=335, height=540, caption="FLAPPY BIRD!")

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
pipes = pyglet.graphics.OrderedGroup(1)
foreground = pyglet.graphics.OrderedGroup(2)
player = pyglet.graphics.OrderedGroup(3)

bg = pyglet.image.load("background.png")
background_1 = pyglet.sprite.Sprite(bg, 0, 0, batch=batch, group=background)
background_2 = pyglet.sprite.Sprite(bg, bg.width, 0, batch=batch, group=background)

base = pyglet.image.load("base.png")
base_1 = pyglet.sprite.Sprite(base, 0, 0, batch=batch, group=foreground)
base_2 = pyglet.sprite.Sprite(base, base.width, 0, batch=batch, group=foreground)

bird_image = pyglet.image.load("yellowbird-midflap.png")
bird_image.anchor_x = bird_image.width // 2
bird_image.anchor_y = bird_image.height // 2

score = 0

class Bird:
	def __init__(self):
		self.charector = \
			pyglet.sprite.Sprite(bird_image, window.width * 0.2, window.height/2, batch=batch, group=player)
		self.y_speed = 0
		self.rotation_vel = 0
		self.alive = True
	
	def update(self):
		self.y_speed -= 0.6
		self.rotation_vel += 1
		self.charector.y += self.y_speed
		self.charector.rotation = min(self.rotation_vel, 90)
	
	def jump(self):
		self.y_speed = 7 * 1.3
		self.rotation_vel = -35
	
	def has_died(self, pipes):
		if self.charector.y < base.height or self.charector.y > self.charector.height + window.height:
			return True
		
		for pipe in pipes:
			if self.charector.x > pipe.top_pipe.x and self.charector.x < pipe.top_pipe.x + pipe.tp.width:
				if self.charector.y >= pipe.top_pipe.y:
					return True
				elif self.charector.y <= pipe.bottom_pipe.y + pipe.bp.height:
					return True


class Pipe:
	tp = pyglet.image.load("down-pipe.png")
	bp = pyglet.image.load("pipe.png")
	
	def __init__(self, i):
		self.extra_x = i
		self.top_pipe = pyglet.sprite.Sprite(self.tp, x = window.width + i, y = random.randint(325, 484), batch=batch, group=pipes)
		self.bottom_pipe = pyglet.sprite.Sprite(self.bp, x = window.width + i, y = self.top_pipe.y - 125 - self.bp.height, batch=batch, group=pipes)
	
	def update(self):
		global score
		self.top_pipe.x -= 3
		self.bottom_pipe.x -= 3

		if self.top_pipe.x <= -100:
			self.top_pipe.x = window.width + 100
			self.bottom_pipe.x = window.width + 100
			self.top_pipe.y = random.randint(325, 484)
			self.bottom_pipe.y = self.top_pipe.y - 125 - self.bp.height
			score += 1
	
	def reset(self):
		self.top_pipe.x = window.width + self.extra_x
		self.bottom_pipe.x = window.width + self.extra_x

		self.top_pipe.y = random.randint(325, 484)
		self.bottom_pipe.y = self.top_pipe.y - 125 - self.bp.height

bird = Bird()
pipes = [Pipe(0), Pipe(335/2), Pipe(335)]
time_created_pipe = 100

def restart_game():
	global bird, pipes, time_created_pipe, score
	bird = Bird()
	for pipe in pipes:
		pipe.reset()
	time_created_pipe = 100
	score = 0

def update_char(dt):
	global time_created_pipe,  pipes

	bird.update()
	for pipe in pipes:
		pipe.update()
	time_created_pipe -= 1

	if bird.has_died(pipes):
		restart_game()

def update_bg(dt):
	background_1.x -= 1.5 * dt
	background_2.x -= 1.5 * dt
	if background_1.x <= -bg.width:
		background_1.x = bg.width
	if background_2.x <= -bg.width:
		background_2.x = bg.width
	
	base_1.x -= 3 * dt
	base_2.x -= 3 * dt
	if base_1.x <= -base.width:
		base_1.x = base.width
	if base_2.x <= -base.width:
		base_2.x = base.width	

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		bird.jump()

score_label = pyglet.text.Label(str(score),
						  font_name = 'monospace',
						  font_size = 36,
						  x = window.width//2, y = (window.height//10)*9.3,
						  anchor_x = 'center', anchor_y = 'center', batch=batch, group=player)

@window.event
def on_draw():
	window.clear()
	batch.draw()
	score_label.text = str(score)

pyglet.clock.schedule_interval(update_char, 1/60)
pyglet.clock.schedule_interval(update_bg, 1/60)
pyglet.app.run()