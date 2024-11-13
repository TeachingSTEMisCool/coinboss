import pygame

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile_num):
        super().__init__()
        img_path = f'assets/Backgrounds/Tilesets/Floor/tile{tile_num}.png'
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass