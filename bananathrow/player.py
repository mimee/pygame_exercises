import pygame


class Player(pygame.sprite.Sprite):
    color = (255, 128, 64)
    size = (8, 24)

    def __init__(self, *args, **kwargs):
        color = kwargs.pop("color", Player.color)
        size = kwargs.pop("size", Player.size)
        super(Player, self).__init__(*args, **kwargs)
        self.color = color
        self.size = size
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect()
        self.image.fill(self.color)
        self.score = 0


class AIPlayer(Player):
    pass
