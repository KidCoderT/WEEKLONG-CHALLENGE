import math, sys
import pyglet, random
from pyglet.window import mouse

window = pyglet.window.Window(width=700, height=700, caption="COOKIE CLICKER!")

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
player = pyglet.graphics.OrderedGroup(1)
ui = pyglet.graphics.OrderedGroup(2)

bg = pyglet.shapes.Rectangle(0, 0, window.width, window.height, (251, 211, 219), batch, background)

score = 0

# circle = pyglet.shapes.Circle(window.width/2, window.height/2, radius, batch=batch)
image = pyglet.image.load("cookie.png")
radius = image.width/2
circle_border = pyglet.shapes.Circle(window.width/2, window.height/2, radius+5, color=(0, 0, 0), batch=batch, group = player)
circle = pyglet.sprite.Sprite(img=image, batch=batch, x=window.width/2 - radius, y=window.height/2 - radius, group = player)

score_label = pyglet.text.Label(str(score),
						  font_name = 'monospace',
						  font_size = 72,
						  color=(0, 0, 0, 255),
						  x = window.width//2, y = (window.height//10) * 2.3, group=ui,
						  anchor_x = 'center', anchor_y = 'center', batch=batch)

def update(dt):
	if circle.scale > 1:
		circle.scale -= 0.02
		circle.x = window.width/2 - radius*circle.scale
		circle.y = window.height/2 - radius*circle.scale
	circle_border.radius = radius*circle.scale + 5

@window.event
def on_mouse_press(x, y, button, modifiers):
	global score
	if button == mouse.LEFT:
		if math.dist((window.width/2, window.height/2), (x, y)) < radius:
			score += 1
			circle.scale = 1.1
			circle_border.radius = radius*circle.scale + 5

@window.event
def on_draw():
	window.clear()
	batch.draw()
	score_label.text = str(score)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()