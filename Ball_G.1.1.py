import random
import pygame
from pygame import mixer

# Initialise the Game
pygame.init()

# Playing the music of the game
mixer.music.load("Freeze-Man-Stage-Iceberg-Area-M.mp3")
mixer.music.play()

# Creating the Image for player, ball, background and boost
snowball_Img = pygame.image.load("snowball.png")

player_Img = pygame.image.load("noot-noot2.png")

background = pygame.image.load("background_icy.png")

speed_boost_Img = pygame.image.load("red fish_70.png")

# Limit the screen to 600 by 600 pixel
screen = pygame.display.set_mode([608, 608])

# Set the name of the game
pygame.display.set_caption("Nootnoot game")

# Adding some color
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# The game will run with 60 fps
frame_rate = 60

# Creating all variable for the snowball
# Starting position
snowball_x = 250
snowball_y = 250

# Taking a random number of direction at the start for x and y, can only be between -5 and -4 or 4 and 5
random_number = [-5, -4, 4, 5]
snowball_x_direction = random.choice(random_number)
snowball_y_direction = random.choice(random_number)

# Creating all the variable for the player
# creating the dimension of the player
player_width = 70
player_height = 70

# Starting position of player
player_x = 300
player_y = 500

# Player direction initialises to be 0, pressing the key will change them to -1 or 1
player_x_direction = 0
player_y_direction = 0

# Declaring that the initial speed of the player is 3
player_speed = 3

# Choosing the font
font = pygame.font.Font("freesansbold.ttf", 20)
game_over_font = pygame.font.Font("freesansbold.ttf", 60)

# Initialise score
score = 0
previous_score = 0
high_score = 0

# Creates the timer
timer = pygame.time.Clock()

game_Over = False

# Initialise position and state of the speed_boost
speed_boost_available = False
speed_boost_x = -100
speed_boost_y = -100
last_grabbed = 0


# Checks when the player took the boost and wait 10 points before creating a new speed boost
def speed_boost_check():
    global speed_boost_available
    global score
    global last_grabbed
    global speed_boost_x
    global speed_boost_y
    global player_speed
    if score - last_grabbed > 10 and not speed_boost_available:
        speed_boost_available = True
        # Speed boost is 70*70, so max it can go is 530; -8 because of the wall, then it can only spawn max to 522
        speed_boost_x = random.randint(10, 520)
        speed_boost_y = random.randint(10, 520)


# Increases the speeed of the snowball every time the snowball did a number of bounce
def check_difficulty():
    global score
    global snowball_y_direction
    global snowball_x_direction
    # It will increase randomly by 1 the direction of x and y dependant of score // =1
    y_mod = (score // random.randint(9, 10))
    x_mod = (score // random.randint(7, 8))
    # If the ball is going towards the right, adding 1 to the x direction every 7 or 8 point
    if snowball_x_direction > 0:
        snowball_x_direction = 4 + x_mod
    # If the snowball is going towards the left
    elif snowball_x_direction < 0:
        snowball_x_direction = -4 - x_mod
    # If the snowball is going down, adding 1 to the y direction every 9 or 10 point
    if snowball_y_direction > 0:
        snowball_y_direction = 5 + y_mod
    # If the snowball is going up
    elif snowball_y_direction < 0:
        snowball_y_direction = -5 - y_mod


# Detects if the player and the snowball intercepted
def check_collision(playerx, playery, ballx, bally):
    if abs(playerx-ballx) < 40 and abs(playery-bally) < 40:
        global player_x_direction
        global player_y_direction
        global snowball_x_direction
        global snowball_y_direction
        player_x_direction = 0
        player_y_direction = 0
        snowball_x_direction = 0
        snowball_y_direction = 0
        game_over()


# Creates the game Over state
def game_over():
    global game_Over
    display_game_over = game_over_font.render("Game Over ", True, red, white)
    screen.blit(display_game_over, (150, 250))
    display_restart = font.render("Press Space to Restart ", True, black, white)
    screen.blit(display_restart, (200, 450))
    game_Over = True


# Update the position of the player
def update_player_position():
    global player_x
    global player_y
    global player_x_direction
    global player_y_direction

    # Player speed is initially 3 but increases with boost
    # If we press right key (when we press right key player_x_direction = 1; so it's >0)
    if player_x_direction > 0:
        # Blocks so that the player doesn't come out of the window on the right
        if player_x < 600 - player_width:
            player_x += player_x_direction * player_speed
    # If we press left key (player_x_direction = -1)
    if player_x_direction < 0:
        # Blocks on the left side so player doesn't go off-screen
        if player_x > -2:
            player_x += player_x_direction * player_speed
    # If we press down key (player_y_direction = 1)
    if player_y_direction > 0:
        if player_y < 600 - player_height:
            player_y += player_y_direction * player_speed
    # If we press up key (player_y_direction = -1)
    if player_y_direction < 0:
        if player_y > 8:
            player_y += player_y_direction * player_speed


# Update the ball position
def update_ball_position():
    global snowball_x
    global snowball_y
    global snowball_x_direction
    global snowball_y_direction
    global score

    # When the snowball is going towards the right
    if snowball_x_direction > 0:
        # has not touches the wall yet (the snowball is 70*70 and the wall is 8 pixel long, so 600-72 = 528)
        if snowball_x < 528:
            snowball_x += snowball_x_direction
        # Touches the wall (change direction by the opposite and add +1 to the score)
        else:
            snowball_x_direction *= -1
            score += 1
    # When the snowball is going towards the left
    elif snowball_x_direction < 0:
        if snowball_x > 8:
            snowball_x += snowball_x_direction
        else:
            snowball_x_direction *= -1
            score += 1
    # When the snowball is going down
    if snowball_y_direction > 0:
        if snowball_y < 528:
            snowball_y += snowball_y_direction
        else:
            snowball_y_direction *= -1
            score += 1
    # When the snowball is going up
    elif snowball_y_direction < 0:
        if snowball_y > 8:
            snowball_y += snowball_y_direction
        else:
            snowball_y_direction *= -1
            score += 1


running = True

# Setting up the Game
while running:
    # Setting up the frame rate
    timer.tick(frame_rate)

    # Adding all the function
    update_ball_position()
    update_player_position()
    check_difficulty()
    speed_boost_check()

    # Setting up the keys of the game
    for event in pygame.event.get():
        # If we press quit, end the game
        if event.type == pygame.QUIT:
            running = False
        # If we press a key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_direction = -1
            if event.key == pygame.K_RIGHT:
                player_x_direction = 1
            if event.key == pygame.K_UP:
                player_y_direction = -1
            if event.key == pygame.K_DOWN:
                player_y_direction = 1
        # If we release a key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_direction = 0
            if event.key == pygame.K_RIGHT:
                player_x_direction = 0
            if event.key == pygame.K_UP:
                player_y_direction = 0
            if event.key == pygame.K_DOWN:
                player_y_direction = 0
            # When game Over, start the game again
            if event.key == pygame.K_SPACE and game_Over:
                snowball_x = 300
                snowball_y = 300
                snowball_x_direction = random.choice(random_number)
                snowball_y_direction = random.choice(random_number)
                player_x = 300
                player_y = 500
                # retain the previous score
                previous_score = score
                # Check if High Score has been beaten
                if score > high_score:
                    high_score = score
                last_grabbed = 0
                player_speed = 3
                # hide the speed boost
                speed_boost_y = -100
                speed_boost_x = -100
                score = 0
                # reset game Over and speed boost
                game_Over = False
                speed_boost_available = False

    # Setting the background
    screen.blit(background, (0, 0))
    # Setting the snowball on the screen
    snowball = screen.blit(snowball_Img, (snowball_x, snowball_y))
    # Setting the player on the screen
    gamer = screen.blit(player_Img, (player_x, player_y))
    # Checks the collision between snowball and player
    check_collision(gamer.centerx, gamer.centery, snowball.centerx, snowball.centery)
    # Display the score
    display_score = font.render("Score: " + str(score), True, black, white)
    screen.blit(display_score, (265, 15))
    # Display the high score
    display_High_score = font.render("Highest Score: " + str(high_score), True, black, white)
    screen.blit(display_High_score, (15, 15))
    # display previous score
    display_previous_score = font.render("Previous Score: " + str(previous_score), True, black, white)
    screen.blit(display_previous_score, (400, 15))

    # check if speed boost is available
    if speed_boost_available:
        speed_boost = screen.blit(speed_boost_Img, (speed_boost_x, speed_boost_y))
        # When player and speed boost collides, add 1 in player speed, hide the speed boost and make it unavailable
        if gamer.colliderect(speed_boost):
            player_speed += 1
            speed_boost_x = -100
            speed_boost_y = -100
            last_grabbed = score
            speed_boost_available = False
    # Display the speed
    display_speed = font.render("Speed: " + str(player_speed - 2), True, black, white)
    screen.blit(display_speed, (15, 572))
    pygame.display.flip()
pygame.quit()
