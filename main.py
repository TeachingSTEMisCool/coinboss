import pygame, sys
from settings import *
from world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class CoinBoss:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.keys = None

    def play(self):
        world = World(floor_map, detail_map, self.screen)
        while True:
            for event in pygame.event.get():
                # Check to see if the user quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Get pressed keys
            self.keys = pygame.key.get_pressed()
    
            world.update(self.keys)
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    cb = CoinBoss(screen, WIDTH, HEIGHT)
    cb.play()