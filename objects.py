import pygame as pg
import math
import random

# player variables
PLAYER_WIDTH = 55
PLAYER_HEIGHT = 55

# alien variables
ALIEN_WIDTH = 30
ALIEN_HEIGHT = 30
ALIEN_SPEED = 1.5

# bullet variables
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
BULLET_SPEED = 5


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.img = pg.transform.scale(pg.image.load('Assets/Images/player_ship.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.angle = 0

    def update_angle(self, mouse_x, mouse_y):
        # Calculate the angle in radians
        angle_rad = math.atan2(mouse_y - self.y, mouse_x - self.x)
        # Convert the angle to degrees and adjust for the Pygame coordinate system
        self.angle = math.degrees(angle_rad) + 90

    def draw(self, window):
        rotated_img = pg.transform.rotate(self.img, -self.angle)  # Rotate the image
        player_rect = rotated_img.get_rect(center=(self.x, self.y))  # create a rectangle around the image
        window.blit(rotated_img, player_rect.topleft)


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.x = player.x
        self.y = player.y
        self.img = pg.transform.scale(pg.image.load('Assets/Images/laser_projectile.png'), (BULLET_WIDTH, BULLET_HEIGHT))
        self.angle = player.angle - 90  # -90 to adjust for the rotation of the player ship
        self.rect = self.img.get_rect(center=(self.x, self.y))  # create a rectangle around the image

    def move(self):
        self.rect.x += math.cos(math.radians(self.angle)) * BULLET_SPEED  # directional vector * bullet speed
        self.rect.y += math.sin(math.radians(self.angle)) * BULLET_SPEED

    def draw(self, window):
        window.blit(self.img, self.rect.topleft)


class Alien(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        # generate random distance
        max_distance = int(math.sqrt(((width/2) ** 2) + ((height/2) ** 2))) + 50
        min_distance = int(math.sqrt(((width/2) ** 2) + ((height/2) ** 2)))
        distance = random.randint(min_distance, max_distance)

        # generate random angle
        angle = math.radians(random.uniform(0, 360))

        # Calculate alien's initial x and y coordinates relative to the center of the screen
        self.x = width/2 + math.cos(angle) * distance
        self.y = height/2 + math.sin(angle) * distance
        self.angle = math.degrees(angle)

        # get image
        self.img = pg.transform.scale(pg.image.load('Assets/Images/enemy_ship.png'), (ALIEN_WIDTH, ALIEN_HEIGHT))
        self.rect = self.img.get_rect(center=(self.x, self.y))  # create a rectangle around the image

    def move(self):
        self.x -= math.cos(math.radians(self.angle)) * ALIEN_SPEED
        self.y -= math.sin(math.radians(self.angle)) * ALIEN_SPEED

    def draw(self, window):
        self.rect = self.img.get_rect(center=(self.x, self.y))
        window.blit(self.img, self.rect.topleft)
