import pygame
from support import import_sprite

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect
        self.mask = pygame.mask.from_surface(self.image)

    def _import_character_assets(self):
        character_path = 'assets/Items/Treasure/Coin'
        self.animations = import_sprite(character_path)

    def _animate(self):
        animation = self.animations
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def update(self):
        self._animate()