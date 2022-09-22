import pygame
import os
from multipledispatch import dispatch

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

def quit():
    pygame.display.quit()
    pygame.font.quit()
    pygame.quit()

def join(dirs: list[str]) -> str:
    path = dirs[0]
    for i in range(len(dirs) - 1):
        path = os.path.join(path, dirs[i+1])
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
