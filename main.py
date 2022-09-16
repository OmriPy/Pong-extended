import pygame
import random, math, sys, os
from multipledispatch import dispatch
from utils import *

# Initialization:
CurDir = os.path.dirname(__file__) # Change this variable's value to pathlib.Path.cwd() when Building
pygame.init()
pygame.font.init()
pygame.display.init()
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
ICON = pygame.image.load(join([CurDir, 'Assets', 'Images', 'icon.png']))
pygame.display.set_icon(ICON)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
PINK = (255, 0, 200)
PURPLE = (132, 52, 250)
CYAN = (0, 255, 255)
GRAY = (128, 128 ,128)
SPECIAL_COLOR = (27, 35, 43)
TRANSPERANT_BLACK = (0, 0, 0, 64)

# Sound effects
HIT_BALL = pygame.mixer.Sound(join([CurDir, 'Assets', 'Sound effects', 'HittingBall.mp3']))
LOST = pygame.mixer.Sound(join([CurDir, 'Assets', 'Sound effects', 'Lost.mp3']))
STARTING_GAME = pygame.mixer.Sound(join([CurDir, 'Assets', 'Sound effects', 'StartOfGame.mp3']))
TRANSITION_SOUND = pygame.mixer.Sound(join([CurDir, 'Assets', 'Sound effects', 'Transition.wav']))

# Images
CLOUD1 = pygame.image.load(join([CurDir, 'Assets', 'Images', 'cloud1.png']))
CLOUD1 = pygame.transform.scale(CLOUD1, (125, 125))
CLOUD2 = pygame.image.load(join([CurDir, 'Assets', 'Images', 'cloud2.png']))
CLOUD3 = pygame.image.load(join([CurDir, 'Assets', 'Images', 'cloud3.png']))
CLOUD4 = pygame.image.load(join([CurDir, 'Assets', 'Images', 'cloud4.png']))
GRASS_IMGAE = pygame.image.load(join([CurDir, 'Assets', 'Images', 'grass.png']))
GRASS_IMGAE = pygame.transform.scale(GRASS_IMGAE, (100, 80))
SUN = pygame.image.load(join([CurDir, 'Assets', 'Images', 'sun.png']))
SUN = pygame.transform.scale(SUN, (175, 175))

# Visual objects
Paddle_right = pygame.Rect(0, HEIGHT / 2 - 35, 6, 70)
Paddle_left = pygame.Rect(2, HEIGHT / 2 - 35, 6, 70)
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)

play_button = pygame.Rect(0, 0, 160, 50)
settings_button = pygame.Rect(0, 0, 160, 50)
exit_button = pygame.Rect(0, 0, 160, 50)

CLOUDS_Y = [(20, 75), (50, 150), (125, 175), (150, 250)]
cloud1 = pygame.Rect(random.randint(0, WIDTH - CLOUD1.get_width()),
                    random.randint(CLOUDS_Y[0][0], CLOUDS_Y[0][1]), CLOUD1.get_width(), CLOUD1.get_height())
cloud2 = pygame.Rect(random.randint(0, WIDTH - CLOUD2.get_width()),
                    random.randint(CLOUDS_Y[1][0], CLOUDS_Y[1][1]), CLOUD2.get_width(), CLOUD2.get_height())
cloud3 = pygame.Rect(random.randint(0, WIDTH - CLOUD3.get_width()),
                    random.randint(CLOUDS_Y[2][0], CLOUDS_Y[2][1]), CLOUD3.get_width(), CLOUD3.get_height())
cloud4 = pygame.Rect(random.randint(0, WIDTH - CLOUD4.get_width()),
                    random.randint(CLOUDS_Y[3][0], CLOUDS_Y[3][1]), CLOUD4.get_width(), CLOUD4.get_height())

buttons_area = pygame.Surface((275, 275), pygame.SRCALPHA)
buttons_area_rect = pygame.Rect(0, 0, buttons_area.get_width(), buttons_area.get_height())

gameOver = pygame.Surface((300, 300), pygame.SRCALPHA)
gameOver_rect = pygame.Rect(0, 0, gameOver.get_width(), gameOver.get_height())

gamePaused = pygame.Surface((300, 100), pygame.SRCALPHA)
gamePaused_rect = pygame.Rect(0, 0, gamePaused.get_width(), gamePaused.get_height())

# Velocities
VELOCITIES = [[4, -4], [3, -3]]
ball_vel_x, ball_vel_y = random.choice(VELOCITIES[0]), random.choice(VELOCITIES[1])
PADDLES_VEL = 4
CLOUDS_POTENTIAL_VELS = [1, -1]
cloud1_vel, cloud2_vel = random.choice(CLOUDS_POTENTIAL_VELS), random.choice(CLOUDS_POTENTIAL_VELS)
cloud3_vel, cloud4_vel = random.choice(CLOUDS_POTENTIAL_VELS), random.choice(CLOUDS_POTENTIAL_VELS)
CLOUDS_VELS = [cloud1_vel, cloud2_vel, cloud3_vel, cloud4_vel]
if equal(CLOUDS_VELS):
    odd = random.randint(0, len(CLOUDS_VELS) - 1)
    CLOUDS_VELS[odd] *= -1

# UI
paddle_right_points, paddle_left_points = 0, 0
limit_points = 5
name_right, name_left = "Right", "Left"

# Fonts:
FPS_FONT = pygame.font.SysFont("cambria", 12, True)
SCORE_FONT = pygame.font.SysFont("Verdana", 18)
NAMES_FONT = pygame.font.SysFont("Verdana", 22, True)
BUTTONS_FONT = pygame.font.SysFont("Verdana", 28, True)
PONG_FONT = pygame.font.Font(join([CurDir, "Assets", "SHOWG.ttf"]), 100)
PONG_FONT.set_italic(True)
PAUSED_TITLE_FONT = pygame.font.SysFont("Calibri", 30, True)
PAUSED_FONT = pygame.font.SysFont("Calibri", 16, True)

# Other:
clock = pygame.time.Clock()
FPS = 60

# Classes
class MainMenu:

    @staticmethod
    def Display():
        opened = False
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_game.under(pygame.mouse.get_pos()):
                        pygame.mouse.set_visible(False)
                        Game.run = True
                        Game.playing = True
                        Game.paused = False
                        Game.Play()
                    elif button_exit.under(pygame.mouse.get_pos()):
                        Transition(WIN, CYAN, BLACK)
                        quit()
                        sys.exit()
                if not opened:
                    Transition(WIN, BLACK, CYAN)
                    pygame.mixer.Sound.play(STARTING_GAME)
                    opened = True
            MainMenu.Move_clouds()
            MainMenu.Draw(CYAN)

    @staticmethod
    def Draw(bg: tuple):
        WIN.fill(bg)
        WIN.blit(SUN, (WIN.get_width() - SUN.get_width(), 0))
        WIN.blit(CLOUD1, (cloud1.x, cloud1.y))
        WIN.blit(CLOUD2, (cloud2.x, cloud2.y))
        WIN.blit(CLOUD3, (cloud3.x, cloud3.y))
        WIN.blit(CLOUD4, (cloud4.x, cloud4.y))
        for i in range(math.ceil(WIN.get_width() / GRASS_IMGAE.get_width())):
            WIN.blit(GRASS_IMGAE, (GRASS_IMGAE.get_width() * i, WIN.get_height() - GRASS_IMGAE.get_height()))
        WIN.blit(buttons_area, (WIN.get_width() / 2 - buttons_area.get_width() / 2,
                                WIN.get_height() / 2 - buttons_area.get_height() / 2 + 50))
        pygame.draw.rect(buttons_area, TRANSPERANT_BLACK, buttons_area_rect, 0, 25)
        button_game.rect.x, button_game.rect.y = WIN.get_width() / 2 - button_game.rect.width / 2, WIN.get_height() / 2 - 50
        button_settings.rect.x, button_settings.rect.y = WIN.get_width() / 2 - button_settings.rect.width / 2, WIN.get_height() / 2 + button_settings.rect.height / 2
        button_exit.rect.x, button_exit.rect.y = WIN.get_width() / 2 - button_exit.rect.width / 2, WIN.get_height() / 2 + 100
        button_game.Draw(BLUE, BLUE, WHITE, 3, 10, False)
        button_settings.Draw(PURPLE, PURPLE, WHITE, 3, 10, False)
        button_exit.Draw(RED, RED, WHITE, 3, 10, False)
        Name = PONG_FONT.render("PONG", 1, BLUE)
        WIN.blit(Name, (WIN.get_width() / 2 - Name.get_width() / 2, WIN.get_height() / 7))
        pygame.display.update()

    @staticmethod
    def Move_clouds():
        for i, cloud in enumerate([cloud1, cloud2, cloud3, cloud4]):
            cloud.x += CLOUDS_VELS[i]
            if cloud.x > WIN.get_width() or cloud.right < 0: # Respawn cloud
                cloud.y = random.randint(CLOUDS_Y[i][0], CLOUDS_Y[i][1])
                CLOUDS_VELS[i] = random.choice(CLOUDS_POTENTIAL_VELS)
                if equal(CLOUDS_VELS):
                    CLOUDS_VELS[i] *= -1
                if CLOUDS_VELS[i] == CLOUDS_POTENTIAL_VELS[0]:
                    cloud.x = 0 - cloud.width
                else:
                    cloud.x = WIN.get_width()

class Game:
    
    run = True
    playing = True
    paused = False
    in_paused_menu = False
    winner = ""

    @staticmethod
    def Play():
        while Game.run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    sys.exit()
            Game.Draw(SPECIAL_COLOR, GRAY, WHITE, BLACK)
            Game.UI(CYAN, WHITE)
            if Game.playing and not Game.paused:
                Game.Ball_movement()
                Game.Paddles_movement()
            else:
                Game.Center_ball_paddles()
                if Game.paused and Game.playing and Game.in_paused_menu:
                    Game.Paused_menu_UI()
                    Game.Paused_menu_Keys()
            pygame.display.update()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                if Game.in_paused_menu == False:
                    Game.paused = True
                    Game.in_paused_menu = True
                else:
                    Game.paused = False
                    Game.in_paused_menu = False

    @staticmethod
    def Draw(bg: tuple, Ball_color: tuple, Paddles_color: tuple, Lines_color: tuple):
        WIN.fill(bg)
        pygame.draw.line(WIN, Lines_color, (WIN.get_width() / 2, 0),
                                                    (WIN.get_width() / 2, WIN.get_height()), 2)
        pygame.draw.line(WIN, Lines_color, (0, int(WIN.get_height() / 7.5)),
                                                    (WIN.get_width(), int(WIN.get_height() / 7.5)), 4)
        pygame.draw.ellipse(WIN, Ball_color, ball)
        Paddle_right.x = WIN.get_width() - Paddle_right.width - 2
        Paddle_right.height = int(WIN.get_height() / 8.57)
        Paddle_left.height = Paddle_right.height
        pygame.draw.rect(WIN, Paddles_color, Paddle_right)
        pygame.draw.rect(WIN, Paddles_color, Paddle_left)

    @staticmethod
    def UI(Score_color: tuple, Names_color: tuple):
        fps = FPS_FONT.render(str(int(clock.get_fps())), 1, Score_color)
        right_player_points = SCORE_FONT.render(f"Score: {paddle_right_points}/{limit_points}", 1, Score_color)
        left_player_points = SCORE_FONT.render(f"Score: {paddle_left_points}/{limit_points}", 1, Score_color)
        if Game.playing:
            right_player_name = NAMES_FONT.render(name_right, 1, Names_color)
            left_player_name = NAMES_FONT.render(name_left, 1, Names_color)
        elif Game.winner != "":
            if Game.winner == name_right:
                right_player_name = NAMES_FONT.render(f"{name_right} Won!", 1, GREEN)
                left_player_name = NAMES_FONT.render(f"{name_left} Lost!", 1, RED)
            else:
                right_player_name = NAMES_FONT.render(f"{name_right} Lost!", 1, RED)
                left_player_name = NAMES_FONT.render(f"{name_left} Won!", 1, GREEN)
            game_over = SCORE_FONT.render("Hello there", 1, BLUE, WHITE)
            WIN.blit(gameOver, (WIN.get_width() / 2 - gameOver.get_width() / 2,
                                        WIN.get_height() / 2 - gameOver.get_height() / 2))
            pygame.draw.rect(gameOver, TRANSPERANT_BLACK, gameOver_rect, 0, 25)
            WIN.blit(game_over, (WIN.get_width() / 2 - game_over.get_width() / 2,
                                        WIN.get_height() / 2 - game_over.get_height() / 2))
        else: raise Exception("Something is wrong!")
        WIN.blit(fps, (WIN.get_width() - fps.get_width() - 3, 0))
        WIN.blit(right_player_points, (WIN.get_width() / 2 + 10, 10))
        WIN.blit(left_player_points, (10, 10))
        WIN.blit(right_player_name, (WIN.get_width() / 2 + 10,
                                            int(WIN.get_height() / 7.5) - right_player_name.get_height() - 10))
        WIN.blit(left_player_name, (10, int(WIN.get_height() / 7.5) - right_player_name.get_height() - 10))

    @staticmethod
    def Ball_movement():
        global ball_vel_x, ball_vel_y
        ball.x += ball_vel_x
        ball.y += ball_vel_y
        # Intersection with right paddle
        if ball.right >= Paddle_right.left:
            if ball.centery - 5 < Paddle_right.bottom and\
               ball.centery + 5 > Paddle_right.top: # If the right paddle blocked the ball
                pygame.mixer.Sound.play(HIT_BALL)
                ball_vel_x *= -1
                ball.right = Paddle_right.left
            else:
                Game.New_round("left")
        # Intersection with left paddle
        elif ball.left <= Paddle_left.right:
            if ball.centery - 5 < Paddle_left.bottom and\
               ball.centery + 5 > Paddle_left.top: # If the left paddle blocked the ball
                pygame.mixer.Sound.play(HIT_BALL)
                ball_vel_x *= -1
                ball.left = Paddle_left.right
            else:
                Game.New_round("right")
        # Collisions
        if ball.top <= int(WIN.get_height() / 7.5) or ball.bottom >= WIN.get_height():
            ball_vel_y *= -1
        if ball.left <= 0 or ball.right >= WIN.get_width():
            ball_vel_x *= -1

    @staticmethod
    def Paddles_movement():
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]: # Up
            if Paddle_right.top - PADDLES_VEL > int(WIN.get_height() / 7.5):
                Paddle_right.y -= PADDLES_VEL
        if keys_pressed[pygame.K_DOWN]: # Down
            if Paddle_right.bottom + PADDLES_VEL <= WIN.get_height():
                Paddle_right.y += PADDLES_VEL
        if keys_pressed[pygame.K_w]: # W
            if Paddle_left.top - PADDLES_VEL > int(WIN.get_height() / 7.5):
                Paddle_left.y -= PADDLES_VEL
        if keys_pressed[pygame.K_s]: # S
            if Paddle_left.bottom + PADDLES_VEL <= WIN.get_height():
                Paddle_left.y += PADDLES_VEL

    @staticmethod
    def New_round(winner: str):
        global ball_vel_x, paddle_right_points, paddle_left_points
        pygame.mixer.Sound.play(LOST)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(int(2.5 * 1000))
        ball.center = (WIN.get_width() / 2, WIN.get_height() / 2 + int(WIN.get_height() / 7.5) / 2)
        if winner == "right":
            ball_vel_x = VELOCITIES[0][1]
            paddle_right_points += 1
            if paddle_right_points >= limit_points:
                Game.winner = name_right
                Game.playing = False
        elif winner == "left":
            ball_vel_x = VELOCITIES[0][0]
            paddle_left_points += 1
            if paddle_left_points >= limit_points:
                Game.winner = name_left
                Game.playing = False
        else: raise Exception("Please enter \"right\" or \"left\".")
    
    @staticmethod
    def Center_ball_paddles():
        ball.center = (WIN.get_width() / 2, WIN.get_height() / 2 + int(WIN.get_height() / 7.5) / 2)
        Paddle_right.centery = WIN.get_height() / 2 + int(WIN.get_height() / 7.5) / 2
        Paddle_left.centery = WIN.get_height() / 2 + int(WIN.get_height() / 7.5) / 2

    @staticmethod
    def Paused_menu_UI():
        WIN.blit(gamePaused, (WIN.get_width() / 2 - gamePaused.get_width() / 2,
                                    WIN.get_height() / 2 - gamePaused.get_height() / 2 + int(WIN.get_height() / 7.5) / 2))
        pygame.draw.rect(gamePaused, TRANSPERANT_BLACK, gamePaused_rect, 0, 25)
        paused_text_title = PAUSED_TITLE_FONT.render("Game Paused", 1, RED)
        paused_text_continue = PAUSED_FONT.render("To keep playing, press Enter", 1, PURPLE)
        paused_text_back = PAUSED_FONT.render("To go back to main menu, press ESC", 1, PURPLE)
        WIN.blit(paused_text_title, (WIN.get_width() / 2 - paused_text_title.get_width() / 2,
        WIN.get_height() / 2 - gamePaused.get_height() / 2 + int(WIN.get_height() / 7.5) / 2 + gamePaused.get_height() / 8))

        WIN.blit(paused_text_continue, (WIN.get_width() / 2 - paused_text_continue.get_width() / 2,
        WIN.get_height() / 2 - gamePaused.get_height() / 2 + int(WIN.get_height() / 7.5) / 2 + 50))

        WIN.blit(paused_text_back, (WIN.get_width() / 2 - paused_text_back.get_width() / 2,
        WIN.get_height() / 2 - gamePaused.get_height() / 2 + int(WIN.get_height() / 7.5) / 2 + 75))
    
    @staticmethod
    def Paused_menu_Keys():
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_KP_ENTER] or keys_pressed[13]: # 13 is the ascii code for the left Enter key.
            Game.run = False
            Game.playing = False
            Game.paused = False
            Game.in_paused_menu = False
            pygame.mouse.set_visible(True)

class Settings:
    pass

class Button:

    def __init__(self, Surface: pygame.Surface, Rect: pygame.Rect, Text: str, Font: pygame.font.Font):
        self.screen = Surface
        self.rect = Rect
        self.text = Text
        self.font = Font

    def under(self, clicked_pos: tuple) -> bool:
        if clicked_pos[0] >= self.rect.x and clicked_pos[0] <= self.rect.right and\
            clicked_pos[1] >= self.rect.y and clicked_pos[1] <= self.rect.bottom:
            return True
        else: return False

    @dispatch(tuple, tuple, bool)
    def Draw(self, Button_color: tuple, Text_color: tuple, update: bool = True):
        text = self.font.render(self.text, 1, Text_color)
        pygame.draw.rect(self.screen, Button_color, self.rect)
        self.screen.blit(text, (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2))
        if update: pygame.display.update()

    @dispatch(tuple, tuple, tuple, int, bool)
    def Draw(self, Outline_color: tuple, Text_color: tuple, bg: tuple, width: int, update: bool = True):
        text = self.font.render(self.text, 1, Text_color)
        pygame.draw.rect(self.screen, bg, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)
        pygame.draw.rect(self.screen, Outline_color, self.rect, width)
        self.screen.blit(text, (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2))
        if update: pygame.display.update()

    @dispatch(tuple, tuple, tuple, int, int, bool)
    def Draw(self, Outline_color: tuple, Text_color: tuple, bg: tuple, width: int, border_radius: int, update: bool = True):
        text = self.font.render(self.text, 1, Text_color)
        pygame.draw.rect(self.screen, bg, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0, border_radius)
        pygame.draw.rect(self.screen, Outline_color, self.rect, width, border_radius)
        self.screen.blit(text, (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2))
        if update: pygame.display.update()

# Objects:
button_game = Button(WIN, play_button, "Play", BUTTONS_FONT)
button_settings = Button(WIN, settings_button, "Settings", BUTTONS_FONT)
button_exit = Button(WIN, exit_button, "Exit", BUTTONS_FONT)

def main():
    MainMenu.Display()

if __name__ == "__main__":
    main()
