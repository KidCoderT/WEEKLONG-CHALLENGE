import pyglet, random

window = pyglet.window.Window(width=700, height=700, caption="BUBBLE SORT!")

def p5_map(n: int, start1: int, stop1: int, start2: int, stop2: int):
	return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

def is_sorted(data: list) -> bool:
	"""Determine whether the data is sorted."""
	return all(a <= b for a, b in zip(data, data[1:]))

size = 100 # Size of the array
m = 300 # max range for a value in the array

sorted = False

# the data to sort
l: list[int] = [random.randint(1, m) for _ in range(size - 1)]
l.append(m)
random.shuffle(l)

# Each cell width
width = window.width / size

current_index = 0
correct_until = -1

def update(dt):
	global sorted, l, current_index, correct_until

	if sorted: return
	if is_sorted(l):
		sorted = True
	else:
		current_value = l[current_index];
		j = current_index - 1
		while j >= 0 and l[j] > current_value:
			l[j + 1] = l[j]
			j = j - 1
		
		l[j + 1] = current_value
		current_index += 1
		correct_until += 1

		if current_index >= size:
			current_index = 0

@window.event
def on_draw():
	window.clear()
	# Draw The Values
	for i, n in enumerate(l):
		color = (255, 255, 255)
		if i == current_index:
			color = (200, 100, 100)
		
		if sorted:
			color = (255, 255, 255)

		rect = pyglet.shapes.Rectangle(
			i*width,
			0,
			width,
			p5_map(n, 0, m, 0, window.height),
			color=color
		)
		rect.draw()

pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()

# Average Time complexity O(n^2)
