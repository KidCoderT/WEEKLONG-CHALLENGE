import math, sys
import pyglet
from pyglet.window import key, mouse
import random

window = pyglet.window.Window(width=480, height=800, caption="SPACE INVADERS")

batch = pyglet.graphics.Batch()

class Invaders:
	alien_image = pyglet.image.load("invader.png")

	def __init__(self):
		self.row_count = 6
		self.y = 40
		self.aliens = self.initialize_aliens()
		self.bullets = []
		self.speed = 0.8
		self.move_x = self.speed
		self.move_down = False
		self.time_since_last_bullet = 0
		self.cooldown = 40
	
	def shoot(self):
		if len(self.aliens) > 0:
			random_column = self.aliens[random.randint(0, len(self.aliens)-1)]
			self.bullets.append(
				pyglet.shapes.Rectangle(random_column[-1].x, random_column[-1].y, 2, 10, batch=batch)
			)
	
	def update(self, player):
		if len(self.aliens) > 0:
			for row in self.aliens:
				for alien in row:
					alien.x += self.move_x
					if self.move_down: alien.y -= 10
			
			if self.move_down:
				self.move_down = False
			
			if self.aliens[-1][-1].x + self.aliens[-1][-1].width > window.width:
				self.move_x = -self.speed
				self.move_down = True
			
			elif self.aliens[0][-1].x - self.aliens[0][-1].width < 0:
				self.move_x = self.speed
				self.move_down = True
			
			else:
				self.move_down = False
			
			if self.time_since_last_bullet >= self.cooldown:
				self.shoot()
				self.time_since_last_bullet = random.randint(-5, 20)
			self.time_since_last_bullet += 1
		else:
			self.row_count += 0.5
			self.aliens = self.initialize_aliens()
			self.cooldown -= 5

		for bullet in self.bullets:
			bullet.y -= 10
			if bullet.y < -20: self.bullets.remove(bullet)
			if player.check_collision(bullet.x, bullet.y):
				self.bullets.remove(bullet)
	
	def initialize_aliens(self):
		temp_aliens = []
		x = 48
		for i in range(9):
			new_column = []
			y = window.height - 70
			for j in range(int(self.row_count)):
				new_column.append(self.new_enemy(x, y))
				y -= 50
			temp_aliens.append(new_column)
			x += 45
		
		return temp_aliens
	
	def new_enemy(self, x, y):
		invader = pyglet.sprite.Sprite(img=self.alien_image, x=x, y=y, batch=batch)
		invader.image.anchor_x = invader.width // 2
		invader.image.anchor_y = invader.height // 2
		invader.scale = 0.05
		return invader
	
	def check_collision(self, x, y):
		happend = False
		for row in self.aliens:
			for alien in row:
				if math.dist((x, y), (alien.x, alien.y)) < 20:
					row.remove(alien)
					happend = True
		self.clean_table()
		return happend

	def clean_table(self):
		for row in self.aliens:
			if len(row) == 0:
				self.aliens.remove(row)

class Player:
	shooter_image = pyglet.image.load("shooter.png")
	def __init__(self):
		self.sprite = pyglet.sprite.Sprite(img=self.shooter_image, x=window.width/2, y=30, batch=batch)
		self.sprite.image.anchor_x = self.sprite.width // 2
		self.sprite.image.anchor_y = self.sprite.height // 2
		self.sprite.scale = 0.1
		self.moving_left = False
		self.moving_right = False
		self.bullets = []
		self.should_shoot = False
		self.time_since_last_bullet = 0
		self.health = 3
		self.score = 0
	
	def update(self, invaders: Invaders):
		if self.moving_left: self.sprite.x -= 3
		if self.moving_right: self.sprite.x += 3
		self.constrain()
		if self.should_shoot and self.time_since_last_bullet >= 20:
			self.bullets.append(
				pyglet.shapes.Rectangle(self.sprite.x, self.sprite.y, 4, 8, batch=batch)
			)
			self.time_since_last_bullet = 0
		self.time_since_last_bullet += 1
		
		for bullet in self.bullets:
			bullet.y += 10
			if bullet.y > window.height + 20: self.bullets.remove(bullet)
			elif invaders.check_collision(bullet.x, bullet.y):
				self.bullets.remove(bullet)
				self.score += 10
	
	def constrain(self):
		if self.sprite.x - self.sprite.width <= 0:
			self.sprite.x += 3
		if self.sprite.x + self.sprite.width >= window.width:
			self.sprite.x -= 3
	
	def check_collision(self, x, y):
		happend = False
		if math.dist((x, y), (self.sprite.x, self.sprite.y)) < 20:
			self.health -= 1
			happend = True
		return happend

invaders = Invaders()
player = Player()

def update(dt):
	invaders.update(player)
	player.update(invaders)
	if player.health <= 0:
		sys.exit()
	if invaders.aliens[0][-1].y < 100:
		sys.exit()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		invaders.check_collision(x, y)

@window.event
def on_key_press(symbol, modifier):
	if symbol == key.A or symbol == key.LEFT:
		player.moving_left = True
	if symbol == key.D or symbol == key.RIGHT:
		player.moving_right = True
	if symbol == key.SPACE:
		player.should_shoot = True

@window.event
def on_key_release(symbol, modifier):
	if symbol == key.A or symbol == key.LEFT:
		player.moving_left = False
	if symbol == key.D or symbol == key.RIGHT:
		player.moving_right = False
	if symbol == key.SPACE:
		player.should_shoot = False

score_title_label = pyglet.text.Label("SCORE",
						  font_name = 'monospace',
						  font_size = 18,
						  x = window.width//4, y = (window.height//10)*9.8,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)
lives_title_label = pyglet.text.Label("LIVES",
						  font_name = 'monospace',
						  font_size = 18,
						  x = window.width//4 * 3, y = (window.height//10)*9.8,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

score_value_label = pyglet.text.Label(str(player.score),
						  font_name = 'monospace',
						  font_size = 18, color=(0, 255, 0, 255),
						  x = window.width//4 + 80, y = (window.height//10)*9.8,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)
lives_value_label = pyglet.text.Label(str(player.health),
						  font_name = 'monospace',
						  font_size = 18, color=(0, 255, 0, 255),
						  x = window.width//4 * 3 + 60, y = (window.height//10)*9.8,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

@window.event
def on_draw():
	window.clear()
	batch.draw()
	lives_value_label.text = str(player.health)
	score_value_label.text = str(player.score)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()