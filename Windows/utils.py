import pygame
import os

def join(dirs: list[str]) -> str:
    path = dirs[0]
    for i in range(len(dirs)-1):
        path = os.path.join(path, dirs[i+1])
    return path

def equal(vels: list[int]) -> bool:
    for i in range(len(vels)):
        if vels[i] != vels[0]: return False
    return True

def Transition(screen: pygame.Surface ,starting_color: tuple[int, int, int] | list[int, int, int], ending_color: tuple[int, int, int] | list[int, int, int]):
    starting_color = list(starting_color)
    ending_color = list(ending_color)
    current = starting_color
    while current != [0, 0, 0]:
        for i in range(len(current)):
            if current[i] > 0:
                current[i] -= 1
            else: continue
        screen.fill(tuple(current))
        pygame.display.update()
        pygame.time.delay(2)
    while current != ending_color:
        for i in range(len(current)):
            if current[i] < ending_color[i]:
                current[i] += 1
            else: continue
        screen.fill(tuple(current))
        pygame.display.update()
        pygame.time.delay(2)

def quit():
    pygame.quit()
    pygame.font.quit()
    pygame.display.quit()