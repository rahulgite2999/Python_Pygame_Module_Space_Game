import random
import math
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('space.jpg')

mixer.music.load('bgmusic.wav')
mixer.music.play(-1)

pygame.display.set_caption("HULLYA'S GAME")

icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerimg = pygame.image.load('ss.png')
playerX = 370
playerY = 480
player_change = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 10

for i in range(no_of_enemy):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 140))
    enemyX_change.append(1)
    enemyY_change.append(40)

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

game = pygame.font.Font('freesansbold.ttf', 75)


def show_score(x, y):
    score = font.render("HULLYA'S GAME SCORE - " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    gm = game.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gm, (250, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


run = True

while run:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -4
            if event.key == pygame.K_RIGHT:
                player_change = 4

            if event.key == pygame.K_SPACE:
                mixer.music.load('Gun+Silencer.wav')
                mixer.music.play()

                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    playerX = playerX + player_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(no_of_enemy):
        if enemyY[i] >= 400:
            for j in range(no_of_enemy):
                enemyY[j] = 1000
            game_over()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] = enemyY[i] + enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] = enemyY[i] + enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value = score_value + 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 140)

        enemy(int(enemyX[i]), int(enemyY[i]), i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(int(playerX), int(playerY))

    show_score(textX, textY)

    pygame.display.update()
