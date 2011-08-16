import sys
import pygame
from player import Player
from scene import Scene


SURFACE_PROPERTIES = pygame.DOUBLEBUF | pygame.HWSURFACE  # | pygame.FULLSCREEN


class Game(object):
    class Quit(Exception):
        pass

    class Kill(Exception):
        pass

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.window = pygame.display.set_mode((320, 240), SURFACE_PROPERTIES)
        self.scene = self.setup_scene()
        self.end_game_score = 2

    def setup_scene(self):
        scene = Scene(self.window)
        scene.add_player(self.player1)
        scene.add_player(self.player2)
        return scene

    def run(self):
        self.scene.fire_banana(self.player1, 60, 20)
        while max(self.player1.score, self.player2.score) < self.end_game_score:
            try:
                self.tick()
            except Game.Kill:
                self.scene = self.setup_scene()
                continue
            except Game.Quit:
                sys.stdout.write("Quit\n")
                sys.stdout.flush()
                break

    def tick(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise Game.Quit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    raise Game.Quit
            if e.type == pygame.USEREVENT and hasattr(e, 'winner'):
                e.winner.score += 1
                sys.stdout.write("Kill by %r" % e.winner)
                sys.stdout.flush()
                raise Game.Kill
        self.scene.update()
        pygame.display.flip()
