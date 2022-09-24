import pygame
import os

COLORS: dict[str, tuple] = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "PINK": (255, 0, 200),
    "PURPLE": (132, 52, 250),
    "CYAN": (0, 255, 255),
    "GRAY": (128, 128, 128),
    "SPECIAL": (27, 35, 43),
    "TRANSP_BLACK": (0, 0, 0, 64)
}

def quit():
    pygame.display.quit()
    pygame.font.quit()
    pygame.quit()

def join(dirs: list[str]) -> str:
    path = dirs[0]
    for i in range(1, len(dirs)):
        path = os.path.join(path, dirs[i])
    return path

def equal(vels: list[int]) -> bool:
    for i in range(len(vels)):
        if vels[i] != vels[0]: return False
    return True

def Transition(screen: pygame.Surface, starting_color: tuple | list, ending_color: tuple | list):
    starting_color = list(starting_color)
    ending_color = list(ending_color)
    current = starting_color
    while current != [0, 0, 0]:
        screen.fill(tuple(current))
        pygame.display.update()
        for i in range(len(current)):
            if current[i] > 0:
                current[i] -= 1
    while current != ending_color:
        screen.fill(tuple(current))
        pygame.display.update()
        for i in range(len(current)):
            if current[i] < ending_color[i]:
                current[i] += 1

class Button:

    def __init__(self, Surface: pygame.Surface, Rect: pygame.Rect, Text: str, Font: pygame.font.Font):
        self.screen = Surface
        self.rect = Rect
        self.text = Text
        self.font = Font

    def Under(self, clicked_pos: tuple) -> bool:
        if clicked_pos[0] >= self.rect.x and clicked_pos[0] <= self.rect.right and\
            clicked_pos[1] >= self.rect.y and clicked_pos[1] <= self.rect.bottom:
            return True
        return False

    def Draw(self, Rect_color: tuple, Text_color: tuple, bg: tuple = 0, width: int = 0, border_radius: int = -1):
        text = self.font.render(self.text, 1, Text_color)
        if bg != 0:
            pygame.draw.rect(self.screen, bg, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0, border_radius)
        pygame.draw.rect(self.screen, Rect_color, self.rect, width, border_radius)
        self.screen.blit(text, (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2))
