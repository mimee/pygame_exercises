import math
import time
import pygame
import pygame.gfxdraw


class Banana(pygame.sprite.Sprite):
    gravity = -9.81  # m/s2
    size = (16 ,16)
    color = (127, 196, 127, 255)
    scale_factor = 4  # px/m

    def __init__(self, player, angle, speed):
        super(Banana, self).__init__()
        self.player = player
        self.angle = angle * math.pi / 180  # converted to radians
        self.speed = speed # m/s
        self.vector = (self.speed * math.cos(self.angle),
                       self.speed * math.sin(self.angle))
        self.last_update = pygame.time.get_ticks()
        self.image = pygame.surface.Surface(self.size)
        self.image = pygame.surface.Surface.convert_alpha(self.image)
        x, y = self.player.rect.midtop
        x -= self.size[0] / 2
        y -= self.size[1]
        self.x, self.y = x, y
        self.rect = self.image.get_rect().move(x, y)
        self.update()

    def render(self):
        r = self.size[0] / 2 - 2
        x = y = r + 2
        self.image.fill((0, 0, 0, 0))
        pygame.gfxdraw.filled_circle(self.image, x, y, r, self.color)

    def update(self):
        ticks = pygame.time.get_ticks()
        timediff = float(ticks - self.last_update) / 1000  # sn
        vx, vy = self.vector
        self.vector = (vx, vy + self.gravity * timediff)
        dx, dy = self.vector
        self.x += dx * timediff * self.scale_factor
        self.y += -dy * timediff * self.scale_factor
        self.rect.topleft = int(self.x), int(self.y)
        self.last_update = ticks
        self.render()
        return self.x, self.y
