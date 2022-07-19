import random
import pygame
from pygame import mixer

pygame.init()

mixer.music.load("Fall_guys_music.mp3")
mixer.music.play()

background = pygame.image.load("background_image.jpg")

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Ball Game")
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 165, 0)
frame_rate = 60

random_number = [-5, -4, 4, 5]

circle_x = 300
circle_y = 300
circle_x_direction = random.choice(random_number)
circle_y_direction = random.choice(random_number)

player_width = 30
player_height = 50
player_x = 300
player_y = 500
player_x_direction = 0
player_y_direction = 0
player_speed = 3

font = pygame.font.Font("freesansbold.ttf", 20)
game_over_font = pygame.font.Font("freesansbold.ttf", 60)
score = 0
previous_score = 0
high_score = 0
timer = pygame.time.Clock()

game_Over = False

speed_boost_available = False
speed_boost_x = -100
speed_boost_y = -100
last_grabbed = 0


def circle_direction_check():
    global circle_y_direction
    global circle_x_direction
    if not game_Over:
        if circle_y_direction == circle_x_direction or circle_y_direction == -circle_x_direction:
            circle_y_direction += 1


def speed_boost_check():
    global speed_boost_available
    global score
    global last_grabbed
    global speed_boost_x
    global speed_boost_y
    global player_speed
    if score - last_grabbed > 10 and not speed_boost_available:
        speed_boost_available = True
        speed_boost_x = random.randint(10, 590)
        speed_boost_y = random.randint(10, 590)


def check_difficulty():
    global score
    global circle_y_direction
    global circle_x_direction
    y_mod = (score // 8)
    x_mod = (score // 10)
    if circle_x_direction > 0:
        circle_x_direction = 4 + x_mod
    elif circle_x_direction < 0:
        circle_x_direction = -4 - x_mod
    if circle_y_direction > 0:
        circle_y_direction = 5 + y_mod
    elif circle_y_direction < 0:
        circle_y_direction = -5 - y_mod



def check_collision(playerx, playery, ballx, bally):
    if abs(playerx-ballx) < 45 and abs(playery-bally) < 55:
        global player_x_direction
        global player_y_direction
        global circle_x_direction
        global circle_y_direction
        player_x_direction = 0
        player_y_direction = 0
        circle_x_direction = 0
        circle_y_direction = 0
        game_over()


def game_over():
    global game_Over
    display_game_over = game_over_font.render("Game Over ", True, red, white)
    screen.blit(display_game_over, (150, 250))
    display_restart = font.render("Press Space to Restart ", True, black, white)
    screen.blit(display_restart, (200, 450))
    game_Over = True


def update_player_position():
    global player_x
    global player_y
    global player_x_direction
    global player_y_direction

    if player_x_direction > 0:
        if player_x < 600 - player_width:
            player_x += player_x_direction * player_speed
    if player_x_direction < 0:
        if player_x > 0:
            player_x += player_x_direction * player_speed
    if player_y_direction > 0:
        if player_y < 600 - player_height:
            player_y += player_y_direction * player_speed
    if player_y_direction < 0:
        if player_y > 0:
            player_y += player_y_direction * player_speed


def update_ball_position():
    global circle_x
    global circle_y
    global circle_x_direction
    global circle_y_direction
    global score

    if circle_x_direction > 0:
        if circle_x < 570:
            circle_x += circle_x_direction
        else:
            circle_x_direction *= -1
            score += 1
    elif circle_x_direction < 0:
        if circle_x > 30:
            circle_x += circle_x_direction
        else:
            circle_x_direction *= -1
            score += 1
    if circle_y_direction > 0:
        if circle_y < 570:
            circle_y += circle_y_direction
        else:
            circle_y_direction *= -1
            score += 1
    elif circle_y_direction < 0:
        if circle_y > 30:
            circle_y += circle_y_direction
        else:
            circle_y_direction *= -1
            score += 1


running = True

while running:
    timer.tick(frame_rate)
    circle_direction_check()
    update_ball_position()
    update_player_position()
    check_difficulty()
    speed_boost_check()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_direction = -1
            if event.key == pygame.K_RIGHT:
                player_x_direction = 1
            if event.key == pygame.K_UP:
                player_y_direction = -1
            if event.key == pygame.K_DOWN:
                player_y_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_direction = 0
            if event.key == pygame.K_RIGHT:
                player_x_direction = 0
            if event.key == pygame.K_UP:
                player_y_direction = 0
            if event.key == pygame.K_DOWN:
                player_y_direction = 0
            if event.key == pygame.K_SPACE and game_Over:
                circle_x = 300
                circle_y = 300
                circle_x_direction = random.choice(random_number)
                circle_y_direction = random.choice(random_number)
                player_x = 300
                player_y = 500
                previous_score = score
                if score > high_score:
                    high_score = score
                last_grabbed = 0
                player_speed = 3
                speed_boost_y = -100
                speed_boost_x = -100
                score = 0
                game_Over = False
                speed_boost_available = False

    screen.blit(background,(0,1))
    ball = pygame.draw.circle(screen, red, (circle_x, circle_y), 30)
    gamer = pygame.draw.rect(screen, orange, [player_x, player_y, player_width, player_height])
    check_collision(gamer.centerx, gamer.centery, ball.centerx, ball.centery)
    display_score = font.render("Score: " + str(score), True, black, white)
    screen.blit(display_score, (265, 10))
    display_High_score = font.render("Highest Score: " + str(high_score), True, black, white)
    screen.blit(display_High_score, (10, 10))
    display_previous_score = font.render("Previous Score: " + str(previous_score), True, black, white)
    screen.blit(display_previous_score, (390, 10))
    if speed_boost_available:
        speed_boost = pygame.draw.rect(screen, blue, [speed_boost_x, speed_boost_y, 20, 20])
        if gamer.colliderect(speed_boost):
            player_speed += 1
            speed_boost_x = -100
            speed_boost_y = -100
            last_grabbed = score
            speed_boost_available = False
    display_speed = font.render("Speed: " + str(player_speed - 2), True, black, white)
    screen.blit(display_speed, (10, 550))
    pygame.display.flip()
    print("x : ",circle_y_direction)
    print("y : ",circle_x_direction)
pygame.quit()
