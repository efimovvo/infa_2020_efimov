import pygame
from pygame.draw import *


# Pygame initializing
pygame.init()

# Pygame window creating
screen = pygame.display.set_mode((300, 200))

# Objects drawing


# Screen reloading
pygame.display.update()


FPS = 30
clock = pygame.time.Clock()

finished = False

# Main circle of event catching
while not finished:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True

pygame.quit()