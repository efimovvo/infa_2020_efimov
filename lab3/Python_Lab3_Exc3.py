from random import *
import pygame
from pygame.draw import *
import numpy as np

# Function for new drawing elements
def draw_polyline(color, point_set):
	' Function is drawing polyline by points '
	for i in range(len(point_set) - 1):
		line(
			screen,
			color,
			point_set[i],
			point_set[i+1],
			basic_line_width
			)

def orto_vector(vector):
	' Function returns a normal vector '
	return np.array([-vector[1], vector[0]])

def vector_lenght(vector):
	' Function returns length of vector '
	return (vector[0]**2 + vector[1]**2)**0.5

# Functions for objects
def draw_head(color, center, head_size):
	' Function is drawing ellipsoid head '
	ellipse(
		screen,
		color,
		pygame.Rect(
			(
				int(center[0] - head_size * 1.2 // 2),
				center[1] - head_size // 2,
				int(head_size * 1.2),
				head_size
			)
		),
		0
	)

def draw_dress(color, base_point, height):
	' Function is drawng triangle dress/body '
	left_corner = [
		base_point[0] - height // 3,
		base_point[1] + height
		]

	right_corner = [
		base_point[0] + height // 3,
		base_point[1] + height
		]

	polygon(
		screen,
		color,
		[
			base_point,
			left_corner,
			right_corner
		]
		)

def draw_suite(color, base_point, height):
	' Function is drawing ellipsoid suite/body '
	ellipse(
		screen,
		color,
		pygame.Rect(
			(
				int(base_point[0] - height * 0.4 // 2),
				center[1] - height // 2 + 10,
				int(height * 0.4),
				height
			)
		),
		0
	)

def draw_legs(color, base_point, length, type):
	'  Function is drawing two legs in two polylines '
	# Right leg
	point_set = [
		(base_point[0] + length // 8, base_point[1]),
		(base_point[0] + length // 8, base_point[1] + length),
		(base_point[0] + length // 3, base_point[1] + length + length // 30),
		]

	draw_polyline(color, point_set)

	# Left leg
	if type == 'symmetry':
		point_set = [
			(base_point[0] - length // 8, base_point[1]),
			(base_point[0] - length // 8, base_point[1] + length),
			(base_point[0] - length // 3, base_point[1] + length + length // 30),
			]
	else:
		point_set = [
			(base_point[0] - length // 8, base_point[1]),
			(base_point[0] - length // 2, base_point[1] + length),
			(base_point[0] - length // 1.5, base_point[1] + length)
			]

	draw_polyline(color, point_set)

def draw_arms(color, base_point, length, arms):
	' Function is drawing two arms in one polyline '
	if arms['left'] == 'bend':
		point_set = [
			(base_point[0] - length, base_point[1]),
			(base_point[0] - length // 2, base_point[1] + length // 2)
			]
	else:
		point_set = [(base_point[0] - length, base_point[1] + length)]

	point_set += [(base_point[0], base_point[1])]

	if arms['right'] == 'bend':
		point_set += [
			(base_point[0] + length // 2, base_point[1] + length // 2),
			(base_point[0] + length, base_point[1])
			]
	else:
		point_set += [(base_point[0] + length, base_point[1] + length)]

	draw_polyline(color, point_set)

def draw_girl(place_x, height, arms):
	' Function is drawing a girl in chosen place '
	center_of_head = [
		LENGTH // 2 + place_x,
		HEIGHT // 2 - height // 2
		]

	head_size = height // 3

	draw_legs(
		BLACK,
		[center_of_head[0], center_of_head[1] + height],
		height // 2,
		'symmetry'
		)
	draw_arms(
		BLACK,
		[center_of_head[0], center_of_head[1] + height // 4],
		height // 2,
		arms
		)
	draw_dress(PURPLE, center_of_head, height)
	draw_head(SKIN, center_of_head, head_size)

def draw_boy(place_x, height, arms):
	' Function is drawing a boy in chosen place '
	center_of_head = [
		LENGTH // 2 + place_x,
		HEIGHT // 2 - height // 2
		]

	head_size = height // 3

	draw_legs(
		BLACK,
		[center_of_head[0], center_of_head[1] + height],
		height // 2,
		'assymmetry'
		)
	draw_arms(
		BLACK,
		[center_of_head[0], center_of_head[1] + height // 4],
		height // 2,
		arms
		)
	draw_suite(GRAY, center_of_head, height)
	draw_head(SKIN, center_of_head, head_size)

def draw_icecream(
	colors, base_point, fiber_length, icecream_size, 
	fiber_vector, icecream_vector
	):
	' Function is drawng an icecream '
	# Vectors normalizing
	fiber_vector_length = vector_lenght(fiber_vector)
	icecream_vector_length = vector_lenght(icecream_vector)
	if fiber_vector_length > 0:
		fiber_vector = fiber_length * fiber_vector / fiber_vector_length
	if icecream_vector_length > 0:
		icecream_vector = icecream_size * icecream_vector / icecream_vector_length

	# Drawing the fiber
	point_set = [base_point]
	point_set += [(np.array(base_point) + fiber_vector).tolist()]
		
	draw_polyline(BLACK, point_set)

	# Drawing the cone
	point_set = [point_set[1]]
	point_set += (
		np.array([point_set[0]]) +
		icecream_vector +
		orto_vector(icecream_vector) // 2).tolist()
	point_set += (
		np.array([point_set[0]]) +
		icecream_vector -
		orto_vector(icecream_vector) // 2).tolist()

	print(point_set)
	polygon(
		screen,
		colors['cone'],
		point_set
		)


	# Drawing the balls
	rotation_angle = np.arctan(icecream_vector[0] / icecream_vector[1]) * 180 / np.pi

	surface_for_ball = []
	ball = []

	for i in range(len(colors) - 1):
		surface_for_ball += [pygame.Surface(
			(icecream_size // 2, icecream_size // 2.5),
			pygame.SRCALPHA,
			32
			)]
		ball += [ellipse(
			surface_for_ball[i],
			colors['ball_'+str(i+1)],
			pygame.Rect(
				(
					0,
					0,
					icecream_size // 2,
					icecream_size // 2.5
				)
			),
			0
			)]

		surface_for_ball[i] = pygame.transform.rotate(
			surface_for_ball[i],
			rotation_angle
			)

		screen.blit(
			surface_for_ball[i],
			point_set[-1] +
			icecream_vector // 5
			)

		if i == 0:
			point_set += [((np.array(point_set[1]) + np.array(point_set[2])) // 2).tolist()]
		elif i == 1:
			point_set += [
			(
				(np.array(point_set[2]) + np.array(point_set[3])) // 2 +
				icecream_vector // 5
			).tolist()
			]




pygame.init()


# Constants
FPS = 30
LENGTH = 800
HEIGHT = 600

# Color set
BLUE = (170, 238, 255)
GREEN = (55, 200, 113)
SKIN = (244, 227, 215)
PURPLE = (255, 85, 221)
BLACK = (0, 0, 0)
GRAY = (167, 147, 172)
ORANGE = (255, 204, 0)
BROWN = (85, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# It is basic/center point for all picture
center = np.array([LENGTH // 2, HEIGHT // 2])

radius_of_face = 100
basic_line_width = 1

screen = pygame.display.set_mode((LENGTH, HEIGHT))



# Drawing background color (sky)
screen.fill(BLUE)

# Drawing background color (grass)
rect(screen, GREEN, [0, HEIGHT, LENGTH, - HEIGHT // 2], 0)

# Drawing two girls in center
draw_girl(-HEIGHT // 12, HEIGHT // 6, arms={'left' : 'straight', 'right' : 'bend'})
draw_girl(HEIGHT // 12, HEIGHT // 6, arms={'left' : 'bend', 'right' : 'straight'})
draw_boy(-HEIGHT // 4, HEIGHT // 6, arms={'left' : 'straight', 'right' : 'straight'})
draw_boy(HEIGHT // 4, HEIGHT // 6, arms={'left' : 'straight', 'right' : 'straight'})
draw_icecream(
	colors={'cone' : ORANGE,
			'ball_1' : BROWN,
			'ball_2' : WHITE,
			'ball_3' : RED},
	base_point=(center + np.array([0, -HEIGHT // 24])),
	fiber_length=HEIGHT // 6,
	icecream_size=HEIGHT // 10,
	fiber_vector=np.array([0.1, -0.8]),
	icecream_vector=np.array([-0.1, -1])
	)
draw_icecream(
	colors={'cone' : ORANGE,
			'ball_1' : BROWN,
			'ball_2' : WHITE,
			'ball_3' : RED},
	base_point=(center + np.array([HEIGHT // 3, HEIGHT // 25])),
	fiber_length=0,
	icecream_size=HEIGHT // 20,
	fiber_vector=np.array([1, 1]),
	icecream_vector=np.array([0.1, -0.6])
	)
draw_icecream(
	colors={'cone' : RED,
			'ball_1' : RED,
			'ball_2' : RED},
	base_point=(center + np.array([-HEIGHT // 3, HEIGHT // 25])),
	fiber_length=HEIGHT // 10,
	icecream_size=HEIGHT // 15,
	fiber_vector=np.array([-0.1, -1]),
	icecream_vector=np.array([-0.1, -1])
	)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True

pygame.quit()