import pygame
from objects import Player, Bullet

# TODO:
# - look into sprites
# - enemies

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")
# pygame.display.set_icon

# variables
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/Images/background.jpg'), (WIDTH, HEIGHT))


def handle_bullets(bullets):
    for bullet in bullets:

        # check if bullet is off the screen
        if bullet.x <= 0 or bullet.x >= WIDTH or bullet.y <= 0 or bullet.y >= HEIGHT:
            bullets.remove(bullet)

        bullet.move()
        print(bullets)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed(3)
                if mouse[0]:
                    bullets.append(Bullet(player))

        # update mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # update player
        draw(player, mouse_x, mouse_y, bullets)


if __name__ == "__main__":
    main()
