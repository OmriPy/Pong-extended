import pygame
import os

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