import pygame
from objects import *

# TODO:
#
# - window icon
# - hit animation
# - add sounds
#

# BUGS:
#
# - alien player collision accuracy
# - player diagonal movement speed
#

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens game")
# pygame.display.set_icon

# variables
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/Images/background.jpg'), (WIDTH, HEIGHT))
DIFFICULTY_SCALING = 0.0002


# bullet movement and termination on hitting screen edge
def handle_bullets(bullets):
    for bullet in bullets:
        # check if bullet is off the screen
        if bullet.rect.x <= 0 or bullet.rect.x >= WIDTH or bullet.rect.y <= 0 or bullet.rect.y >= HEIGHT:
            bullet.kill()

        bullet.move()
        bullet.draw(WIN)


def handle_aliens(aliens, player):
    for alien in aliens:
        alien.move(player)
        alien.update_angle(player)
        alien.draw(WIN)


def handle_lives(player, lives):
    lives.clear()  # empty the list from previous iteration
    x = WIDTH - LIFE_SIZE[0] - 10
    for i in range(player.lives):
        lives.append(Life(x, 10))
        x -= LIFE_SIZE[0] + 5  # add 2 tyo width for space between icons
        lives[i].draw(WIN)  # call draw method of just created icon


def handle_ammo(bullets):
    # create bullets
    ammo = []
    ammo_amount = MAX_BULLETS - len(bullets.sprites())
    x = WIDTH/2 + (AMMO_SIZE[0] * ammo_amount) / 2 + 10
    for i in range(ammo_amount):
        ammo.append(Ammo(x, HEIGHT-AMMO_SIZE[1] - 10))
        x -= AMMO_SIZE[0] + 5
        ammo[i].draw(WIN)


def player_move(player, pressed_keys):
    # adjust player position
    if pressed_keys[pg.K_w] and (player.rect.y - PLAYER_SPEED) >= PLAYER_HEIGHT/2:  # up
        player.y -= PLAYER_SPEED
    if pressed_keys[pg.K_s] and (player.rect.y + PLAYER_SPEED) <= HEIGHT - PLAYER_HEIGHT/2:  # down
        player.y += PLAYER_SPEED
    if pressed_keys[pg.K_a] and (player.rect.x - PLAYER_SPEED) >= PLAYER_WIDTH/2:  # left
        player.x -= PLAYER_SPEED
    if pressed_keys[pg.K_d] and (player.rect.x + PLAYER_SPEED) <= WIDTH - PLAYER_WIDTH/2:  # right
        player.x += PLAYER_SPEED

    # function to update sync rect and player coordinates
    player.update_rect()


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
            if player.lives <= 0:  # end game if player lost all lives
                player.isAlive = False


def draw(player, mouse_x, mouse_y, bullets, aliens, lives, first):

    if first:
        start_screen()

    # display end screen when player dies
    elif not player.isAlive:
        game_over(player)

    # draw game if player.isAlive == True
    else:
        WIN.blit(BACKGROUND, (0, 0))  # draw background
        player.update_angle(mouse_x, mouse_y)  # get latest mouse coordinates
        player.draw(WIN)  # draw player
        handle_aliens(aliens, player)  # move aliens
        handle_bullets(bullets)  # move bullets
        check_collisions(bullets, aliens, player)  # check for all collisions
        handle_ammo(bullets)
        handle_lives(player, lives)
        update_score(player)  # update text
        pygame.display.update()  # update display


# what gets shown after player dies
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
    text3 = font3.render('Press SPACE to play again', True, WHITE)
    text3_x = WIDTH / 2 - text3.get_width() / 2
    text3_y = HEIGHT - text3.get_height() - 30
    WIN.blit(text3, (text3_x, text3_y))
    pygame.display.update()


# shown upon first starting the game
def start_screen():
    WIN.blit(BACKGROUND, (0, 0))  # new background

    # welcome text
    font1 = pygame.font.SysFont('sfnsmono', 40, bold=pygame.font.Font.bold)
    text1 = font1.render('WELCOME TO ALIENS', True, WHITE)
    text1_x = WIDTH / 2 - text1.get_width() / 2
    text1_y = HEIGHT / 2 - text1.get_height() / 2 - WIDTH / 10
    WIN.blit(text1, (text1_x, text1_y))

    # restart instruction
    font2 = pygame.font.SysFont('sfnsmono', 20, bold=pygame.font.Font.bold)
    text2 = font2.render('Press SPACE to START', True, WHITE)
    text2_x = WIDTH / 2 - text2.get_width() / 2
    text2_y = HEIGHT - text2.get_height() - 30
    WIN.blit(text2, (text2_x, text2_y))

    pygame.display.update()


def main(first):

    clock = pygame.time.Clock()
    player = Player(WIDTH / 2, HEIGHT / 2)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    lives = []
    ammo = []
    spawn_timer = 0
    difficulty = 1
    bullet_timer = 0
    run = True

    # game loop
    while run:
        clock.tick(FPS)

        bullet_timer += clock.get_rawtime() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed(3)  # get the state of all mouse buttons
                if mouse[0] and len(bullets.sprites()) < MAX_BULLETS and bullet_timer >= 0.05:  # check if left mouse button
                    # noinspection PyTypeChecker
                    bullet = Bullet(player)
                    bullets.add(bullet)  # create a new bullet
                    bullet_timer = 0  # reset timer

            if event.type == pygame.KEYDOWN:
                # when first and space is pressed start a new game with first = False
                if event.key == pygame.K_SPACE:

                    # space restarts the game
                    if first:  # player is on welcome screen
                        main(False)
                    elif not player.isAlive:  # if player has lost
                        main(False)

        # player movement
        pressed_keys = pygame.key.get_pressed()  # returns a list of all currently pressed keys
        player_move(player, pressed_keys)

        # alien creation
        spawn_timer += clock.get_rawtime() / 1000
        difficulty -= DIFFICULTY_SCALING
        if spawn_timer >= difficulty:
            # noinspection PyTypeChecker
            aliens.add(Alien(WIDTH, HEIGHT, player))  # spawn a new alien
            spawn_timer = 0  # reset timer

        # update mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # update player
        draw(player, mouse_x, mouse_y, bullets, aliens, lives, first)


if __name__ == "__main__":
    main(True)
