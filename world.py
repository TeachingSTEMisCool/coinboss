import pygame
import random
from settings import *
from floor import Floor
from detail import Detail
from player import Player
from coin import Coin
from enemy import Enemy
from boss import Boss

pygame.font.init()
font = pygame.font.Font('assets/Ui/Font/NormalFont.ttf', 32)

class World:
    def __init__(self, floor_data, detail_data, screen):
        self.screen = screen
        self.floor_data = floor_data
        self.detail_data = detail_data
        self.num_coins = 10
        self.game_length = 30
        self.time_left = self.game_length
        self._setup_floor(self.floor_data)
        self._setup_details(self.detail_data)
        # self._spawn_boss(200, 200)
        self.game_over = False
        self.frames = 0

    def _setup_floor(self, data):
        self.floor_tiles = pygame.sprite.Group()
        for row_index, row in enumerate(data):
            for col_index, tile_num in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                tile = Floor((x, y), tile_size, tile_num)
                self.floor_tiles.add(tile)

    def _setup_details(self, data):
        self.detail_tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(data):
            for col_index, tile_type in enumerate(row):
                if tile_type != None:
                    x, y = col_index * tile_size, row_index * tile_size
                    if tile_type == "P":
                        player = Player((x, y))
                        self.player.add(player)
                    elif tile_type == 'E':
                        enemy = Enemy((x, y))
                        self.enemies.add(enemy)
                    else:
                        tile = Detail((x, y), tile_size, tile_type)
                        self.detail_tiles.add(tile)
        for i in range(self.num_coins):
            self._spawn_coin()

    def _spawn_boss(self, x, y):
        self.boss = pygame.sprite.Group()
        boss = Boss((x, y))
        self.boss.add(boss)

    def _spawn_coin(self):
        # Initial spawn
        row_index = random.randint(0, len(detail_map) - 1)
        col_index = random.randint(0, len(detail_map[row_index]) - 1)
        x, y = row_index * tile_size, col_index * tile_size
        coin = Coin((x, y))
        # Keep moving until not colliding
        while pygame.sprite.spritecollide(coin, self.detail_tiles.sprites(), False) or not (10 < x < WIDTH - (10 + tile_size) and 10 < y < HEIGHT- (10 + tile_size)):
            row_index = random.randint(0, len(detail_map) - 1)
            col_index = random.randint(0, len(detail_map[row_index]) - 1)
            x, y = row_index * tile_size, col_index * tile_size
            coin = Coin((x, y))
        self.coins.add(coin)

    def _coin_collision(self):
        player = self.player.sprite
        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect):
                player.score += 1
                coin.kill()
                self._spawn_coin()

    def _running_update(self, keys):
        self.frames += 1
        self._coin_collision()
        # Draw and update floor tiles
        self.floor_tiles.update()
        self.floor_tiles.draw(self.screen)
        # Draw and update detail tiles
        self.detail_tiles.update()
        self.detail_tiles.draw(self.screen)
        # Update coins
        self.coins.update()
        self.coins.draw(self.screen)
        # Update enemies
        self.enemies.update(self.player.sprite, self.detail_tiles.sprites())
        self.enemies.draw(self.screen)
        # Update boss
        # self.boss.update()
        # self.boss.draw(self.screen)
        # Draw and update player
        self.player.update(WIDTH, HEIGHT, keys, self.enemies.sprites(), self.detail_tiles.sprites())
        self.player.draw(self.screen)
        # Update score
        text = font.render('Score: ' + str(self.player.sprite.score), False, (255, 255, 255))
        self.screen.blit(text, (10, 0))
        # Update timer
        self.time_left = self.game_length - (self.frames // 60)
        text = font.render('Time: ' + str(self.time_left), False, (255, 255, 255))
        self.screen.blit(text, (640, 0))
        if self.time_left == 0:
            self.game_over = True
            self.frames = 0

    def _game_over_update(self, keys):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 110, 420, 220))
        pygame.draw.rect(self.screen, (102, 153, 153), pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 100, 400, 200))
        game_over_font = pygame.font.Font('assets/Ui/Font/NormalFont.ttf', 64)
        text = game_over_font.render('Game Over', False, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 100))
        text = font.render('Score: ' + str(self.player.sprite.score), False, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2))
        restart_font = pygame.font.Font('assets/Ui/Font/NormalFont.ttf', 24)
        text = restart_font.render('Press \'r\' to restart', False, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 + 65))
        if keys[pygame.K_r]:
            self._restart()

    def _restart(self):
        self.floor_tiles.empty()
        self.detail_tiles.empty()
        self.player.empty()
        self.coins.empty()
        self.enemies.empty()
        self.time_left = self.game_length
        self._setup_floor(self.floor_data)
        self._setup_details(self.detail_data)
        self.game_over = False

    def update(self, keys):
        if not self.game_over:
            self._running_update(keys)
        else:
            self._game_over_update(keys)