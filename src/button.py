import pygame
import sys

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Define Button class
class Button:

    """Esta classe cria os botões das telas finais do jogo."""
    
    def __init__(self, x, y, width, height, color, text, screen):
        """
        Inicializa a classe Button.

        Parâmetros:
        - x (list): Largura do botão.
        - y (int): Altura do botão.
        - width (int): Largura do botão.
        - height (int): Altura do botão.
        - color (tuple): Cor do botão
        - box (dict): Dicionário contendo informações sobre a caixa do jogo.
        """
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        """
        Desenha o botão na tela.

        Parâmetros:

        Returns:
            pygame.Surface: Uma superfície contendo a imagem carregada e redimensionada

        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        text = self.font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

