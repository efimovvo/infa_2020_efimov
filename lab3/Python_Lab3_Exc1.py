from random import *
import pygame
from pygame.draw import *
import numpy as np


pygame.init()


FPS = 30
screen_length = 400
screen_height = 400

center = (screen_length // 2, screen_height // 2)

radius_of_face = 100
basic_line_width = 1

screen = pygame.display.set_mode((screen_length, screen_height))

# Color set
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (180, 180, 180)


def draw_an_eye (screen, center, radius, radius_of_pupil):
	' Function id drawing a red eye in given center with black pupil '
	circle(screen, red, center, radius, 0)
	circle(screen, black, center, radius + basic_line_width, basic_line_width)
	circle(screen, black, center, radius_of_pupil, 0)

def draw_a_brow (screen, center, vector):
	' Function is drawing a black brow in given brow vector '
	polygon(
		screen,
		black,
		(
			(np.array(center) + 30 * vector - 30 * np.array([- vector[1], vector[0]])).tolist(),
			(np.array(center) - 30 * vector - 30 * np.array([- vector[1], vector[0]])).tolist(),
			(np.array(center) - 30 * vector - 20 * np.array([- vector[1], vector[0]]) ).tolist(),
			(np.array(center) + 30 * vector - 20 * np.array([- vector[1], vector[0]]) ).tolist()
		)
		)


# Drawing background color
screen.fill(grey)

# Drawing circle of smile face and border
circle(screen, yellow, center, radius_of_face, 0)
circle(screen, black, center, radius_of_face + 2 * basic_line_width, 2 * basic_line_width)

# Drawing of eyes
left_eye_center, right_eye_center =  (
	(int(center[0] - 0.45 * radius_of_face), int(center[0] - 0.35 * radius_of_face)),
	(int(center[0] + 0.45 * radius_of_face), int(center[0] - 0.35 * radius_of_face))
	)
left_eye_radius, right_eye_radius = (
	int((1 + random()) * 0.1 * radius_of_face),
	int((1 + random()) * 0.1 * radius_of_face)
	)
left_eye_radius_of_pupil = right_eye_radius_of_pupil = int(0.08 * radius_of_face)

draw_an_eye(screen, left_eye_center, left_eye_radius, left_eye_radius_of_pupil)
draw_an_eye(screen, right_eye_center, right_eye_radius, right_eye_radius_of_pupil)

# Drawing of brows
brow_angle = np.pi / 6
left_brow_vector = np.array([np.cos(brow_angle), np.sin(brow_angle)])
right_brow_vector = np.array([np.cos(- brow_angle), np.sin(- brow_angle)])

draw_a_brow(screen, left_eye_center, left_brow_vector)
draw_a_brow(screen, right_eye_center, right_brow_vector)

# Drawing of mouth
mouth_width = 100
rect(
	screen,
	black,
	(
		int(center[0] - mouth_width * 0.5),
		int(center[1] + radius_of_face * 0.3),
		mouth_width,
		20
	),
	0
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