"""
Define a classe de jogador utilizada no game.
"""
import pygame
from utils import load_image, load_sound
from math import floor, ceil
from character import Character

class Player(Character):
    """
    Classe que herda de Character. Implementa a movimentação e renderização do Pacman.
    """

    def __init__(self, start_x, start_y, start_direction, x_limit, y_limit):
        """
        Instanciador da classe Player.

        Parameters:
            start_x (int): Posição inicial do Pacman no eixo x.
            start_y (int): Posição inicial do Pacman no eixo y.
            start_direction (int): Direção inicial do Pacman. 0-Direita, 1-Esquerda, 2-Cima, 3-Baixo.
            x_limit (int): Limite do eixo x.
            y_limit (int): Limite do eixo y.
        """
        super().__init__(start_x, start_y, start_direction, x_limit, y_limit)

        self.images = []
        for i in range(1, 5):
            name = f"/images/pacman/{i}.png"
            self.images.append(load_image(name))
        self.sounds = {}

        self.counter = 0


    def set_image(self, ):
        """
        Define a imagem do Pacman de acordo com a direção e o contador.
        """
        image = self.images[floor(self.counter)]
        pos =  (0 ,0)

        pygame.draw.circle(self.image, (0, 0, 0), (45/2, 45/2), ceil(45/2)+1)
        if self.direction == 0:
            self.image.blit(image, pos)
        elif self.direction == 1:
            self.image.blit(pygame.transform.flip(image, True, False), pos)
        elif self.direction == 2:
            self.image.blit(pygame.transform.rotate(image, 90), pos)
        elif self.direction == 3:
            self.image.blit(pygame.transform.rotate(image, 270), pos)

    def get_input(self, ):
        """
        Método que define a direção do Pacman de acordo com as teclas pressionadas.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.turns[0]:
            self.direction = 0
        elif keys[pygame.K_a] and self.turns[1]:
            self.direction = 1
        elif keys[pygame.K_w] and self.turns[2]:
            self.direction = 2
        elif keys[pygame.K_s] and self.turns[3]:
            self.direction = 3

    def move(self, ):
        """
        Define a movimentação do Pacman de acordo com a direção que ele está.
        """

        if self.direction == 0 and self.turns[0]:
            self.rect.x += self.speed
        elif self.direction == 1 and self.turns[1]:
            self.rect.x -= self.speed
        elif self.direction == 2 and self.turns[2]:
            self.rect.y -= self.speed
        elif self.direction == 3 and self.turns[3]:
            self.rect.y += self.speed
        
        if self.rect.x > self.x_limit:
            self.rect.x = -25
        elif self.rect.x < -50:
            self.rect.x = self.x_limit - 10

        if self.rect.y > self.y_limit:
            self.rect.y = -25
        elif self.rect.y < -50:
            self.rect.y = self.y_limit - 10
        
    def restart(self, ):
        """
        Método que reinicia o Pacman para a posição inicial.
        """
        self.base_restart()

    
    def update(self, ):
        """
        Sobrescrevendo o método update da classe Sprite. Define a imagem do Pacman de acordo com a direção e o contador.

        Parameters:
        
        Returns:
        """
        self.counter = (self.counter + 0.15)%4
        self.set_image()
        pass