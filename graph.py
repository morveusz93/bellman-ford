import math
from pygame.surface import Surface
from pygame.rect import Rect
import pygame
from settings import *
from typing import Optional

class Graph:
    def __init__(self, surface: Surface) -> None:
        self.vertices: 'list[Vertex]' = []
        self.edges: 'list[Edge]' = []
        self.surface = surface

    def get_active_vertex(self) -> Optional['Vertex']:
        if all_active_vertices := [n for n in self.vertices if n.active]:
            return all_active_vertices[0]

    def get_active_edge(self) -> Optional['Edge']:
        if all_active_edges := [e for e in self.edges if e.active]:
            return all_active_edges[0]

    def update_edge_weight(self, event):
        active_edge = self.get_active_edge()
        if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            active_edge.toggle_active()
            return
        active_edge.change_weight(event)

    def create_vertex(self, pos: 'tuple[int, int]') -> None:
        new_vertex = Vertex(pos)
        self.vertices.append(new_vertex)

    def create_edge(self, start: 'Vertex', end: 'Vertex') -> None:
        new_edge = Edge(start, end)
        self.edges.append(new_edge)
            
    def check_collide(self, pos: 'tuple[int, int]', button: int):
        collide_edge = self.check_collide_object(self.edges, pos)
        collide_vertex = self.check_collide_object(self.vertices[::-1], pos)
        
        if not any ((collide_edge, collide_vertex)):
            self.create_vertex(pos)
            self.turn_off_all_active_elements()
            return

        if collide_edge:
            if button == 1:
                if active_edge := self.get_active_edge():
                    active_edge.toggle_active()
                collide_edge.toggle_active()
            else:
                self.edges.remove(collide_edge)
                return

        if collide_vertex:
            if button == 1:
                self.connect_or_toggle_vertex(collide_vertex)
            else:
                self.vertices.remove(collide_vertex)
                self.remove_edges_connected_to_vertex(collide_vertex)
        
    def remove_edges_connected_to_vertex(self, vertex):
        self.edges = list(filter(lambda e: vertex not in (e.start_vertex, e.end_vertex), self.edges))

    def check_collide_object(self, objects_list, pos):
        for obj in objects_list:
            if obj.collidepoint(*pos, self.surface):
                return obj
        return None
    
    def connect_or_toggle_vertex(self, clicked_vertex: 'Vertex') -> None:
        if active_vertex := self.get_active_vertex():
            self.connect_vertices(start_vertex=active_vertex, end_vertex=clicked_vertex)
        else:
            clicked_vertex.toggle_active()

    def connect_vertices(self, end_vertex: 'Vertex', start_vertex: 'Vertex') -> None:
        if self.are_vertices_already_connected(start_vertex, end_vertex):
            return
        if start_vertex != end_vertex:
            self.create_edge(start=start_vertex, end=end_vertex)
        start_vertex.toggle_active()

    def are_vertices_already_connected(self, start_vertex, end_vertex):
        for e in self.edges:
            if e.start_vertex == start_vertex or e.start_vertex == end_vertex:
                if e.end_vertex == start_vertex or e.end_vertex == end_vertex:
                    return True
        return False
    
    def turn_off_all_active_elements(self):
        for e in self.vertices + self.edges:
            if e.active:
                e.toggle_active()

    def draw(self) -> None:
        for obj in self.vertices + self.edges:
            obj.draw(self.surface)


class Vertex:
    def __init__(self, pos: 'tuple[int, int]') -> None:
        self.pos = pos
        self.active = False
        self.text = DisplayText(center_pos=pos, text="")

    def __repr__(self) -> str:
        return f"<Vertex in {self.pos}>"

    def collidepoint(self, x: int, y: int,  surface: Surface) -> bool:
        rect = self.draw(surface)
        return rect.collidepoint(x, y)
 
    def toggle_active(self) -> None:
        self.active = not self.active
 
    def draw(self, surface: Surface) -> Rect:
        color = VERTEX_COLOR
        if self.active:
            color = VERTEX_ACTIVE_COLOR
        pygame.draw.circle(surface, VERTEX_BORDER_COLOR, self.pos, VERTEX_RADIUS + VERTEX_BORDER_WIDTH, width=VERTEX_BORDER_WIDTH)
        circle = pygame.draw.circle(surface, color, self.pos, VERTEX_RADIUS)
        self.text.draw(surface, bg_color=color)
        return circle


class Edge:
    def __init__(self, start: 'Vertex', end: 'Vertex') -> None:
        self.start_vertex = start
        self.end_vertex = end
        self.active = False
        self.weight = 0

        self.calculate_rotation()
        self.calculate_start_pos()
        self.calculate_end_pos()

        text_pos = self.calculate_midpoint(self.start_pos, self.end_pos)
        self.text = DisplayText(center_pos = text_pos, text=self.get_weight_text())

    def __repr__(self) -> str:
        return f"<Edge connects {self.start_vertex} - {self.end_vertex}>"
    
    def get_weight_text(self):
        return f"weight: {self.weight}"

    def calculate_rotation(self) -> None:
        start_pos = self.start_vertex.pos
        end_pos = self.end_vertex.pos
        self.rotation = math.degrees(math.atan2(start_pos[1] - end_pos[1], end_pos[0] - start_pos[0])) + 90

    def calculate_start_pos(self) -> None:
        start_pos = self.start_vertex.pos
        self.start_pos = (
            start_pos[0] + VERTEX_RADIUS * math.sin(math.radians(self.rotation)), 
            start_pos[1] + VERTEX_RADIUS * math.cos(math.radians(self.rotation))
        )

    def set_weight(self, w):
        self.weight = w
        self.text.text = self.get_weight_text()

    def calculate_end_pos(self) -> None:
        end_pos = self.end_vertex.pos
        self.end_pos = (
            end_pos[0] - (VERTEX_RADIUS + EDGE_ARROW_LENGTH) * math.sin(math.radians(self.rotation)),
            end_pos[1] - (VERTEX_RADIUS + EDGE_ARROW_LENGTH) * math.cos(math.radians(self.rotation))
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
        new_weight = None
        if event.key == pygame.K_BACKSPACE:
            str_weight = str(self.weight)
            if len(str_weight) == 1 or (len(str_weight) == 2 and str_weight.startswith("-")):
                new_weight = 0
            else:
                new_weight = int(str(self.weight)[:-1])

        elif event.unicode in ALLOWED_INPUT_KEYS:
            if event.unicode.isdigit():
                new_weight = int(str(self.weight) + event.unicode)
            elif event.unicode == "-":
                new_weight = self.toggle_positive_negative_weight(self.weight)
            elif event.unicode == "+":
                new_weight = abs(self.weight)
        if new_weight is not None:
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

    def draw(self, surface: Surface, bg_color=None) -> Rect:
        if not bg_color:
            bg_color = TEXT_BG_COLOR if not self.active else TEXT_ACTIVE_BG_COLOR
        text_render = self.font.render(self.text, True, TEXT_COLOR, bg_color)
        textRect = text_render.get_rect()
        textRect.center = self.center
        surface.blit(text_render, textRect)
