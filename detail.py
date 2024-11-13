import pygame
from PIL import Image

class Detail(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile_type):
        super().__init__()
        img_path = f'assets/Backgrounds/Tilesets/Detail/{tile_type}.png'
        temp_img = Image.open(img_path)
        width, height = temp_img.size
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (2 * width, 2 * height))
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect

    def update(self):
        self.old_rect = self.rect.copy()