import unittest
import pygame
from player import Player
from scene import Scene


class SceneTestCase(unittest.TestCase):
    def get_surface(self):
        return pygame.Surface((800, 600))

    def test_smooth(self):
        scene = Scene(self.get_surface())
        s = scene._smooth([0, 1, 0], iterations=2, strength=0.5, width=1)
        self.assertAlmostEqual(s[0], 0.25)
        self.assertAlmostEqual(s[1], 0.50)
        self.assertAlmostEqual(s[2], 0.25)
        s = scene._smooth([0, 0, 1, 0, 0], iterations=1, strength=0.1, width=2)
        self.assertAlmostEqual(s[0], 0.02)
        self.assertAlmostEqual(s[1], 0.02)
        self.assertAlmostEqual(s[2], 0.92)
        self.assertAlmostEqual(s[3], 0.02)
        self.assertAlmostEqual(s[4], 0.02)

    def test_generated_block_heights_are_within_limits(self):
        scene = Scene(self.get_surface())
        h_max = scene.max_block_height * 600
        # The initializer should have generated block heights
        # but we will randomize a few more times just to be sure.
        for _ in range(100):
            for h in scene.get_block_heights():
                self.assert_(h >= 0.0)
                self.assert_(h <= h_max)
            scene.generate_blocks()

    def test_each_player_is_positioned_on_a_different_block(self):
        scene = Scene(self.get_surface())
        # Add as many player as the number of blocks scene has
        for player in [Player() for _ in range(scene.block_count)]:
            scene.add_player(player)
        self.assertEqual(len(scene.player_positions), scene.block_count)
        self.assertEqual(len(set(scene.player_positions)), scene.block_count)


if __name__ == '__main__':
    unittest.main()
