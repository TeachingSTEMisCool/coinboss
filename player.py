import pygame
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.dx, self.dy = 0, 0
        self.direction = 'down'
        self.score = 0
        self.is_attacking = False
        self.last_attack = 0
        self.attack_cooldown = 1000

    def _import_character_assets(self):
        character_path = 'assets/Actor/Characters/Knight/SeparateAnim/'
        self.animations = {
            'attack_left': [],
            'attack_right': [],
            'attack_up': [],
            'attack_down': [],
            'dead': [],
            'idle': [],
            'item': [],
            'jump': [],
            'special1': [],
            'special2': [],
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
            if self.is_attacking:
                self.is_attacking = False
                self.status = 'idle'
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def _get_status(self):
        if self.dx < 0:
            self.status = 'walk_left'
        elif self.dx > 0:
            self.status = 'walk_right'
        elif self.dy < 0:
            self.status = 'walk_up'
        elif self.dy > 0:
            self.status = 'walk_down'
        else:
            self.status = 'idle'
    
    def _movement_collision(self, width, height, keys, enemies, tiles):
        self.dx, self.dy = 0, 0
        if keys[pygame.K_UP]:
            self.dy = -self.speed
        if keys[pygame.K_DOWN]:
            self.dy = self.speed
        if keys[pygame.K_LEFT]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.dx = self.speed
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if not self.is_attacking and current_time - self.last_attack > self.attack_cooldown:
                self.is_attacking = True
                self.status = 'attack_down'
                if self.dy > 0:
                    self.status = 'attack_down'
                if self.dy < 0:
                    self.status = 'attack_up'
                if self.dx < 0:
                    self.status = 'attack_left'
                if self.dx > 0:
                    self.status = 'attack_right'
                self.last_attack = current_time
                
        # Move the player
        if not self.is_attacking:
            self.rect.x += self.dx
            self.rect.y += self.dy

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

        # Check for collisions with details
        for sprite in tiles:
            if sprite.rect.colliderect(self.rect):
                # Horizontal collision
                if self.dx != 0:
                    # Collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    # Collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                # Vertical collision
                if self.dy != 0:
                    # Collision on bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    # Collision on top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

        # Check for collisions with enemies
        if self.is_attacking:
            for sprite in enemies:
                if self.rect.colliderect(sprite.rect):
                    sprite.kill()

    def update(self, width, height, keys, enemies, tiles):
        self.old_rect = self.rect.copy()
        self._movement_collision(width, height, keys, enemies, tiles)
        if not self.is_attacking:
            self._get_status()
        self._animate()