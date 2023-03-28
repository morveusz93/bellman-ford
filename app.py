import pygame
from pygame.locals import RESIZABLE
from events_mapper import EVENTS_MAPPER


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1800, 1200
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, RESIZABLE, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        else:
            if _method := EVENTS_MAPPER.get(event.type):
                _method()

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
