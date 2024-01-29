import pygame
import math
from objects import Player, Bullet, Alien, Live, LIVE_SIZE

# TODO:
#
# - window icon
# - hit animation
# - add sounds
# - limit shooting speed and amount of bullets
#

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")
# pygame.display.set_icon

# variables
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/Images/background.jpg'), (WIDTH, HEIGHT))


# bullet movement and termination on hitting screen edge
def handle_bullets(bullets):
    for bullet in bullets:
        # check if bullet is off the screen
        if bullet.rect.x <= 0 or bullet.rect.x >= WIDTH or bullet.rect.y <= 0 or bullet.rect.y >= HEIGHT:
            bullet.kill()

        bullet.move()
        bullet.draw(WIN)


def handle_aliens(aliens):
    for alien in aliens:
        alien.move()
        alien.draw(WIN)


def handle_lives(player, lives):
    lives.clear()  # empty the list from previous iteration
    x = WIDTH - LIVE_SIZE[0] - 10
    for i in range(player.lives):
        lives.append(Live(x, 10))
        x -= LIVE_SIZE[0] + 2  # add 2 tyo width for space between icons
        lives[i].draw(WIN)  # call draw method of just created icon


# displaying text during live game
def update_score(player):
    font = pygame.font.SysFont('sfnsmono', 20)
    text = font.render('Score: ' + str(player.score), True, WHITE)
    text_x = WIDTH - text.get_width() - 10
    text_y = HEIGHT - text.get_height() - 10
    WIN.blit(text, (text_x, text_y))


def check_collisions(bullets, aliens, player):
    if pygame.sprite.groupcollide(bullets, aliens, True, True):  # if bullets and aliens collide remove them
        player.score += 1  # increment score if player scores a hit
    for alien in aliens:
        # look through all aliens if they are touching the player
        if pygame.sprite.collide_rect(player, alien):
            aliens.remove(alien)  # remove alien if it touches player
            player.lives -= 1  # player loses one life
            if player.lives <= 0:
                player.isAlive = False


def draw(player, mouse_x, mouse_y, bullets, aliens, lives):
    # display end screen when player dies
    if not player.isAlive:
        game_over(player)

    # draw game if player.isAlive == True
    else:
        WIN.blit(BACKGROUND, (0, 0))  # draw background
        player.update_angle(mouse_x, mouse_y)  # get latest mouse coordinates
        player.draw(WIN)  # draw player
        handle_aliens(aliens)  # move aliens
        handle_bullets(bullets)  # move bullets
        check_collisions(bullets, aliens, player)  # check for all collisions
        handle_lives(player, lives)
        update_score(player)  # update text
        pygame.display.update()  # update display


def game_over(player):
    WIN.blit(BACKGROUND, (0, 0))  # new background

    # GAME OVER
    font1 = pygame.font.SysFont('sfnsmono', 40)
    text1 = font1.render('GAME OVER!', True, WHITE)
    text1_x = WIDTH / 2 - text1.get_width() / 2
    text1_y = HEIGHT / 2 - text1.get_height() / 2 - WIDTH / 10
    WIN.blit(text1, (text1_x, text1_y))

    # score: 0
    font2 = pygame.font.SysFont('sfnsmono', 20)
    text2 = font2.render('Your score: ' + str(player.score), True, WHITE)
    text2_x = WIDTH / 2 - text2.get_width() / 2
    text2_y = text1_y + text2.get_height() + text1.get_height() / 2
    WIN.blit(text2, (text2_x, text2_y))

    # restart instruction
    font3 = pygame.font.SysFont('sfnsmono', 20, bold=pygame.font.Font.bold)
    text3 = font2.render('Press SPACE to play again', True, WHITE)
    text3_x = WIDTH / 2 - text3.get_width() / 2
    text3_y = HEIGHT - text3.get_height() - 30
    WIN.blit(text3, (text3_x, text3_y))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    lives = []
    spawn_timer = 0
    difficulty = 1
    max_bullet = 6
    bullet_timer = 0
    run = True

    while run:
        clock.tick(FPS)

        bullet_timer += clock.get_rawtime() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.isAlive:
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed(3)  # get the state of all mouse buttons
                if mouse[0] and len(bullets.sprites()) < max_bullet and bullet_timer >= 0.05:  # check if left mouse button\
                    # noinspection PyTypeChecker
                    bullets.add(Bullet(player))
                    bullet_timer = 0


        # alien creation
        spawn_timer += clock.get_rawtime() / 750
        difficulty -= 0.0001
        if spawn_timer >= difficulty:
            # noinspection PyTypeChecker
            aliens.add(Alien(WIDTH, HEIGHT))  # spawn a new alien
            spawn_timer = 0  # reset timer

        # update mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # update player
        draw(player, mouse_x, mouse_y, bullets, aliens, lives)


if __name__ == "__main__":
    main()
