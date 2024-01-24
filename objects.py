import pygame as pg

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 33


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pg.transform.scale(pg.image.load('Assets/Images/player_ship.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))

    def draw(self, window):
        window.blit(self.img, ((self.x-(PLAYER_WIDTH/2)), (self.y-(PLAYER_HEIGHT/2))))

