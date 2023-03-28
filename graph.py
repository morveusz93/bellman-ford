from pygame.surface import Surface
from pygame.rect import Rect
import pygame
from settings import *


class Graph:
    def __init__(self) -> None:
        self.nodes: 'list[Node]' = []

    def create_node(self, pos: 'tuple[int]'):
        new_node = Node(pos)
        self.nodes.append(new_node)

    def check_collide(self, pos: 'tuple[int]', surface: Surface):
        for node in self.nodes:
            if node.collidepoint(*pos, surface):
                self.nodes.remove(node)
                del node
                return

    def draw(self, surface: Surface):
        for node in self.nodes:
            node.draw(surface)


class Node:
    def __init__(self, pos: 'tuple[int]') -> None:
        self.pos = pos

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rect = self.draw(surface)
        return rect.collidepoint(x, y)

    
    def draw(self, surface: Surface) -> Rect:
        return pygame.draw.circle(surface, NODE_COLOR, self.pos, NODE_RADIUS)


class Edge:
    pass