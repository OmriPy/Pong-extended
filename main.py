import pygame
import random, os, time

# Initialization:
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
PINK = (255, 0, 200)
CYAN = (0, 255, 255)
GRAY = (128, 128 ,128)

# Visual objects
Paddle_right = pygame.Rect(WIDTH - 2 - 6, HEIGHT / 2 - 35, 6, 70)
Paddle_left = pygame.Rect(2, HEIGHT / 2 - 35, 6, 70)
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)

# Velocities
VELOCITIES = [3, -3]
ball_vel_x, ball_vel_y = random.choice(VELOCITIES), random.choice(VELOCITIES)
paddles_vel = 4

# UI
paddle_right_points, paddle_left_points = 0, 0

# Sound effects
HIT_BALL = pygame.mixer.Sound(os.path.join('Assets', 'HittingBall.mp3'))
LOST = pygame.mixer.Sound(os.path.join('Assets', 'Lost.mp3'))

# Other:
clock = pygame.time.Clock()
FONT = pygame.font.Font("freesansbold.ttf", 32)

# Methods:
def Draw_game(Background: tuple, Ball_color: tuple, Paddles_color: tuple, Text_color: tuple):
    WIN.fill(Background)
    right_player_points = FONT.render(str(paddle_right_points), 1, Text_color)
    left_player_points = FONT.render(str(paddle_left_points), 1, Text_color)
    pygame.draw.line(WIN, BLACK, (WIDTH / 2 - 1, 0), (WIDTH / 2 - 1, HEIGHT), 2)
    WIN.blit(right_player_points, (WIDTH / 2 + 20, HEIGHT / 2 - right_player_points.get_height() / 2))
    WIN.blit(left_player_points, (WIDTH / 2 - left_player_points.get_width() - 20, HEIGHT / 2 - left_player_points.get_height() / 2))
    pygame.draw.rect(WIN, Paddles_color, Paddle_right)
    pygame.draw.rect(WIN, Paddles_color, Paddle_left)
    pygame.draw.ellipse(WIN, Ball_color, ball)
    pygame.display.update()

def Ball_movement():
    global ball_vel_x, ball_vel_y
    ball.x += ball_vel_x
    ball.y += ball_vel_y
    # Intersection with right paddle
    if ball.right >= Paddle_right.left:
        if ball.centery < Paddle_right.bottom and ball.centery > Paddle_right.top: # If the right paddle blocked the ball
            pygame.mixer.Sound.play(HIT_BALL)
            ball_vel_x *= -1
            ball.right = Paddle_right.left
        else:
            pygame.mixer.Sound.play(LOST)
            time.sleep(LOST.get_length())
            New_round("left")
    # Intersection with left paddle
    if ball.left <= Paddle_left.right:
        if ball.centery < Paddle_left.bottom and ball.centery > Paddle_left.top: # If the left paddle blocked the ball
            pygame.mixer.Sound.play(HIT_BALL)
            ball_vel_x *= -1
            ball.left = Paddle_left.right
        else:
            pygame.mixer.Sound.play(LOST)
            time.sleep(LOST.get_length())
            New_round("right")
    # Collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel_y *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_vel_x *= -1

def Paddles_movement():
    global paddle_right_points, paddle_left_points
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]: # Up
        if Paddle_right.top >= 0:
            Paddle_right.y -= paddles_vel
    if keys_pressed[pygame.K_DOWN]: # Down
        if Paddle_right.bottom <= HEIGHT:
            Paddle_right.y += paddles_vel
    if keys_pressed[pygame.K_w]: # W
        if Paddle_left.top >= 0:
            Paddle_left.y -= paddles_vel
    if keys_pressed[pygame.K_s]: # S
        if Paddle_left.bottom <= HEIGHT:
            Paddle_left.y += paddles_vel
    if keys_pressed[pygame.K_c]:
        Main_menu()

def New_round(winner: str):
    global ball_vel_x, paddle_right_points, paddle_left_points
    ball.center = (WIDTH / 2 - ball.width / 2, HEIGHT / 2 - ball.height / 2)
    if winner == "right":
        ball_vel_x = -3
        paddle_right_points += 1
    elif winner == "left":
        ball_vel_x = 3
        paddle_left_points += 1
    else: raise Exception("Please enter \"right\" or \"left\".")

def Main_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                run = False
        WIN.fill(RED)
        pygame.display.update()
        s = pygame.key.get_pressed()
        if s[pygame.K_ESCAPE]:
            run = False

def Game():
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                run = False
        Draw_game(GRAY, WHITE, BLACK, BLACK)
        Ball_movement()
        Paddles_movement()

def main():
    Main_menu()
    pygame.quit()


if __name__ == "__main__":
    main()