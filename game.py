import pygame
from objects import Player

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")

def draw(player):
    player.draw(WIN)
    pygame.display.update()

def main():
    run = True
    player = Player(WIDTH / 2, HEIGHT/2)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw(player)

if __name__ == "__main__":
    main()
