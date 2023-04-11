from pygame.surface import Surface
from pygame.rect import Rect
from settings import HINTS_TEXT_COLOR, BG_COLOR, HINTS_TEXT_SIZE
import pygame

class Instruction:
    def __init__(self) -> None:
        self.start_pos = (20, 20)
        self.font = pygame.font.Font('freesansbold.ttf', HINTS_TEXT_SIZE)

    def get_hints(self) -> 'list[str]':
        return [
            "To dissmiss hints -> press F1",
            "To show it again -> also press F1",
            "To add a vertex -> left click at free space",
            "To remove a vertex -> right click it",
            "To active a vertex -> left click it",
            "To connect two vertices -> active them both",
            "To remove an edge -> right click it",
            "To active an edge -> left click it",
            "To change weight -> active an edge and type new weight with your keybord",
            "To set negative weight -> type weight and press '-'",
            "TO START BELLMAN-FORD ALGORITH -> PRESS 'S' WHEN START VERTEX IS ACTIVE!"
        ]

    def draw(self, surface: Surface) -> Rect:
        text_margin = 5
        for i, hint in enumerate(self.get_hints()):
            text_render = self.font.render(hint, True, HINTS_TEXT_COLOR, BG_COLOR)
            text_rect = text_render.get_rect()
            pos = self.start_pos[0], self.start_pos[1] + (HINTS_TEXT_SIZE + text_margin) * i
            text_rect.topleft = pos
            surface.blit(text_render, text_rect)
