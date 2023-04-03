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

    def get_active_node(self) -> Optional['Node']:
        if all_nodes := [n for n in self.nodes if n.active]:
            return all_nodes[0]

    def create_node(self, pos: 'tuple[int, int]') -> None:
        new_node = Node(pos)
        self.nodes.append(new_node)

    def create_edge(self, start: 'Node', end: 'Node') -> None:
        new_edge = Edge(start, end)
        self.edges.append(new_edge)
            
    def check_collide(self, pos: 'tuple[int, int]', button: int):
        collide_edge = self.check_collide_object(self.edges, pos)
        collide_node = self.check_collide_object(self.nodes[::-1], pos)
        
        if not any ((collide_edge, collide_node)):
            self.create_node(pos)
            return

        if collide_edge:
            if button != 1:
                self.edges.remove(collide_edge)
                return

        if collide_node:
            if button == 1:
                self.connect_or_toggle_node(collide_node)
            else:
                self.nodes.remove(collide_node)
                self.remove_edges_connected_to_node(collide_node)
        
    def remove_edges_connected_to_node(self, node):
        self.edges = list(filter(lambda e: node not in (e.start_node, e.end_node), self.edges))

    def check_collide_object(self, objects_list, pos):
        for obj in objects_list:
            if obj.collidepoint(*pos, self.surface):
                return obj
        return None
    
    def connect_or_toggle_node(self, clicked_node: 'Node') -> None:
        if active_node := self.get_active_node():
            self.connect_nodes(start_node=active_node, end_node=clicked_node)
        else:
            clicked_node.toggle_active()

    def connect_nodes(self, end_node: 'Node', start_node: 'Node') -> None:
        if self.are_nodes_already_connected(start_node, end_node):
            return
        if start_node != end_node:
            self.create_edge(start=start_node, end=end_node)
        start_node.toggle_active()

    def are_nodes_already_connected(self, start_node, end_node):
        for e in self.edges:
            if e.start_node == start_node or e.start_node == end_node:
                if e.end_node == start_node or e.end_node == end_node:
                    return True
        return False

    def draw(self) -> None:
        for obj in self.nodes + self.edges:
            obj.draw(self.surface)


class Node:
    def __init__(self, pos: 'tuple[int, int]') -> None:
        self.pos = pos
        self.active = False

    def __repr__(self) -> str:
        return f"<Node in {self.pos}>"

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

    def __repr__(self) -> str:
        return f"<Edge connects {self.start_node} - {self.end_node}>"

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

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rects = self.draw(surface)
        return rects[0].collidepoint(x, y) or rects[1].collidepoint(x, y)
 
    def draw(self, surface: Surface) -> 'tuple[Rect, Rect]':
        color = EDGE_COLOR
        if self.active:
            color = EDGE_ACTIVE_COLOR
        line = pygame.draw.line(
            surface, 
            color, 
            self.start_pos,
            self.end_pos,
            width=EDGE_WIDTH
        )
        polygon = pygame.draw.polygon(
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
        return (line, polygon)
