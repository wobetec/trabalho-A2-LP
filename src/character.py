import pygame

class Character(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, start_direction, x_limit, y_limit):
        super().__init__()
        self.start_pos = (start_x, start_y)
        self.start_direction = start_direction
        self.direction = start_direction
        self.image = pygame.Surface((45, 45))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.speed = 3
        self.turns = [False, False, False, False]
        self.x_limit = x_limit
        self.y_limit = y_limit
    
    def base_restart(self, ):
        """
        Método que reinicia o Pacman para a posição e atributos inicias
        """
        self.rect.center = self.start_pos
        self.direction = self.start_direction
    
    def set_turns(self, turns):
        """
        Método que define as direções que o Pacman pode virar.

        Parameters:
            turns (list): Lista de booleanos que define as direções que o Pacman pode virar.
        """
        self.turns = turns
    
    def set_direction(self, direction):
        """
        Método que define a direção do Pacman.

        Parameters:
            direction (int): Direção do Pacman.
        """
        self.direction = direction
    
    def get_center(self, ):
        """
        Método que retorna a posição central do Pacman.

        Returns:
            tuple: Tupla com a posição central do Pacman.
        """
        return self.rect.center

    def get_rect(self, ):
        """Retorna o retângulo do fantasma."""
        return self.rect

    def get_direction(self, ):
        """Retorna a direção do fantasma."""
        return self.direction