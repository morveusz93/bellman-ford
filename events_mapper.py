from pygame.locals import RESIZABLE, VIDEOEXPOSE, VIDEORESIZE
import pygame
from methods import draw_cicrcle


EVENTS_MAPPER = {
    VIDEORESIZE: pygame.display.update,
    VIDEOEXPOSE: pygame.display.update,
    pygame.MOUSEBUTTONUP: draw_cicrcle
}
