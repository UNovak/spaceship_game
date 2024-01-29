import pygame
from objects import Player, Bullet, Alien

# TODO:
#
# - collision detection player - alien
# - fix alien movement
# - score counter
# - end game condition
# - creating multiple enemies
# - window icon
# - restart button
# - hit animation
# - increasing difficulty
# - adjusting speed variables
# - add sounds
# - limit shooting speed and amount of bullets
#

pygame.init()
pygame.font.init()

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
            bullet.kill()

        bullet.move()
        bullet.draw(WIN)


def handle_aliens(aliens):
    for alien in aliens:
        alien.move()
        alien.draw(WIN)


def update_text(player):

    font = pygame.font.SysFont('sfnsmono', 20)
    text = font.render('Score: ' + str(player.score), True, WHITE)
    text_x = WIDTH - text.get_width() - 10
    text_y = HEIGHT - text.get_height() - 10
    WIN.blit(text, (text_x, text_y))


def check_collisions(bullets, aliens, player,):
    if pygame.sprite.groupcollide(bullets, aliens, True, True):  # if bullets and aliens collide remove them
        player.score += 1
    for alien in aliens:
        if pygame.sprite.collide_rect(player, alien):
            aliens.remove(alien)


def draw(player, mouse_x, mouse_y, bullets, aliens):
    WIN.blit(BACKGROUND, (0, 0))
    player.update_angle(mouse_x, mouse_y)
    player.draw(WIN)
    handle_aliens(aliens)
    handle_bullets(bullets)
    check_collisions(bullets, aliens, player)
    update_text(player)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    spawn_timer = 0
    difficulty = 1

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed(3)  # get the state of all mouse buttons
                if mouse[0]:  # check if left mouse button\
                    # noinspection PyTypeChecker
                    bullets.add(Bullet(player))

        # alien creation
        spawn_timer += clock.get_rawtime() / 250
        if spawn_timer >= difficulty:
            # noinspection PyTypeChecker
            aliens.add(Alien(WIDTH, HEIGHT))  # spawn a new alien
            spawn_timer = 0  # reset timer

        # update mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # update player
        draw(player, mouse_x, mouse_y, bullets, aliens)


if __name__ == "__main__":
    main()
