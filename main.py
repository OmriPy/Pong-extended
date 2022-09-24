import pygame
import random, sys, os
from math import ceil
from utils import *


# Initialization:
CurDir = os.path.dirname(__file__) # Change this variable's value to pathlib.Path.cwd() when Building
pygame.init()
pygame.font.init()
pygame.display.init()
WIDTH, HEIGHT = 1000, 600
Window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
ICON = pygame.image.load(join([CurDir, 'Assets', 'Images', 'icon.png']))
pygame.display.set_icon(ICON)


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

CLOUDS_Y: dict[int, tuple] = {
    0: (20, 75),
    1: (50, 150),
    2: (125, 175),
    3: (150, 250)
}
cloud1 = pygame.Rect(random.randint(0, WIDTH - CLOUD1.get_width()), random.randint(CLOUDS_Y.get(0)[0], CLOUDS_Y.get(0)[1]),
                    CLOUD1.get_width(), CLOUD1.get_height())
cloud2 = pygame.Rect(random.randint(0, WIDTH - CLOUD2.get_width()), random.randint(CLOUDS_Y.get(1)[0], CLOUDS_Y.get(1)[1]),
                    CLOUD2.get_width(), CLOUD2.get_height())
cloud3 = pygame.Rect(random.randint(0, WIDTH - CLOUD3.get_width()), random.randint(CLOUDS_Y.get(2)[0], CLOUDS_Y.get(2)[1]),
                    CLOUD3.get_width(), CLOUD3.get_height())
cloud4 = pygame.Rect(random.randint(0, WIDTH - CLOUD4.get_width()), random.randint(CLOUDS_Y.get(3)[0], CLOUDS_Y.get(3)[1]),
                    CLOUD4.get_width(), CLOUD4.get_height())

buttons_area = pygame.Surface((275, 275), pygame.SRCALPHA)
buttons_area_rect = pygame.Rect(0, 0, buttons_area.get_width(), buttons_area.get_height())

gameOver = pygame.Surface((300, 300), pygame.SRCALPHA)
gameOver_rect = pygame.Rect(0, 0, gameOver.get_width(), gameOver.get_height())

gamePaused = pygame.Surface((300, 100), pygame.SRCALPHA)
gamePaused_rect = pygame.Rect(0, 0, gamePaused.get_width(), gamePaused.get_height())

# Velocities
BALL_VELS = {"X": (4, -4), "Y": (3, -3)}
ball_vel_x, ball_vel_y = random.choice(BALL_VELS.get("X")), random.choice(BALL_VELS.get("Y"))
PADDLES_VEL = 4
CLOUDS_POTENTIAL_VELS = [1, -1]
cloud1_vel, cloud2_vel = random.choice(CLOUDS_POTENTIAL_VELS), random.choice(CLOUDS_POTENTIAL_VELS)
cloud3_vel, cloud4_vel = random.choice(CLOUDS_POTENTIAL_VELS), random.choice(CLOUDS_POTENTIAL_VELS)
CLOUDS_VELS = [cloud1_vel, cloud2_vel, cloud3_vel, cloud4_vel]
if equal(CLOUDS_VELS):
    odd = random.randint(0, len(CLOUDS_VELS) - 1)
    CLOUDS_VELS[odd] *= -1

# UI
paddle_left_points, paddle_right_points = 0, 0
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

# Time:
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
                if event.type == pygame.QUIT:
                    quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Button_Game.Under(pygame.mouse.get_pos()):
                        pygame.mouse.set_visible(False)
                        Game.Run = True
                        Game.Playing = True
                        Game.Paused = False
                        Game.Play()
                    elif Button_Exit.Under(pygame.mouse.get_pos()):
                        Transition(Window, COLORS.get("CYAN"), COLORS.get("BLACK"))
                        quit()
                        sys.exit()
                if not opened:
                    Transition(Window, COLORS.get("BLACK"), COLORS.get("CYAN"))
                    pygame.mixer.Sound.play(STARTING_GAME)
                    opened = True
            MainMenu.Move_clouds()
            MainMenu.Draw(COLORS.get("CYAN"))

    @staticmethod
    def Draw(bg: tuple):
        Window.fill(bg)
        Window.blit(SUN, (Window.get_width() - SUN.get_width(), 0))
        Window.blit(CLOUD1, (cloud1.x, cloud1.y))
        Window.blit(CLOUD2, (cloud2.x, cloud2.y))
        Window.blit(CLOUD3, (cloud3.x, cloud3.y))
        Window.blit(CLOUD4, (cloud4.x, cloud4.y))
        for i in range(ceil(Window.get_width() / GRASS_IMGAE.get_width())):
            Window.blit(GRASS_IMGAE, (GRASS_IMGAE.get_width() * i, Window.get_height() - GRASS_IMGAE.get_height()))
        Window.blit(buttons_area, (Window.get_width() / 2 - buttons_area.get_width() / 2,
                                Window.get_height() / 2 - buttons_area.get_height() / 2 + 50))
        pygame.draw.rect(buttons_area, COLORS.get("TRANSP_BLACK"), buttons_area_rect, 0, 25)
        Button_Game.rect.x, Button_Game.rect.y = Window.get_width() / 2 - Button_Game.rect.width / 2, Window.get_height() / 2 - 50
        Button_Settings.rect.x, Button_Settings.rect.y = Window.get_width() / 2 - Button_Settings.rect.width / 2, Window.get_height() / 2 + Button_Settings.rect.height / 2
        Button_Exit.rect.x, Button_Exit.rect.y = Window.get_width() / 2 - Button_Exit.rect.width / 2, Window.get_height() / 2 + 100
        Button_Game.Draw(COLORS.get("BLUE"), COLORS.get("BLUE"), COLORS.get("WHITE"), 3, 10)
        Button_Settings.Draw(COLORS.get("PURPLE"), COLORS.get("PURPLE"), COLORS.get("WHITE"), 3, 10)
        Button_Exit.Draw(COLORS.get("RED"), COLORS.get("RED"), COLORS.get("WHITE"), 3, 10)
        Name = PONG_FONT.render("PONG", 1, COLORS.get("BLUE"))
        Window.blit(Name, (Window.get_width() / 2 - Name.get_width() / 2, Window.get_height() / 7))
        pygame.display.update()

    @staticmethod
    def Move_clouds():
        for i, cloud in enumerate([cloud1, cloud2, cloud3, cloud4]):
            cloud.x += CLOUDS_VELS[i]
            if cloud.x > Window.get_width() or cloud.right < 0: # Respawn cloud
                cloud.y = random.randint(CLOUDS_Y.get(i)[0], CLOUDS_Y.get(i)[1])
                CLOUDS_VELS[i] = random.choice(CLOUDS_POTENTIAL_VELS)
                if equal(CLOUDS_VELS):
                    CLOUDS_VELS[i] *= -1
                if CLOUDS_VELS[i] == CLOUDS_POTENTIAL_VELS[0]:
                    cloud.x = 0 - cloud.width
                else:
                    cloud.x = Window.get_width()

class Game:
    
    Run = False
    Playing = False
    Paused = False
    Horizontal_Line_Y: None
    Winner = ""

    @staticmethod
    def Play():
        while Game.Run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    sys.exit()
            Game.Horizontal_Line_Y = int(Window.get_height() / 7.5)
            Game.Draw(COLORS.get("SPECIAL"), COLORS.get("GRAY"), COLORS.get("WHITE"), COLORS.get("BLACK"))
            Game.UI(COLORS.get("CYAN"), COLORS.get("WHITE"))
            if Game.Playing and not Game.Paused:
                Game.Ball_Movement()
                Game.Paddles_Movement()
            else:
                Game.Center_ball_paddles()
                if Game.Playing and Game.Paused:
                    Game.Paused_Menu_UI()
                    Game.Paused_Menu_Keys()
            pygame.display.update()

    @staticmethod
    def Draw(bg: tuple, Ball_color: tuple, Paddles_color: tuple, Lines_color: tuple):
        Window.fill(bg)
        pygame.draw.line(Window, Lines_color, (Window.get_width() / 2, 0),
                                            (Window.get_width() / 2, Window.get_height()), 2)
        pygame.draw.line(Window, Lines_color, (0, Game.Horizontal_Line_Y),
                                            (Window.get_width(), Game.Horizontal_Line_Y), 4)
        pygame.draw.ellipse(Window, Ball_color, ball)
        Paddle_right.x = Window.get_width() - Paddle_right.width - 2
        Paddle_right.height = int(Window.get_height() / 8.57)
        Paddle_left.height = Paddle_right.height
        pygame.draw.rect(Window, Paddles_color, Paddle_right)
        pygame.draw.rect(Window, Paddles_color, Paddle_left)

    @staticmethod
    def UI(Score_color: tuple, Names_color: tuple):
        fps = FPS_FONT.render(str(int(clock.get_fps())), 1, Score_color)
        right_player_points = SCORE_FONT.render(f"Score: {paddle_right_points}/{limit_points}", 1, Score_color)
        left_player_points = SCORE_FONT.render(f"Score: {paddle_left_points}/{limit_points}", 1, Score_color)
        if Game.Playing:
            right_player_name = NAMES_FONT.render(name_right, 1, Names_color)
            left_player_name = NAMES_FONT.render(name_left, 1, Names_color)
        elif Game.Winner != "":
            if Game.Winner == name_right:
                right_player_name = NAMES_FONT.render(f"{name_right} Won!", 1, COLORS.get("GREEN"))
                left_player_name = NAMES_FONT.render(f"{name_left} Lost!", 1, COLORS.get("RED"))
            else:
                right_player_name = NAMES_FONT.render(f"{name_right} Lost!", 1, COLORS.get("RED"))
                left_player_name = NAMES_FONT.render(f"{name_left} Won!", 1, COLORS.get("GREEN"))
            game_over = SCORE_FONT.render("Hello there", 1, COLORS.get("BLUE"), COLORS.get("WHITE"))
            Window.blit(gameOver, (Window.get_width() / 2 - gameOver.get_width() / 2,
                                        Window.get_height() / 2 - gameOver.get_height() / 2))
            pygame.draw.rect(gameOver, COLORS.get("TRANSP_BLACK"), gameOver_rect, 0, 25)
            Window.blit(game_over, (Window.get_width() / 2 - game_over.get_width() / 2,
                                        Window.get_height() / 2 - game_over.get_height() / 2))
        else: raise Exception("Something is wrong!")
        Window.blit(fps, (Window.get_width() - fps.get_width() - 3, 0))
        Window.blit(right_player_points, (Window.get_width() / 2 + 10, 10))
        Window.blit(left_player_points, (10, 10))
        Window.blit(right_player_name, (Window.get_width() / 2 + 10,
                                        Game.Horizontal_Line_Y - right_player_name.get_height() - 10))
        Window.blit(left_player_name, (10, Game.Horizontal_Line_Y - right_player_name.get_height() - 10))

    @staticmethod
    def Ball_Movement():
        global ball_vel_x, ball_vel_y
        ball.x += ball_vel_x
        ball.y += ball_vel_y
        if ball.right >= Paddle_right.left: # Intersection with right paddle
            if ball.centery - 5 < Paddle_right.bottom and\
               ball.centery + 5 > Paddle_right.top: # If the right paddle blocked the ball
                pygame.mixer.Sound.play(HIT_BALL)
                ball_vel_x *= -1
                ball.right = Paddle_right.left
            else:
                Game.New_round("left")
        elif ball.left <= Paddle_left.right :# Intersection with left paddle
            if ball.centery - 5 < Paddle_left.bottom and\
               ball.centery + 5 > Paddle_left.top: # If the left paddle blocked the ball
                pygame.mixer.Sound.play(HIT_BALL)
                ball_vel_x *= -1
                ball.left = Paddle_left.right
            else:
                Game.New_round("right")
        # Collisions
        if ball.top <= Game.Horizontal_Line_Y or ball.bottom >= Window.get_height():
            ball_vel_y *= -1
        if ball.left <= 0 or ball.right >= Window.get_width():
            ball_vel_x *= -1

    @staticmethod
    def Paddles_Movement():
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]: # Up
            if Paddle_right.top - PADDLES_VEL > Game.Horizontal_Line_Y:
                Paddle_right.y -= PADDLES_VEL
        if keys_pressed[pygame.K_DOWN]: # Down
            if Paddle_right.bottom + PADDLES_VEL <= Window.get_height():
                Paddle_right.y += PADDLES_VEL
        if keys_pressed[pygame.K_w]: # W
            if Paddle_left.top - PADDLES_VEL > Game.Horizontal_Line_Y:
                Paddle_left.y -= PADDLES_VEL
        if keys_pressed[pygame.K_s]: # S
            if Paddle_left.bottom + PADDLES_VEL <= Window.get_height():
                Paddle_left.y += PADDLES_VEL

    @staticmethod
    def New_round(Round_Winner: str):
        global ball_vel_x, paddle_right_points, paddle_left_points
        pygame.mixer.Sound.play(LOST)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(int(2.5 * 1000))
        ball.center = (Window.get_width() / 2, Window.get_height() / 2 + Game.Horizontal_Line_Y / 2)
        if Round_Winner == "right":
            ball_vel_x = BALL_VELS.get("X")[1]
            paddle_right_points += 1
            if paddle_right_points >= limit_points:
                Game.Winner = name_right
                Game.Playing = False
        elif Round_Winner == "left":
            ball_vel_x = BALL_VELS.get("X")[0]
            paddle_left_points += 1
            if paddle_left_points >= limit_points:
                Game.Winner = name_left
                Game.Playing = False
        else: raise Exception("Please enter \"right\" or \"left\".")

    @staticmethod
    def Center_ball_paddles():
        ball.center = (Window.get_width() / 2, Window.get_height() / 2 + Game.Horizontal_Line_Y / 2)
        Paddle_right.centery = Window.get_height() / 2 + Game.Horizontal_Line_Y / 2
        Paddle_left.centery = Window.get_height() / 2 + Game.Horizontal_Line_Y / 2

    @staticmethod
    def Paused_Menu_UI():
        Window.blit(gamePaused, (Window.get_width() / 2 - gamePaused.get_width() / 2,
                            Window.get_height() / 2 - gamePaused.get_height() / 2 + Game.Horizontal_Line_Y / 2))
        pygame.draw.rect(gamePaused, COLORS.get("TRASNP_BLACK"), gamePaused_rect, 0, 25)
        paused_text_title = PAUSED_TITLE_FONT.render("Game Paused", 1, COLORS.get("RED"))
        paused_text_continue = PAUSED_FONT.render("To keep playing, press Enter", 1, COLORS.get("PURPLE"))
        paused_text_back = PAUSED_FONT.render("To go back to main menu, press ESC", 1, COLORS.get("PURPLE"))
        Window.blit(paused_text_title, (Window.get_width() / 2 - paused_text_title.get_width() / 2,
        Window.get_height() / 2 - gamePaused.get_height() / 2 + Game.Horizontal_Line_Y / 2 + gamePaused.get_height() / 8))

        Window.blit(paused_text_continue, (Window.get_width() / 2 - paused_text_continue.get_width() / 2,
        Window.get_height() / 2 - gamePaused.get_height() / 2 + Game.Horizontal_Line_Y / 2 + 50))

        Window.blit(paused_text_back, (Window.get_width() / 2 - paused_text_back.get_width() / 2,
        Window.get_height() / 2 - gamePaused.get_height() / 2 + Game.Horizontal_Line_Y / 2 + 75))
    
    @staticmethod
    def Paused_Menu_Keys():
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_KP_ENTER] or keys_pressed[13]: # 13 is the ascii code for the left Enter key.
            Game.Run = False
            Game.Playing = False
            Game.Paused = False
            pygame.mouse.set_visible(True)
        elif keys_pressed[pygame.K_ESCAPE]:
            '''
            if not Game.Paused:
                Game.Paused = True
            else:
                Game.Paused = False
            '''
            Game.Paused = not Game.Paused

class Settings: ...

# Objects:
Button_Game = Button(Window, play_button, "Play", BUTTONS_FONT)
Button_Settings = Button(Window, settings_button, "Settings", BUTTONS_FONT)
Button_Exit = Button(Window, exit_button, "Exit", BUTTONS_FONT)

def main():
    MainMenu.Display()

if __name__ == "__main__":
    main()
