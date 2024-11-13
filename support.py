from os import walk
from PIL import Image
import pygame

def import_sprite(path):
    surface_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = f'{path}/{image}'
            temp_img = Image.open(full_path)
            width, height = temp_img.size
            img_surface = pygame.image.load(full_path).convert_alpha()
            img_surface = pygame.transform.scale(img_surface, (width * 2, height * 2))
            surface_list.append(img_surface)
    return surface_list