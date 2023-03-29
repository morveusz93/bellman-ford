from pygame.surface import Surface
from pygame.rect import Rect
import pygame
from settings import *


class Graph:
    def __init__(self) -> None:
        self.nodes: 'list[Node]' = []
        self.nodes_rects: 'list[Rect]' = []

    def create_node(self, pos: 'tuple[int, int]'):
        new_node = Node(pos)
        self.nodes.append(new_node)

    def check_collide(self, pos: 'tuple[int, int]', surface: Surface):
        # if the circles are overlapped, we want to remove the lateset one (appened to list later)
        for node in self.nodes[::-1]:
            if node.collidepoint(*pos, surface):
                return node

    def draw(self, surface: Surface):
        self.nodes_rects = []
        for node in self.nodes:
            rect = node.draw(surface)
            self.nodes_rects.append(rect)


class Node:
    def __init__(self, pos: 'tuple[int, int]') -> None:
        self.pos = pos
        self.active = False

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rect = self.draw(surface)
        return rect.collidepoint(x, y)
 
    def toggle_active(self):
        self.active = not self.active
 
    def draw(self, surface: Surface) -> Rect:
        color = NODE_COLOR
        if self.active:
            color = NODE_ACTIVE_COLOR
        pygame.draw.circle(surface, NODE_BORDER_COLOR, self.pos, NODE_RADIUS + NODE_BORDER_WIDTH, width=NODE_BORDER_WIDTH)
        return pygame.draw.circle(surface, color, self.pos, NODE_RADIUS)


class Edge:
    pass