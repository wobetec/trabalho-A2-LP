"""
Define a classe base para criação dos personagens do jogo.
"""
import pygame

class Character(pygame.sprite.Sprite):
    """
    Classe base para criação dos personagens do jogo.
    """

    def __init__(self, start_x, start_y, start_direction, x_limit, y_limit):
        """
        Construtor da classe Character.

        Parameters:
            start_x (int): Posição inicial no eixo x.
            start_y (int): Posição inicial no eixo y.
            start_direction (int): Direção inicial.
            x_limit (int): Limite do eixo x.
            y_limit (int): Limite do eixo y.
        """
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
        Método que reinicia o personagem para a posição inicial.
        """
        self.rect.center = self.start_pos
        self.direction = self.start_direction
    
    def set_turns(self, turns):
        """
        Define as direções que o personagem pode virar.

        Parameters:
            turns (list): Lista de booleanos que define as direções para virar.
        """
        self.turns = turns
    
    def set_direction(self, direction):
        """
        Define a direção do personagem.

        Parameters:
            direction (int): Direção do personagem.
        """
        self.direction = direction
    
    def get_center(self, ):
        """
        Retorna a posição central do personagem.

        Returns:
            tuple: Tupla com a posição central do personagem.
        """
        return self.rect.center

    def get_rect(self, ):
        """Retorna o retângulo do personagem."""
        return self.rect

    def get_direction(self, ):
        """Retorna a direção do direção do personagem."""
        return self.direction