import pygame
from objects import Player

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")

# variables
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/Images/background.jpg'), (WIDTH, HEIGHT))


def draw(player, mouse_x, mouse_y):
    WIN.blit(BACKGROUND, (0, 0))
    player.update_angle(mouse_x, mouse_y)
    player.draw(WIN)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # update player
        draw(player, mouse_x, mouse_y)


if __name__ == "__main__":
    main()
