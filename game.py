import pygame
from objects import Player, Bullet, Alien

# TODO:
#
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


def update_score(player):
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
            player.isAlive = False


def draw(player, mouse_x, mouse_y, bullets, aliens):

    if not player.isAlive:
        game_over(player)

    else:
        WIN.blit(BACKGROUND, (0, 0))  # draw background
        player.update_angle(mouse_x, mouse_y)  # get latest mouse coordinates
        player.draw(WIN)  # draw player
        handle_aliens(aliens)
        handle_bullets(bullets)
        check_collisions(bullets, aliens, player)
        update_score(player)
        pygame.display.update()


def game_over(player):
    WIN.blit(BACKGROUND, (0, 0))
    font1 = pygame.font.SysFont('sfnsmono', 40)
    text1 = font1.render('GAME OVER!', True, WHITE)
    text1_x = WIDTH / 2 - text1.get_width() / 2
    text1_y = HEIGHT / 2 - text1.get_height() / 2 - WIDTH/10
    WIN.blit(text1, (text1_x, text1_y))

    font2 = pygame.font.SysFont('sfnsmono', 20)
    text2 = font2.render('Your score: ' + str(player.score), True, WHITE)
    text2_x = WIDTH/2 - text2.get_width()/2
    text2_y = text1_y + text2.get_height() + text1.get_height() / 2
    WIN.blit(text2, (text2_x, text2_y))

    font3 = pygame.font.SysFont('sfnsmono', 20, bold=pygame.font.Font.bold)
    text3 = font2.render('Press SPACE to play again', True, WHITE)
    text3_x = WIDTH/2 - text3.get_width()/2
    text3_y = HEIGHT - text3.get_height() - 30
    WIN.blit(text3, (text3_x, text3_y))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    spawn_timer = 0
    difficulty = 1
    run = True

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
