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
        if all_active_nodes := [n for n in self.nodes if n.active]:
            return all_active_nodes[0]

    def get_active_edge(self) -> Optional['Edge']:
        if all_active_edges := [e for e in self.edges if e.active]:
            return all_active_edges[0]

    def update_edge_weight(self, event):
        active_edge = self.get_active_edge()
        if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.toggle_active()
            return
        active_edge.change_weight(event)

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
            self.turn_off_all_active_elements()
            return

        if collide_edge:
            if button == 1:
                collide_edge.toggle_active()
            else:
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
    
    def turn_off_all_active_elements(self):
        for e in self.nodes + self.edges:
            if e.active:
                e.toggle_active()

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
        self.weight = 0

        self.calculate_rotation()
        self.calculate_start_pos()
        self.calculate_end_pos()

        text_pos = self.calculate_midpoint(self.start_pos, self.end_pos)
        self.text = DisplayText(center_pos = text_pos, text=self.get_weight_text())

    def __repr__(self) -> str:
        return f"<Edge connects {self.start_node} - {self.end_node}>"
    
    def get_weight_text(self):
        return f"weight: {self.weight}"

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

    def set_weight(self, w):
        self.weight = w
        self.text.text = self.get_weight_text()

    def calculate_end_pos(self) -> None:
        end_pos = self.end_node.pos
        self.end_pos = (
            end_pos[0] - (NODE_RADIUS + EDGE_ARROW_LENGTH) * math.sin(math.radians(self.rotation)),
            end_pos[1] - (NODE_RADIUS + EDGE_ARROW_LENGTH) * math.cos(math.radians(self.rotation))
        )

    def calculate_midpoint(self, p1, p2):
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rects = self.draw(surface)
        return rects[0].collidepoint(x, y) or rects[1].collidepoint(x, y)
    
    def toggle_active(self) -> None:
        self.active = not self.active
        self.text.toggle_active()

    def change_weight(self, event):
        if event.key == pygame.K_BACKSPACE:
            new_weight = int(str(self.weight)[:-1])
            self.set_weight(new_weight)

        elif event.unicode in ALLOWED_INPUT_KEYS:
            if event.unicode.isdigit():
                new_weight = int(str(self.weight) + event.unicode)
                self.set_weight(new_weight)
            elif event.unicode == "-":
                new_weight = self.toggle_positive_negative_weight(self.weight)
                self.set_weight(new_weight)
            elif event.unicode == "+":
                new_weight = abs(self.weight)
                self.set_weight(new_weight)

    def toggle_positive_negative_weight(self, w):
        if w > 0:
            return -abs(w)
        if w < 0:
            return abs(w)

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
        self.text.draw(surface)
        return (line, polygon)


class DisplayText:
    def __init__(self, center_pos, text) -> None:
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = text
        self.center = center_pos
        self.active = False

    def toggle_active(self) -> None:
        self.active = not self.active

    def draw(self, surface: Surface) -> Rect:
        bg_color = TEXT_BG_COLOR
        if self.active:
            bg_color = TEXT_ACTIVE_BG_COLOR
        text_render = self.font.render(self.text, True, TEXT_COLOR, bg_color)
        textRect = text_render.get_rect()
        textRect.center = self.center
        surface.blit(text_render, textRect)
