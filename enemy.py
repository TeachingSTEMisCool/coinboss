import pygame
from support import import_sprite
from settings import WIDTH, HEIGHT
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'walk_down'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1
        self.possible_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        self.dx, self.dy = self._get_new_direction()
        self.direction = 'down'
        self.score = 0
        self.last_move = 0
        self.COOLDOWN = 5000

    def _get_new_direction(self):
        x, y = self.possible_directions[random.randint(0, len(self.possible_directions) - 1)]
        x *= self.speed
        y *= self.speed
        return x, y

    def _import_character_assets(self):
        character_path = 'assets/Actor/Monsters/Slime/SeparateAnims/'
        self.animations = {
            'walk_left': [],
            'walk_right': [],
            'walk_up': [],
            'walk_down': []
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

    def _movement_collision(self, player, tiles):
        # Check for wall collisions
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = -self.dx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx = -self.dx
        if self.rect.top < 0:
            self.rect.top = 0
            self.dy = -self.dy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy = -self.dy

        # Move the enemy
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check for collisions
        for sprite in tiles:
            if sprite.rect.colliderect(self.rect):
                # Horizontal collision
                if self.dx != 0:
                    # Collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        # self.dx = -self.dx
                        self.dx, self.dy = self._get_new_direction()
                    # Collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        # self.dx = -self.dx
                        self.dx, self.dy = self._get_new_direction()
                # Vertical collision
                if self.dy != 0:
                    # Collision on bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        # self.dy = -self.dy
                        self.dx, self.dy = self._get_new_direction()
                    # Collision on top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        # self.dy = -self.dy
                        self.dx, self.dy = self._get_new_direction()

    def update(self, player, tiles):
        self.old_rect = self.rect.copy()
        self._movement_collision(player, tiles)
        self._animate()