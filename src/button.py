import pygame
import sys

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Define Button class
class QuitButton:
    def __init__(self, x, y, width, height, color, text, screen):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        text = self.font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

