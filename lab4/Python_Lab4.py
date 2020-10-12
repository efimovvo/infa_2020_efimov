import pygame
from pygame.draw import *
from random import randint, random

def draw_the_balls(balls):
	for ball in balls:
		circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), int(ball['r']))

def draw_the_score(score):
	f1 = pygame.font.Font(None, 36)
	text_score = f1.render('Score: ' + str(int(score)), 1, DARK_RED)
	screen.blit(text_score, (10, 40))

def create_ball():
	global x, y, v_x, v_y, r, color
	x = randint(100, screen_size[0] - 100)
	y = randint(100, screen_size[1] - 100)
	v_x = 2*max_ball_speed*(random() - 0.5)
	v_y = 2*max_ball_speed*(random() - 0.5)
	r = randint(max_ball_radius // 2, max_ball_radius)
	color = COLORS[randint(0, 5)]
	return {'x': x, 'y': y, 'v_x': v_x, 'v_y': v_y, 'r': r, 'color': color}

def change_background(color):
	if color == WHITE:
		color = BLACK
	else:
		color = WHITE
	screen.fill(color)
	draw_the_balls(balls)
	return color

def click(event):
	global background_color, score

	for ball in balls:
		distance = ((event.pos[0] - ball['x'])**2 + (event.pos[1] - ball['y'])**2)**0.5
		if (distance <= ball['r']):
			score += 100 // ball['r']
			background_color = change_background(background_color)
			ball['r'] /= 1.5
			ball['v_x'] /= 2
			ball['v_y'] /= 2
			break
	pygame.display.update()

def move_the_ball(ball):
	global score
	ball['x'] += ball['v_x'] * time_step
	max_x = screen_size[0] - ball['r']
	min_x = ball['r']
	if ball['x'] > max_x:
		ball['x'] = 2*max_x - ball['x']
		ball['v_x'] *= -1
	elif ball['x'] < min_x:
		ball['x'] = 2*min_x - ball['x']
		ball['v_x'] *= -1

	ball['y'] += ball['v_y'] * time_step
	max_y = screen_size[1] - ball['r']
	min_y = ball['r']
	if ball['y'] > max_y:
		ball['y'] = 2*max_y - ball['y']
		ball['v_y'] *= -1
	elif ball['y'] < min_y:
		ball['y'] = 2*min_x - ball['y']
		ball['v_y'] *= -1
		score -= ball['r'] / 4
	return ball


pygame.init()

FPS = 10
screen_size = (1000, 600)
screen = pygame.display.set_mode(screen_size)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_RED = (100, 0, 0)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.display.update()
clock = pygame.time.Clock()
finished = False

number_of_balls = 5
balls = []
max_ball_radius = 50
max_ball_speed = 3
score = 0

draw_the_score(0)

for i in range(number_of_balls):
	balls += [create_ball()]
	draw_the_balls([balls[i]])
background_color = BLACK
time_step = FPS

while not finished:
	clock.tick(FPS)
	screen.fill(background_color)
	for ball in balls:
		move_the_ball(ball)
	draw_the_balls(balls)
	draw_the_score(score)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			click(event)

	for i in range(len(balls)):
		if balls[i]['r'] < max_ball_radius / 5:
			balls[i] = create_ball()

pygame.quit()