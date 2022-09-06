import pygame
import random, math, sys
from multipledispatch import dispatch
from utils import *

# Initialization:
pygame.init()
pygame.font.init()
pygame.display.init()
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load(join(['Assets', 'Images', 'icon.png'])))

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
HIT_BALL = pygame.mixer.Sound(join(['Assets', 'Sound effects', 'HittingBall.mp3']))
LOST = pygame.mixer.Sound(join(['Assets', 'Sound effects', 'Lost.mp3']))
STARTING_GAME = pygame.mixer.Sound(join(['Assets', 'Sound effects', 'StartOfGame.mp3']))
TRANSITION_SOUND = pygame.mixer.Sound(join(['Assets', 'Sound effects', 'Transition.wav']))

# Images
CLOUD1 = pygame.image.load(join(['Assets', 'Images', 'cloud1.png']))
CLOUD1 = pygame.transform.scale(CLOUD1, (125, 125))
CLOUD2 = pygame.image.load(join(['Assets', 'Images', 'cloud2.png']))
CLOUD3 = pygame.image.load(join(['Assets', 'Images', 'cloud3.png']))
CLOUD4 = pygame.image.load(join(['Assets', 'Images', 'cloud4.png']))
GRASS_IMGAE = pygame.image.load(join(['Assets', 'Images', 'grass.png']))
GRASS_IMGAE = pygame.transform.scale(GRASS_IMGAE, (100, 80))
SUN = pygame.image.load(join(['Assets', 'Images', 'sun.png']))
SUN = pygame.transform.scale(SUN, (175, 175))

# Visual objects
Paddle_right = pygame.Rect(0, HEIGHT / 2 - 35, 6, 70)
Paddle_left = pygame.Rect(2, HEIGHT / 2 - 35, 6, 70)
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)

play_button = pygame.Rect(0, 0, 160, 50)
settings_button = pygame.Rect(0, 0, 160, 50)
exit_button = pygame.Rect(0, 0, 160, 50)

CLOUDS_Y = [(20, 75), (50, 150), (125, 175), (150, 250)]
cloud1 = pygame.Rect(random.randint(0, WIDTH - CLOUD1.get_width()), random.randint(CLOUDS_Y[0][0], CLOUDS_Y[0][1]), CLOUD1.get_width(), CLOUD1.get_height())
cloud2 = pygame.Rect(random.randint(0, WIDTH - CLOUD2.get_width()), random.randint(CLOUDS_Y[1][0], CLOUDS_Y[1][1]), CLOUD2.get_width(), CLOUD2.get_height())
cloud3 = pygame.Rect(random.randint(0, WIDTH - CLOUD3.get_width()), random.randint(CLOUDS_Y[2][0], CLOUDS_Y[2][1]), CLOUD3.get_width(), CLOUD3.get_height())
cloud4 = pygame.Rect(random.randint(0, WIDTH - CLOUD4.get_width()), random.randint(CLOUDS_Y[3][0], CLOUDS_Y[3][1]), CLOUD4.get_width(), CLOUD4.get_height())

buttons_area = pygame.Surface((275, 275), pygame.SRCALPHA)
buttons_area_rect = pygame.Rect(0, 0, buttons_area.get_width(), buttons_area.get_height())

gameOver = pygame.Surface((300, 300), pygame.SRCALPHA)
gameOver_rect = pygame.Rect(0, 0, gameOver.get_width(), gameOver.get_height())

gamePaused = pygame.Surface((250, 250), pygame.SRCALPHA)
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
PAUSED_FONT = pygame.font.SysFont("Calibri", 30, True)
BUTTONS_FONT = pygame.font.SysFont("Verdana", 28, True)
PONG_FONT = pygame.font.SysFont("showcardgothic", 100, False, True)

# Other:
clock = pygame.time.Clock()
FPS = 60

# Classes
class MainMenu:

    def __init__(self, Surface: pygame.Surface):
        self.screen = Surface


    def Display(self, bg: tuple):
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_game.on_button(pygame.mouse.get_pos()):
                        game.Play()
                    elif button_exit.on_button(pygame.mouse.get_pos()):
                        Transition(WIN, CYAN, BLACK)
                        quit()
                        sys.exit()
            self.Move_clouds()
            self.Draw(bg)
            pygame.display.update()
    

    def Draw(self, bg: tuple):
        self.screen.fill(bg)
        self.screen.blit(SUN, (self.screen.get_width() - SUN.get_width(), 0))
        self.screen.blit(CLOUD1, (cloud1.x, cloud1.y))
        self.screen.blit(CLOUD2, (cloud2.x, cloud2.y))
        self.screen.blit(CLOUD3, (cloud3.x, cloud3.y))
        self.screen.blit(CLOUD4, (cloud4.x, cloud4.y))
        for i in range(math.ceil(self.screen.get_width() / GRASS_IMGAE.get_width())):
            self.screen.blit(GRASS_IMGAE, (GRASS_IMGAE.get_width() * i, self.screen.get_height() - GRASS_IMGAE.get_height()))
        self.screen.blit(buttons_area, (self.screen.get_width() / 2 - buttons_area.get_width() / 2,
                                        self.screen.get_height() / 2 - buttons_area.get_height() / 2 + 50))
        pygame.draw.rect(buttons_area, TRANSPERANT_BLACK, buttons_area_rect, 0, 25)
        button_game.rect.x, button_game.rect.y = self.screen.get_width() / 2 - button_game.rect.width / 2, self.screen.get_height() / 2 - 50
        button_settings.rect.x, button_settings.rect.y = self.screen.get_width() / 2 - button_settings.rect.width / 2, self.screen.get_height() / 2 + button_settings.rect.height / 2
        button_exit.rect.x, button_exit.rect.y = self.screen.get_width() / 2 - button_exit.rect.width / 2, self.screen.get_height() / 2 + 100
        button_game.Draw(BLUE, BLUE, WHITE, 3, 10, False)
        button_settings.Draw(PURPLE, PURPLE, WHITE, 3, 10, False)
        button_exit.Draw(RED, RED, WHITE, 3, 10, False)
        Name = PONG_FONT.render("PONG", 1, BLUE)
        self.screen.blit(Name, (self.screen.get_width() / 2 - Name.get_width() / 2 + 10, self.screen.get_height() / 7))


    def Move_clouds(self):
        i = 0
        for cloud in [cloud1, cloud2, cloud3, cloud4]:
            cloud.x += CLOUDS_VELS[i]
            if cloud.x > self.screen.get_width() or cloud.right < 0: # Respawn cloud
                cloud.y = random.randint(CLOUDS_Y[i][0], CLOUDS_Y[i][1])
                CLOUDS_VELS[i] = random.choice(CLOUDS_POTENTIAL_VELS)
                if equal(CLOUDS_VELS):
                    CLOUDS_VELS[i] *= -1
                if CLOUDS_VELS[i] == CLOUDS_POTENTIAL_VELS[0]:
                    cloud.x = 0 - cloud.width
                else:
                    cloud.x = self.screen.get_width()
            i += 1

class Game:

    def __init__(self, Surface: pygame.Surface,  Ball: pygame.Rect, Paddle_right: pygame.Rect, Paddle_left: pygame.Rect,
                FPS_font: pygame.font.Font, Score_Font: pygame.font.Font, Names_Font: pygame.font.Font, Paused_Font: pygame.font.Font,
                Hit_sound: pygame.mixer.Sound, Lost_sound: pygame.mixer.Sound):
        self.playing = True
        self.paused = False
        self.screen = Surface
        self.ball = Ball
        self.paddle_right = Paddle_right
        self.paddle_left = Paddle_left
        self.fps_font = FPS_font
        self.score_font = Score_Font
        self.names_font = Names_Font
        self.paused_font = Paused_Font
        self.hit_sound = Hit_sound
        self.lose_sound = Lost_sound
        self.winner = ""
    

    def Play(self):
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    quit()
                    sys.exit()
            self.Draw(SPECIAL_COLOR, GRAY, WHITE, BLACK)
            self.UI(CYAN, WHITE)
            if self.playing and not self.paused:
                self.Ball_movement()
                self.Paddles_movement()
            else:
                self.Center_ball_paddles()
                if self.paused and self.playing:
                    self.Paused_menu(RED)
            pygame.display.update()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                self.paused = True
            if keys_pressed[pygame.K_v]: # For now
                self.paused = False


    def Draw(self, bg: tuple, Ball_color: tuple, Paddles_color: tuple, Lines_color: tuple):
        self.screen.fill(bg)
        pygame.draw.line(self.screen, Lines_color, (self.screen.get_width() / 2, 0),
                                                    (self.screen.get_width() / 2, self.screen.get_height()), 2)
        pygame.draw.line(self.screen, Lines_color, (0, int(self.screen.get_height() / 7.5)),
                                                    (self.screen.get_width(), int(self.screen.get_height() / 7.5)), 4)
        pygame.draw.ellipse(self.screen, Ball_color, self.ball)
        self.paddle_right.x = self.screen.get_width() - self.paddle_right.width - 2
        self.paddle_right.height = int(self.screen.get_height() / 8.57)
        self.paddle_left.height = self.paddle_right.height
        pygame.draw.rect(self.screen, Paddles_color, self.paddle_right)
        pygame.draw.rect(self.screen, Paddles_color, self.paddle_left)


    def UI(self, Score_color: tuple, Names_color: tuple):
        fps = self.fps_font.render(str(int(clock.get_fps())), 1, Score_color)
        right_player_points = self.score_font.render(f"Score: {paddle_right_points}/{limit_points}", 1, Score_color)
        left_player_points = self.score_font.render(f"Score: {paddle_left_points}/{limit_points}", 1, Score_color)
        if self.playing:
            right_player_name = self.names_font.render(name_right, 1, Names_color)
            left_player_name = self.names_font.render(name_left, 1, Names_color)
        elif self.winner != "":
            if self.winner == name_right:
                right_player_name = self.names_font.render(f"{name_right} Won!", 1, GREEN)
                left_player_name = self.names_font.render(f"{name_left} Lost!", 1, RED)
            else:
                right_player_name = self.names_font.render(f"{name_right} Lost!", 1, RED)
                left_player_name = self.names_font.render(f"{name_left} Won!", 1, GREEN)
            game_over = self.score_font.render("Hello there", 1, BLUE, WHITE)
            self.screen.blit(gameOver, (self.screen.get_width() / 2 - gameOver.get_width() / 2,
                                        self.screen.get_height() / 2 - gameOver.get_height() / 2))
            pygame.draw.rect(gameOver, TRANSPERANT_BLACK, gameOver_rect, 0, 25)
            self.screen.blit(game_over, (self.screen.get_width() / 2 - game_over.get_width() / 2,
                                        self.screen.get_height() / 2 - game_over.get_height() / 2))
        else: raise Exception("Something is wrong!")
        self.screen.blit(fps, (self.screen.get_width() - fps.get_width() - 3, 0))
        self.screen.blit(right_player_points, (self.screen.get_width() / 2 + 10, 10))
        self.screen.blit(left_player_points, (10, 10))
        self.screen.blit(right_player_name, (self.screen.get_width() / 2 + 10,
                                            int(self.screen.get_height() / 7.5) - right_player_name.get_height() - 10))
        self.screen.blit(left_player_name, (10, int(self.screen.get_height() / 7.5) - right_player_name.get_height() - 10))


    def Ball_movement(self):
        global ball_vel_x, ball_vel_y
        self.ball.x += ball_vel_x
        self.ball.y += ball_vel_y
        # Intersection with right paddle
        if self.ball.right >= self.paddle_right.left:
            if self.ball.centery - 5 < self.paddle_right.bottom and\
               self.ball.centery + 5 > self.paddle_right.top: # If the right paddle blocked the ball
                pygame.mixer.Sound.play(self.hit_sound)
                ball_vel_x *= -1
                self.ball.right = self.paddle_right.left
            else:
                self.New_round("left")
        # Intersection with left paddle
        elif self.ball.left <= self.paddle_left.right:
            if self.ball.centery - 5 < self.paddle_left.bottom and\
               self.ball.centery + 5 > self.paddle_left.top: # If the left paddle blocked the ball
                pygame.mixer.Sound.play(self.hit_sound)
                ball_vel_x *= -1
                self.ball.left = self.paddle_left.right
            else:
                self.New_round("right")
        # Collisions
        if self.ball.top <= int(self.screen.get_height() / 7.5) or self.ball.bottom >= self.screen.get_height():
            ball_vel_y *= -1
        if self.ball.left <= 0 or self.ball.right >= self.screen.get_width():
            ball_vel_x *= -1
    

    def Paddles_movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]: # Up
            if self.paddle_right.top - PADDLES_VEL > int(self.screen.get_height() / 7.5):
                self.paddle_right.y -= PADDLES_VEL
        if keys_pressed[pygame.K_DOWN]: # Down
            if self.paddle_right.bottom + PADDLES_VEL <= self.screen.get_height():
                self.paddle_right.y += PADDLES_VEL
        if keys_pressed[pygame.K_w]: # W
            if self.paddle_left.top - PADDLES_VEL > int(self.screen.get_height() / 7.5):
                self.paddle_left.y -= PADDLES_VEL
        if keys_pressed[pygame.K_s]: # S
            if self.paddle_left.bottom + PADDLES_VEL <= self.screen.get_height():
                self.paddle_left.y += PADDLES_VEL


    def New_round(self, winner: str):
        global ball_vel_x, paddle_right_points, paddle_left_points
        pygame.mixer.Sound.play(self.lose_sound)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(int(2.5 * 1000))
        self.ball.center = (self.screen.get_width() / 2, self.screen.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2)
        if winner == "right":
            ball_vel_x = VELOCITIES[0][1]
            paddle_right_points += 1
            if paddle_right_points >= limit_points:
                self.winner = name_right
                self.playing = False
        elif winner == "left":
            ball_vel_x = VELOCITIES[0][0]
            paddle_left_points += 1
            if paddle_left_points >= limit_points:
                self.winner = name_left
                self.playing = False
        else: raise Exception("Please enter \"right\" or \"left\".")
    
    
    def Center_ball_paddles(self):
        self.ball.center = (self.screen.get_width() / 2, self.screen.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2)
        self.paddle_right.centery = self.screen.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2
        self.paddle_left.centery = self.screen.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2


    def Paused_menu(self, Text_color: tuple):
        self.screen.blit(gamePaused, (self.screen.get_width() / 2 - gamePaused.get_width() / 2,
                                    self.screen.get_height() / 2 - gamePaused.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2))
        pygame.draw.rect(gamePaused, TRANSPERANT_BLACK, gamePaused_rect, 0, 25)
        paused_text = self.paused_font.render("Paused", 1, Text_color)
        self.screen.blit(paused_text, (self.screen.get_width() / 2 - paused_text.get_width() / 2,
        self.screen.get_height() / 2 - gamePaused.get_height() / 2 + int(self.screen.get_height() / 7.5) / 2 + gamePaused.get_height() / 7))

class Settings:
    pass

class Button:

    def __init__(self, Surface: pygame.Surface, Rect: pygame.Rect, Text: str, Font: pygame.font.Font):
        self.screen = Surface
        self.rect = Rect
        self.text = Text
        self.font = Font

    def on_button(self, clicked_pos: tuple) -> bool:
        if clicked_pos[0] > self.rect.x and clicked_pos[0] < self.rect.right and\
            clicked_pos[1] > self.rect.y and clicked_pos[1] < self.rect.bottom:
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
mainMenu = MainMenu(WIN)
game = Game(WIN, ball, Paddle_right, Paddle_left, FPS_FONT, SCORE_FONT, NAMES_FONT, PAUSED_FONT, HIT_BALL, LOST)
settings = Settings()
button_game = Button(WIN, play_button, "Play", BUTTONS_FONT)
button_settings = Button(WIN, settings_button, "Settings", BUTTONS_FONT)
button_exit = Button(WIN, exit_button, "Exit", BUTTONS_FONT)


def main():
    Transition(WIN, BLACK, CYAN)
    pygame.mixer.Sound.play(STARTING_GAME)
    mainMenu.Display(CYAN)


if __name__ == "__main__":
    main()