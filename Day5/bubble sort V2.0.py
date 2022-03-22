import pyglet, random

window = pyglet.window.Window(width=700, height=700, caption="BUBBLE SORT V2.0!")

"""
My Change:
After 1 full iteration through the list you can notice that
the last element placed is the correct element for that place.
After 2nd iteration through the list you can notice that
the second last element placed is the correct element for that place.
And so in both these iteration there really is no need to go further
after a certain point because after that it is already sorted.

this change reduced the computation speed as it doest need to do any further
calculations
"""

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
correct_until = size

def update(dt):
	global sorted, l, current_index, correct_until

	if sorted: return
	if is_sorted(l):
		sorted = True
	else:
		if l[current_index] > l[current_index + 1]:
			temp = l[current_index]
			l[current_index] = l[current_index + 1]
			l[current_index + 1] = temp
		current_index += 1

		if current_index >= size - 1:
			correct_until -= 1
			current_index = 0
		elif current_index == correct_until:
			current_index = 0
			correct_until -= 1

@window.event
def on_draw():
	window.clear()
	# Draw The Values
	for i, n in enumerate(l):
		color = (255, 255, 255)
		if i >= correct_until:
			color = (100, 200, 100)
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
