import math
import random
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders - [YYSCOOP.com]")
window_icon = pygame.image.load("img/favicon.ico")
pygame.display.set_icon(window_icon)

game_background = pygame.image.load("img/game_background_800_600.jpg")
mixer.music.load("src/background_music.mp3")    ## Game Background Music
mixer.music.play(-1)

## ---------------- PLAYER
player_image = pygame.image.load("img/player_64.png")
player_xpos = 370    ## Player position on x-axis
player_ypos = 530    ## Player position on y-axis
player_xmove = 0     ## Player position Change in x-axis

## ---------------- MONSTER
monster_image = []
monster_xpos = []                   ## monster position on x-axis
monster_ypos = []                   ## monster position on y-axis
monster_xmove = []                       ## Player position Change in x-axis
monster_ymove = []                      ## Player position Change in y-axis
total_monster = 6

for i in range(total_monster):
    monster_image.append(pygame.image.load("img/spaceship_64.png"))
    monster_xpos.append(random.randint(0,736))    ## monster position on x-axis
    monster_ypos.append(random.randint(0,150))    ## monster position on y-axis
    monster_xmove.append(7)                       ## Player position Change in x-axis
    monster_ymove.append(30)                      ## Player position Change in y-axis

## ---------------- BULLET
bullet_image = pygame.image.load("img/bullet_32.png")
bullet_xpos = 0                          ## bullet position on x-axis
bullet_ypos = 530                       ## bullet position on y-axis
bullet_xmove = 0                       ## bullet position Change in x-axis
bullet_ymove = 30                      ## bullet position Change in y-axis
bullet_state = "before_shoot"         ## there are two state : before_shoot & after_shoot

## ---------------- SCORE
score = 0
score_xpos = 10
score_ypos = 10
score_font = pygame.font.Font("freesansbold.ttf",32)

## ---------------- SCORE
score = 0
game_over_font = pygame.font.Font("freesansbold.ttf",60)


def player_pos(xvalue, yvalue):
    xvalue = int(xvalue)
    yvalue = int(yvalue)
    screen.blit(player_image, (xvalue, yvalue))

def monster_pos(monster_id,xvalue, yvalue):
    xvalue = int(xvalue)
    yvalue = int(yvalue)
    screen.blit(monster_image[monster_id], (xvalue, yvalue))

def bullet_pos(xvalue, yvalue):
    global bullet_state
    bullet_state = "after_shoot"
    xvalue = int(xvalue)
    yvalue = int(yvalue)
    screen.blit(bullet_image, (xvalue + 16, yvalue + 10))

def collision(monster_x,monster_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow((monster_x - bullet_x),2) + math.pow((monster_y - bullet_y),2))
    # print(distance)
    if distance < 27:
        return True
    else:
        return False

def display_score(xvalue,yvalue):
    xvalue = int(xvalue)
    yvalue = int(yvalue)
    score_val = score_font.render("Score : " + str(score),True,(255,255,255))
    screen.blit(score_val, (xvalue, yvalue))

def game_over():
    game_val = game_over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_val, (200, 250))


## ------------------------------- Main Loop of Game------------------------------
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(game_background, (0, 0))

    x = player_xpos
    y = player_ypos

    ## Setting Key Conytrols -----------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_xmove = -10
                # player_xpos -= 20
            if event.key == pygame.K_RIGHT:
                player_xmove = 10
                # player_xpos += 20
            if event.key == pygame.K_SPACE:
                if bullet_state == "before_shoot":
                    # bullet_ymove = 10
                    bullet_xpos = player_xpos
                    bullet_pos(bullet_xpos,bullet_ypos)
                    bullet_sound = mixer.Sound("src/shoot.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_xmove = 0

    ## updating positions of Player
    player_xpos = player_xpos + player_xmove

    # bullet_xpos = player_xpos
    # bullet_ypos -= bullet_ymove
    # monster_ypos += monster_ymove

    ## Creating restiction points for player
    if player_xpos >= 736:
        player_xpos = 736
    if player_xpos <= 0:
        player_xpos = 0

    ## Creating restiction points for Monsters -------------------------------
    for i in range(total_monster):

        if monster_ypos[i] > 490:
            for monster_id in range(total_monster):
                monster_ypos[monster_id]=3000
            game_over()
            break
        if monster_xpos[i] >=736:
            monster_xmove[i] = -7
            monster_ypos[i] += monster_ymove[i]
        if monster_xpos[i] <=0:
            monster_xmove[i] = 7
            monster_ypos[i] += monster_ymove[i]

        ## when monster & player collision
        collision_status = collision(monster_xpos[i], monster_ypos[i], bullet_xpos, bullet_ypos)
        if collision_status == True:
            collision_sound = mixer.Sound("src/collision_sound.wav")
            collision_sound.play()
            bullet_ypos = 530
            bullet_state = "before_shoot"
            score += 1
            # print(score)
            monster_xpos[i] = random.randint(0, 736)  ## monster position on x-axis
            monster_ypos[i] = random.randint(0, 150)  ## monster position on y-axis

        monster_xpos[i] += monster_xmove[i]
        monster_pos(i, monster_xpos[i], monster_ypos[i])

    ## ---------------------------------------------
    if bullet_ypos <= 0:
        bullet_ypos = 530
        bullet_state = "before_shoot"

    if bullet_state == "after_shoot":
        bullet_pos(bullet_xpos, bullet_ypos)
        bullet_ypos -=  bullet_ymove


    player_pos(x, y)
    display_score(score_xpos,score_ypos)

    pygame.display.update()
