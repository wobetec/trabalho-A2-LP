import pygame

class Character(pygame.sprite.Sprite):


    def __init__(self, start_x, start_y, start_direction):
        super().__init__()
        self.start_pos = (start_x, start_y)
        self.start_direction = start_direction
        self.direction = start_direction
        self.image = pygame.Surface((45, 45))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.speed = 3
        self.turns = [False, False, False, False]