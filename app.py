import pygame
from pygame.locals import RESIZABLE, VIDEOEXPOSE, VIDEORESIZE
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, ALLOWED_INPUT_KEYS
from graph import Graph
from pygame.surface import Surface

class App:
    def __init__(self):
        self.size = self.weight, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.clock = pygame.time.Clock()
        self._running = True
        self._display_surf: Surface = None
        self.graph: Graph = None
 
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Graphs algoritms by Morv')
        self._display_surf = pygame.display.set_mode(self.size, RESIZABLE, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.graph = Graph(surface=self._display_surf)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type in (VIDEORESIZE, VIDEOEXPOSE): 
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.graph.check_collide(pos, event.button)
        if event.type == pygame.KEYDOWN  and any([e.active for e in self.graph.edges]):
            self.graph.update_edge_weight(event)

    def on_loop(self):
        self.clock.tick(FPS)

    def on_render(self):
        self._display_surf.fill('grey')
        self.graph.draw()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
