import pygame
from objects import Player, Bullet

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")

# variables
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/Images/background.jpg'), (WIDTH, HEIGHT))


def handle_bullets(bullets):
    for bullet in bullets:
        bullet.move()
        bullet.draw(WIN)


def draw(player, mouse_x, mouse_y, bullets):
    WIN.blit(BACKGROUND, (0, 0))
    player.update_angle(mouse_x, mouse_y)
    player.draw(WIN)
    handle_bullets(bullets)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    bullets = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP  or event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed(3)
                if mouse[0]:
                    bullets.append(Bullet(WIDTH / 2, HEIGHT/2, player.angle))

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # update player
        draw(player, mouse_x, mouse_y, bullets)


if __name__ == "__main__":
    main()
