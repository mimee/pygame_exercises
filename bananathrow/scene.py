import random
import sys
import pygame
from banana import Banana
from utils import generate_gradient


class Scene(pygame.sprite.Group):
    block_count = 16
    max_block_height = 0.85

    def __init__(self, surface):
        super(Scene, self).__init__()
        self.surface = surface
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.block_rects = []
        self.player_positions = []
        self.banana = None
        self.generate_blocks()
        self.block_fall = self.surface.get_height() / 40
        self.init_background()

    def __str__(self):
        mask = '%%0%dd' % len(str(self.surface.get_height()))
        return ' '.join(mask % v for v in self.get_block_heights())

    def add_player(self, player):
        w, h = self.surface.get_size()
        new_position = random.choice(range(self.block_count))
        while new_position in self.player_positions:
            new_position = random.choice(range(self.block_count))
        self.player_positions.append(new_position)
        block_width = w / self.block_count
        block_rect = self.block_rects[new_position]
        x = block_rect[0] + (block_width - player.size[0]) / 2
        y = h - block_rect[3] - player.size[1]
        player.rect = player.rect.move(x, y)
        self.players.add(player)
        self.add(player)

    def end(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'winner': self.banana.player}))

    def fire_banana(self, player, angle, speed):
        self.banana = Banana(player, angle, speed)
        self.add(self.banana)

    def kill_banana(self):
        self.remove(self.banana)
        self.banana = None

    def get_block_heights(self):
        return [s.image.get_height() for s in self.blocks.sprites()]

    def generate_blocks(self, heights=None):
        w, h = self.surface.get_size()
        block_width = w / self.block_count

        for i, bh in enumerate(heights or self._randomize_blocks()):
            block_height = bh * h
            block = pygame.sprite.Sprite(self, self.blocks)
            block.image = pygame.surface.Surface((block_width, block_height))
            block.rect = block.image.get_rect().move(i * block_width,
                                                     h - block_height)
            block.image.fill((127, 15, 31))
            self.block_rects.append(block.rect)

    def _smooth(self, l, width=1, iterations=5, strength=0.20):
        for _ in range(iterations):
            smooth = []
            for i in range(len(l)):
                v = 0.0
                for j in range(-width, width + 1):
                    v += l[(i + j) % len(l)]
                v /= 2 * width + 1
                smooth.append((v * strength) + (l[i] * (1.0 - strength)))
            l = smooth
        return l

    def _randomize_blocks(self):
        r, m = random.random, self.max_block_height
        return self._smooth([r() * m for i in range(self.block_count)])

    def init_background(self):
        w, h = self.surface.get_size()
        self.background = generate_gradient((63, 95, 127), (195, 195, 255), w, h)
        self.update()

    def update(self):
        self.update_banana()
        self.surface.blit(self.background, (0, 0))
        self.draw(self.surface)
        pygame.time.wait(10)
        sys.stdout.write('.')
        sys.stdout.flush()

    def update_banana(self):
        if self.banana is None:
            return
        banana_x, banana_y = self.banana.update()
        if banana_y > self.surface.get_height() + self.banana.size[1]:
            self.kill_banana()
        collided_blocks = pygame.sprite.spritecollide(self.banana, self.blocks, False)
        if collided_blocks:
            for block in collided_blocks:
                block.rect.top += self.block_fall
                self.kill_banana()
                return
        collided_players = pygame.sprite.spritecollide(self.banana, self.players, False)
        if collided_players:
            for player in collided_players:
                if player == self.banana.player:
                    continue  # Banana cannot harm the shooter
                else:
                    self.end()
