import pygame
from pygame.locals import *
from pygame.draw import *
from random import randint, random
import numpy as np


class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.orig_image = pygame.image.load('tank.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen_size[0] / 2, screen_size[1])

        self.moving_speed = 10
        self.rotation_speed = 0.1
        self.angle_to_east = 0
        self.life = 100

        self.tank_head = TankHead(self)

        all_sprites.add(self)
        all_sprites.add(self.tank_head)

    def update(self):
        key_list = pygame.key.get_pressed()
        if key_list[pygame.K_UP] and self.rect.y > -self.rect.height / 2:
            self.rect.y -= self.moving_speed
        if key_list[pygame.K_DOWN] and self.rect.y < screen_size[1] - self.rect.height / 2:
            self.rect.y += self.moving_speed
        if key_list[pygame.K_LEFT] and self.rect.x > -self.rect.width / 2:
            self.rect.x -= self.moving_speed
        if key_list[pygame.K_RIGHT] and self.rect.x < screen_size[0] - self.rect.width / 2:
            self.rect.x += self.moving_speed
        if key_list[pygame.K_w]:
            delta_x = int(self.moving_speed * np.cos(self.angle_to_east))
            delta_y = int(self.moving_speed * np.sin(self.angle_to_east))

            self.rect.x += delta_x
            self.rect.x %= screen_size[0]
            self.rect.y += delta_y
            self.rect.y %= screen_size[1]
            self.tank_head.update()

        if key_list[pygame.K_d]:
            self.angle_to_east += self.rotation_speed
            self.image = pygame.transform.rotozoom(self.orig_image, -self.angle_to_east * 180 / np.pi, 1)
            self.rect = self.image.get_rect(center=self.rect.center)
        if key_list[pygame.K_a]:
            self.angle_to_east -= self.rotation_speed
            self.image = pygame.transform.rotozoom(self.orig_image, -self.angle_to_east * 180 / np.pi, 1)
            self.rect = self.image.get_rect(center=self.rect.center)

        for bullet in bullets:
            if pygame.sprite.collide_rect(self, bullet) and bullet.color == BLUE:
                if bullet.type == 'rocket':
                    self.life -= 5
                else:
                    self.life -= 1
                bullet.kill()
                bullets.remove(bullet)


        if self.life <= 0:
            self.kill()
            self.tank_head.kill()

            self.__init__()


class TankHead(pygame.sprite.Sprite):
    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)

        self.orig_image = pygame.image.load('tank_head.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.center = tank.rect.center

        self.angle_to_target = 0

        self.tank = tank

    def update(self):
        self.rect.center = self.tank.rect.center
        vector = (pygame.mouse.get_pos()[0] - self.tank.rect.centerx) + 1j * (
                    pygame.mouse.get_pos()[1] - self.tank.rect.centery)
        self.angle_to_target = np.angle(vector, deg=True)
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle_to_target, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, type, power, color):
        if type == 'bullet':
            bullets.append(Bullet(self, power, 3, color))
        else:
            bullets.append(Rocket(self, power, 3, color))
        all_sprites.add(bullets[-1])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank_head, power, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.center = (tank_head.rect.centerx + 10 * np.cos(tank_head.angle_to_target * np.pi / 180),
                            tank_head.rect.centery + 10 * np.sin(tank_head.angle_to_target * np.pi / 180))

        self.x_speed = power * np.cos(tank_head.angle_to_target * np.pi / 180)
        self.y_speed = power * np.sin(tank_head.angle_to_target * np.pi / 180)

        self.color = color
        self.type = 'bullet'
        self.tank_head = tank_head

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x < 0:
            bullets.remove(self)
            self.kill()


class Tower(TankHead):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load('tank_head.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.center = (randint(50, screen_size[0] - 50), randint(50, screen_size[1] - 50))

        self.angle_to_target = randint(-180, 180)
        self.angle_max_speed = 0.5
        self.life = 10

        all_sprites.add(self)

    def update(self):
        vector = (tanks[0].rect.centerx - self.rect.centerx +
                  1j * (tanks[0].rect.centery - self.rect.centery))
        if (np.abs(self.angle_to_target - np.angle(vector, deg=True)) > 180
                and self.angle_to_target > np.angle(vector, deg=True)
                or np.abs(self.angle_to_target - np.angle(vector, deg=True)) < 180
                and self.angle_to_target < np.angle(vector, deg=True)):
            self.angle_to_target += self.angle_max_speed
        else:
            self.angle_to_target -= self.angle_max_speed
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle_to_target, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

        for bullet in bullets:
            if pygame.sprite.collide_rect(self, bullet) and bullet.color == RED:
                bullet.kill()
                bullets.remove(bullet)
                if bullet.type == 'rocket':
                    self.life -= 5
                else:
                    self.life -= 1

            if self.life <= 0:
                self.__init__()

        if randint(0, 100) > 90:
            self.shoot('bullet', 20, BLUE)


class Rocket(Bullet):
    def __init__(self, tank_head, power, size, color):
        pygame.sprite.Sprite.__init__(self)

        self.orig_image = pygame.image.load('rocket.png').convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotozoom(self.orig_image, -tank_head.angle_to_target, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.center = (tank_head.rect.centerx + 20 * np.cos(tank_head.angle_to_target * np.pi / 180),
                            tank_head.rect.centery + 20 * np.sin(tank_head.angle_to_target * np.pi / 180))

        self.x_speed = power * np.cos(tank_head.angle_to_target * np.pi / 180)
        self.y_speed = power * np.sin(tank_head.angle_to_target * np.pi / 180)

        self.type = 'rocket'
        self.color = color
        self.tank_head = tank_head

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x < 0:
            bullets.remove(self)
            self.kill()


# Game initializing
pygame.init()
clock = pygame.time.Clock()
finished = False

# Screen parameters
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

# Game settings

# Creating variables for game process
background_color = WHITE
number_of_towers = 2

# Generating game objects
bullets = []
tanks = []
towers = []

all_sprites = pygame.sprite.Group()
tanks += [Tank()]
for i in range(number_of_towers):
    towers += [Tower()]

# Draw_the_score(score)

# Main game circle
while not finished:
    clock.tick(FPS)
    screen.fill(background_color)
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tanks[0].tank_head.shoot('bullet', 30, RED)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            tanks[0].tank_head.shoot('rocket', 10, RED)
    pressed_keys = pygame.key.get_pressed()

    all_sprites.update()

    pygame.display.flip()

pygame.quit()