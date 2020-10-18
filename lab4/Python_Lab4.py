import pygame
from pygame.draw import *
from random import randint, random
import numpy as np

def draw_the_figures(figures):
	''' Function draw the balls from the list
	---
	arguments:
		figures: list of dictionaries - the list of balls
		form: string - ball of square
	'''
	for figure in figures:
		if figure['form'] == 'ball':
			circle(screen, figure['color'],
				(int(figure['x']), int(figure['y'])), int(figure['r']))
		elif figure['form']  == 'square':
			rect(screen, figure['color'],
				(
					int(figure['x']) - int(figure['r']),
					int(figure['y']) - int(figure['r']),
					2*int(figure['r']),
					2*int(figure['r'])
				)
				)

def draw_the_score(score):
	''' Function draw the score in the left top corner
	---
	arguments:
		score: int - current score
	'''
	pg_text = pygame.font.Font(None, 36)
	if background_color == WHITE:
		color = BLACK
	else:
		color = WHITE
	current_score = pg_text.render('Score: ' + str(int(score)), 1, color) # text rendering
	screen.blit(current_score, (10, 20)) # placing text on the screen
	if len(rating) > 0:
		top_score = pg_text.render('Best score: ' + str(int(rating[0][1])), 1, color) # text rendering
		screen.blit(top_score, (screen_size[0] // 2, 20)) # placing text on the screen

def create_figure(form):
	''' Function create the figure parameters
	---
	attributes:
		form: string - ball or square
	return:
		dictionary('x', 'y', 'v_x', 'v_y', 'r', 'color')
			x: float - figure position on x
			y: float - figure position on y
			v_x: float - figure velocity on x
			v_y: float - figure velocity on y
			r: float - figure radius
			color: list(int, int, int) - figure color in RGB
	'''
	global x, y, v_x, v_y, r, color
	# X, Y position of figure center
	position_x = randint(100, screen_size[0] - 100)
	position_y = randint(100, screen_size[1] - 100)
	# Module of X, Y velocitys of figure
	velocity_x_abs = (max_ball_speed *
		(3 + (10 + (100 + 16*(score - 100)**2)**0.5) / (2 * (score - 100))))
	velocity_y_abs = (max_ball_speed *
		(3 + (10 + (100 + 16*(score - 100)**2)**0.5) / (2 * (score - 100))))
	# Choosing randomly positive or negative direction for ball moving
	if random()>0.5:
		velocity_x = velocity_x_abs
	else:
		velocity_x = -velocity_x_abs
	if random()>0.5:
		velocity_y = velocity_y_abs
	else:
		velocity_y = -velocity_y_abs
	figure_radius = randint(max_ball_radius // 2, max_ball_radius)
	figure_color = COLORS[randint(0, 5)]
	return {'x': position_x, 'y': position_y, 'v_x': velocity_x, 'v_y': velocity_y, 'r': figure_radius, 'color': figure_color, 'form': form}

def change_background(color):
	''' Function changing background color from WHITE to BLACK and back
	---
	arguments:
		color: tuple(int, int, int) - current background color in RGB
	return:
		color: tuple(int, int, int) - new background color in RGB
	'''
	if color == WHITE:
		color = BLACK
	else:
		color = WHITE
	screen.fill(color)
	# Re-drawing figures on the new background
	draw_the_figures(figures)
	return color

def click(event):
	''' Click handler
	---
	arguments:
		event: pygame.event - current event
	'''
	global background_color, score

	# Searching for the clicked ball
	for figure in figures:
		distance = ((event.pos[0] - figure['x'])**2 + (event.pos[1] - figure['y'])**2)**0.5
		if (distance <= figure['r']):
			score += 100 // figure['r']
			background_color = change_background(background_color)
			figure['r'] /= 1.5
			figure['v_x'] /= 1.5
			figure['v_y'] /= 1.5
			break
	pygame.display.update()

def move_the_figure(figure):
	''' Function move the figure during time step
	---
	arguments:
		figure: dictionary - current figure
	'''
	global score

	# Current growth of ball sizes and velocities
	if figure['form'] == 'ball':
		figure['r'] *= 1.005
		figure['v_x'] *= 1.005
		figure['v_y'] *= 1.005

	# Moving along X taking into account the screen sizes
	figure['x'] += figure['v_x'] * FPS
	max_x = screen_size[0] - figure['r']
	min_x = figure['r']
	if figure['x'] > max_x:
		figure['x'] = 2*max_x - figure['x']
		figure['v_x'] *= -1
	elif figure['x'] < min_x:
		figure['x'] = 2*min_x - figure['x']
		figure['v_x'] *= -1

	# Moving along Y taking into account the screen sizes
	if figure['form'] == 'square':
		figure['v_y'] += g * FPS
		figure['y'] += figure['v_y'] * FPS
	elif figure['form'] == 'ball':
		figure['y'] += figure['v_y'] * FPS
	max_y = screen_size[1] - figure['r']
	min_y = figure['r']
	if figure['y'] > max_y:
		figure['y'] = 2*max_y - figure['y']
		figure['v_y'] *= -0.75
		figure['v_x'] *= 0.75
		# Decreasing score after interaction with the floor
		score -= figure['r'] / 4
	elif figure['y'] < min_y:
		figure['y'] = 2*min_x - figure['y']
		figure['v_y'] *= -1

	return figure

def write_line(text, position_x, position_y, height, color):
	pg_text = pygame.font.Font(None, height)
	text_line = pg_text.render(text, 1, color) # text rendering
	screen.blit(text_line, (position_x, position_y)) # placing text on the screen

def game_over():
	''' Function shows your score on the screen and write the score in rating '''
	screen.fill(BLACK)
	write_line(user_name + ', your score is ' + str(int(score)), screen_size[0]//10, screen_size[1]//4, 80, WHITE) # write line number
	'''pg_text = pygame.font.Font(None, 100)
				text_score = pg_text.render(, 1, WHITE) # text rendering
				screen.blit(text_score, (screen_size[0]//10, screen_size[1]//4)) # placing text on the screen'''

	for i in range(np.minimum(10, len(rating))):
		if (i+1 == position_in_rating) or (position_in_rating > 10 and i == 9):
			color = RED
		else:
			color = WHITE

		if i < 8 or position_in_rating <= 10:
			write_line(str(i+1), screen_size[0]//6, screen_size[1]//2.5 + i*20, 30, color) # write line number
			write_line(rating[i][0], screen_size[0]//5, screen_size[1]//2.5 + i*20, 30, color) # write line number
			write_line(str(rating[i][1]), screen_size[0]//1.5, screen_size[1]//2.5 + i*20, 30, color) # write line number
		elif i == 8:
			write_line('...', screen_size[0]//6, screen_size[1]//2.5 + i*20, 30, color) # write tree dot line
			write_line('...', screen_size[0]//5, screen_size[1]//2.5 + i*20, 30, color) # write tree dot line
			write_line('...', screen_size[0]//1.5, screen_size[1]//2.5 + i*20, 30, color) # write tree dot line
		else:
			write_line(str(position_in_rating), screen_size[0]//6, screen_size[1]//2.5 + i*20, 30, color) # write line number
			write_line(rating[position_in_rating-1][0], screen_size[0]//5, screen_size[1]//2.5 + i*20, 30, color) # write line number
			write_line(str(rating[position_in_rating-1][1]), screen_size[0]//1.5, screen_size[1]//2.5 + i*20, 30, color) # write line number
		

	pygame.display.update()

def write_score_to_rating():
	''' Function writing sorted list of players in file
	and returns positon of current player
	---
	return
		position_in_rating: int
	'''
	# Reading current rating
	global rating
	
	# Placing current score on it's position and calculating number in rating
	if len(rating) == 0:
		rating.append([user_name, int(score)])
		position_in_rating = 1
	elif score < rating[-1][1]:
		rating.append([user_name, int(score)])
		position_in_rating = len(rating)
	else:
		for i in range(len(rating)):
			if score >= rating[i][1]:
				rating.insert(i, [user_name, int(score)])
				position_in_rating = i+1
				break

	# Preparing text string to re-write the rating
	rating_string = ''
	for line in rating:
		rating_string += ' '.join(str(x) for x in line)
		rating_string += '\n'
	# Rating re-writing
	with open('rating.txt', 'w') as file:
		file.write(rating_string)
	return position_in_rating

user_name = ''

while len(user_name) == 0:
	user_name = input('Type your nickname: ')

pygame.init()

FPS = 20
screen_size = (1000, 600)
screen = pygame.display.set_mode(screen_size)

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Color set for balls
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.display.update()
clock = pygame.time.Clock()
finished = False
quited = False

number_of_balls = 5
number_of_squares = 3
figures = [] # initializing list of figures
max_ball_radius = 50
max_ball_speed = 0.2
g = 0.0002 # gravity acceleration
score = 0 # initial score
rating = [] # initializing rating list

# Reading rating of players
with open('rating.txt') as file:
	for line in file:
		rating += [line.rstrip().split()]

	for i in range(len(rating)):
		rating[i][1] = int(rating[i][1])
	# Rating sort
	rating = sorted(rating, key=lambda line: -line[1])

# Generating ball set
for i in range(number_of_balls):
	figures += [create_figure(form='ball')]
	draw_the_figures([figures[i]])
# Generating square set
for i in range(number_of_squares):
	figures += [create_figure(form='square')]
	draw_the_figures([figures[i + number_of_balls]])

background_color = BLACK

draw_the_score(score)

while not finished:
	clock.tick(FPS)
	screen.fill(background_color)
	for figure in figures:
		move_the_figure(figure)
	draw_the_figures(figures)
	draw_the_score(score)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
			quited = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			click(event)
	for i in range(len(figures)):
		if figures[i]['r'] < max_ball_radius / 5:
			figures[i] = create_figure(figures[i]['form'])
	for figure in figures:
		if figure['r'] > 0.25 * screen_size[1]:
			finished = True

position_in_rating = write_score_to_rating()
game_over()

# Waiting for quite
while not quited:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quited = True

pygame.quit()