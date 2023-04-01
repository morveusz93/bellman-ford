import math
from pygame.surface import Surface
from pygame.rect import Rect
import pygame
from settings import *
from typing import Optional

class Graph:
    def __init__(self, surface: Surface) -> None:
        self.nodes: 'list[Node]' = []
        self.edges: 'list[Edge]' = []
        self.surface = surface
    
    @property
    def any_active_node(self) -> bool:
        return any([n.active for n in self.nodes])

    def get_active_node(self) -> Optional['Node']:
        return [n for n in self.nodes if n.active][0] if self.any_active_node else None

    def create_node(self, pos: 'tuple[int, int]') -> None:
        new_node = Node(pos)
        self.nodes.append(new_node)

    def create_edge(self, start: 'Node', end: 'Node') -> None:
        new_edge = Edge(start, end)
        self.edges.append(new_edge)

    def check_collide(self, pos: 'tuple[int, int]') -> 'Optional[Node]':
        # if the circles are overlapped, we want to remove the lateset one (appened to list later)
        for node in self.nodes[::-1]:
            if node.collidepoint(*pos, self.surface):
                return node

    def connect_nodes(self, end_node) -> None:
        start_node = self.get_active_node()
        if start_node != end_node:
            self.create_edge(start=start_node, end=end_node)
        start_node.toggle_active()

    def draw(self) -> None:
        for obj in self.nodes + self.edges:
            obj.draw(self.surface)


class Node:
    def __init__(self, pos: 'tuple[int, int]') -> None:
        self.pos = pos
        self.active = False

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rect = self.draw(surface)
        return rect.collidepoint(x, y)
 
    def toggle_active(self) -> None:
        self.active = not self.active
 
    def draw(self, surface: Surface) -> Rect:
        color = NODE_COLOR
        if self.active:
            color = NODE_ACTIVE_COLOR
        pygame.draw.circle(surface, NODE_BORDER_COLOR, self.pos, NODE_RADIUS + NODE_BORDER_WIDTH, width=NODE_BORDER_WIDTH)
        return pygame.draw.circle(surface, color, self.pos, NODE_RADIUS)


class Edge:
    def __init__(self, start: 'Node', end: 'Node') -> None:
        self.start_node = start
        self.end_node = end
        self.active = False
        self.calculate_rotation()
        self.calculate_start_pos()
        self.calculate_end_pos()

    def calculate_rotation(self) -> None:
        start_pos = self.start_node.pos
        end_pos = self.end_node.pos
        self.rotation = math.degrees(math.atan2(start_pos[1] - end_pos[1], end_pos[0] - start_pos[0])) + 90

    def calculate_start_pos(self) -> None:
        start_pos = self.start_node.pos
        self.start_pos = (
            start_pos[0] + NODE_RADIUS * math.sin(math.radians(self.rotation)), 
            start_pos[1] + NODE_RADIUS * math.cos(math.radians(self.rotation))
        )

    def calculate_end_pos(self) -> None:
        end_pos = self.end_node.pos
        self.end_pos = (
            end_pos[0] - (NODE_RADIUS + EDGE_ARROW_LENGTH) * math.sin(math.radians(self.rotation)),
            end_pos[1] - (NODE_RADIUS + EDGE_ARROW_LENGTH) * math.cos(math.radians(self.rotation))
        )

    def draw(self, surface: Surface) -> None:
        color = EDGE_COLOR
        if self.active:
            color = EDGE_ACTIVE_COLOR
        pygame.draw.line(
            surface, 
            color, 
            self.start_pos,
            self.end_pos,
            width=EDGE_WIDTH
        )
        pygame.draw.polygon(
            surface, 
            color, 
            ((
                self.end_pos[0] + EDGE_ARROW_LENGTH * math.sin(math.radians(self.rotation)), 
                self.end_pos[1] + EDGE_ARROW_LENGTH * math.cos(math.radians(self.rotation))
            ), 
             (
                self.end_pos[0] + EDGE_ARROW_LENGTH * math.sin(math.radians(self.rotation - EDGE_ARROW_ANGLE)), 
                self.end_pos[1] + EDGE_ARROW_LENGTH * math.cos(math.radians(self.rotation - EDGE_ARROW_ANGLE))
            ), 
             (
                self.end_pos[0] + EDGE_ARROW_LENGTH * math.sin(math.radians(self.rotation + EDGE_ARROW_ANGLE)), 
                self.end_pos[1] + EDGE_ARROW_LENGTH * math.cos(math.radians(self.rotation + EDGE_ARROW_ANGLE)))
            )
            )

class NodeConnection:
    def __init__(self, start, end) -> None:
        self.start_node = start
        self.end_node = end
        self.price = 0
