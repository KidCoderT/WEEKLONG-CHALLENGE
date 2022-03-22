import pyglet, random

window = pyglet.window.Window(width=700, height=700, caption="BOGO SORT!")

def p5_map(n: int, start1: int, stop1: int, start2: int, stop2: int):
	return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

def is_sorted(data) -> bool:
	"""Determine whether the data is sorted."""
	return all(a <= b for a, b in zip(data, data[1:]))

size = 5 # Size of the array
m = 300 # max range for a value in the array

sorted = False

# the data to sort
l: list[int] = [random.randint(0, m) for _ in range(size - 1)]
l.append(m)

# Each cell width
width = window.width / size

def update(dt):
	global sorted, l

	if sorted: return
	if is_sorted(l):
		sorted = True
	else: random.shuffle(l)

@window.event
def on_draw():
	window.clear()
	# Draw The Values
	for i, n in enumerate(l):
		rect = pyglet.shapes.Rectangle(
			i*width,
			0,
			width,
			p5_map(n, 0, m, 0, window.height),
			color=(255, 255, 255)
		)
		rect.draw()

pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()

# Average Time complexity O((n-1)*n!)
