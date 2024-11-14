import pygame
import random
from support import import_sprite

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'jump'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1
        self.dx, self.dy = 0, 0
        self.direction = 'down'
        self.score = 0
        self.last_move = 0
        self.COOLDOWN = 5000

    def _import_character_assets(self):
        character_path = 'assets/Actor/Boss/GiantSlime/SeparateAnims/'
        self.animations = {
            'hit': [],
            'idle': [],
            'jump': []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def _movement_collision(self):
        pass

    def update(self):
        self._animate()