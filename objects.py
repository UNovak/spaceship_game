import pygame as pg
import math

PLAYER_WIDTH = 55
PLAYER_HEIGHT = 55

BULLET_WIDTH = 10
BULLET_HEIGHT = 5
BULLET_SPEED = 5


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.img = pg.transform.scale(pg.image.load('Assets/Images/player_ship.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.angle = 0

    def update_angle(self, mouse_x, mouse_y):
        # Calculate the angle in radians
        angle_rad = math.atan2(mouse_y - self.y, mouse_x - self.x)
        # Convert the angle to degrees and adjust for the Pygame coordinate system
        self.angle = math.degrees(angle_rad) + 90

    def draw(self, window):
        rotated_img = pg.transform.rotate(self.img, -self.angle)  # Rotate the image
        rect = rotated_img.get_rect(center=(self.x, self.y))
        window.blit(rotated_img, rect.topleft)


class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.x = player.x
        self.y = player.y
        self.img = pg.transform.scale(pg.image.load('Assets/Images/laser_projectile.png'), (BULLET_WIDTH, BULLET_HEIGHT))
        self.angle = player.angle

    def move(self):
        self.x += math.cos(math.radians(self.angle - 90)) * BULLET_SPEED
        self.y += math.sin(math.radians(self.angle - 90)) * BULLET_SPEED

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


