import numpy
import pygame


def generate_gradient(from_color, to_color, width, height, horizontal=False):
    channels = []
    a, b = (height, width) if horizontal else (width, height)
    surface = pygame.Surface((1, a))
    for channel in range(3):
        from_value, to_value = from_color[channel], to_color[channel]
        channels.append(numpy.linspace(from_value, to_value, a))
    gradient = pygame.surfarray.map_array(surface,
                                          numpy.dstack(channels))
    pygame.surfarray.blit_array(surface, gradient)
    surface = pygame.transform.scale(surface, (a, b))
    if horizontal:
        surface = pygame.transform.rotate(surface, 90)
    return surface
