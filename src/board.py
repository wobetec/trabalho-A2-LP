import copy
from math import pi as PI
import pygame
from button import Button
import sys

from utils import load_image

# 0 = empity
# 1 = point
# 2 = fruit
# 3 = vertical wall
# 4 = horizontal wall
# 5 = top right corner
# 6 = top left corner
# 7 = bot left corner
# 8 = bot right corner
# 9 = ghosts gate

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

class Board():
    """Esta classe define o tabuleiro do jogo."""

    AVAILABLE_TILES = [0, 1, 2]
    ENEMIE_AVAILABLE_TILES = [0, 1, 2, 9]

    def __init__(self, board, height, width, box):
        """
        Inicializa a classe Board.

        Parâmetros:
        - board (list): Matriz representando o tabuleiro do jogo.
        - height (int): Altura da janela do jogo.
        - width (int): Largura da janela do jogo.
        - box (dict): Dicionário contendo informações sobre a caixa do jogo.
        """
        self.board = copy.deepcopy(board)
        self.main_color = (0, 0, 255)
        self.height = height
        self.width = width
        self.pixel_height = ((self.height - 50) // 32)
        self.pixel_width = (self.width // 30)
        self.box = pygame.Rect(box["x"], box["y"], box["width"], box["height"])

        self.available_fruits_and_dots = 0
        self.count_fruits_and_dots()
    
    def count_fruits_and_dots(self, ):
        """
        Conta o número de frutas e pontos disponíveis no tabuleiro.
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1 or self.board[i][j] == 2:
                    self.available_fruits_and_dots += 1

    # def draw_stats(self, font, score, screen):
    #     score_text = font.render(f"Pontuação: {score}", True, 'white')
    #     screen.blit(score_text, (10, 920))

    def check_collision_ghost(self, center_x, center_y, dead, in_box, direction):
        """
        Verifica colisões com os fantasmas no tabuleiro.

        Parâmetros:
        - center_x (int): Coordenada x do centro do personagem.
        - center_y (int): Coordenada y do centro do personagem.
        - dead (bool): Indica se o personagem está morto ou não.
        - in_box (bool): Indica se o personagem está dentro ou fora da caixa.
        - direction (int): Direção atual do personagem.

        Retorna:
        Uma lista indicando se há colisão em direções específicas e se o personagem está dentro ou fora da caixa.
        """
        # R, L, U, D
        margin = 15
        turns = [False, False, False, False]
        if 0 < center_x // 30 < 29:
            if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] == 9:
                turns[2] = True
            if self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] < 3 \
                    or (self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[1] = True
            if self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] < 3 \
                    or (self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[0] = True
            if self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                    or (self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[3] = True
            if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                    or (self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[2] = True

            if direction == 2 or direction == 3:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[3] = True
                    if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[2] = True
                if 12 <= center_y % self.pixel_height <= 18:
                    if self.board[center_y // self.pixel_height][(center_x - self.pixel_width) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x - self.pixel_width) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + self.pixel_width) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x + self.pixel_width) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[0] = True

            if direction == 0 or direction == 1:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[3] = True
                    if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[2] = True
                if 12 <= center_y % self.pixel_height <= 18:
                    if self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True
        if self.box.collidepoint(center_x, center_y):
            in_box = True
        else:
            in_box = False
            
        return turns, in_box


    def check_collision_points(self, center_x, center_y, powerup, power_count, score, eaten_ghosts):
        """
        Verifica colisões com os pontos no tabuleiro.

        Parâmetros:
        - center_x (int): Coordenada x do centro do personagem.
        - center_y (int): Coordenada y do centro do personagem.
        - powerup (bool): Indica se há um power-up ativo ou não.
        - power_count (int): Contagem do power-up.
        - score (int): Pontuação atual.
        - eaten_ghosts (list): Lista indicando fantasmas comidos.

        Retorna:
        Atualiza o score, powerups e fantasmas comidos.
        """

        if 0 < center_x < 870:
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 1:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 10
                self.available_fruits_and_dots -= 1
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 2:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 50
                self.available_fruits_and_dots -= 1
                powerup = True
                power_count = 0
                eaten_ghosts = [False, False, False, False]
        return score, powerup, power_count, eaten_ghosts


    def check_postion(self, center_x, center_y, turns, direction):
        """
        Verifica a posição do personagem no tabuleiro e possíveis colisões.

        Parâmetros:
        - center_x (int): Coordenada x do centro do personagem.
        - center_y (int): Coordenada y do centro do personagem.
        - turns (list): Lista de direções permitidas.
        - direction (int): Direção atual do personagem.

        Retorna:
        Uma lista indicando direções permitidas para o movimento.
        """
        turns = [False, False, False, False]
        margin = 15
        # check collisions based on center x and center y of player +/- fudge number
        if center_x // 30 < 29:
            if direction == 0:
                if self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] < 3:
                    turns[1] = True
            if direction == 1:
                if self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] < 3:
                    turns[0] = True
            if direction == 2:
                if self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] < 3:
                    turns[3] = True
            if direction == 3:
                if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] < 3:
                    turns[2] = True

            if direction == 2 or direction == 3:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + margin) // self.pixel_height][center_x // self.pixel_width] < 3:
                        turns[3] = True
                    if self.board[(center_y - margin) // self.pixel_height][center_x // self.pixel_width] < 3:
                        turns[2] = True
                if 12 <= center_y % self.pixel_height <= 18:
                    if self.board[center_y // self.pixel_height][(center_x - self.pixel_width) // self.pixel_width] < 3:
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + self.pixel_width) // self.pixel_width] < 3:
                        turns[0] = True
            if direction == 0 or direction == 1:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + self.pixel_height) // self.pixel_height][center_x // self.pixel_width] < 3:
                        turns[3] = True
                    if self.board[(center_y - self.pixel_height) // self.pixel_height][center_x // self.pixel_width] < 3:
                        turns[2] = True
                if 12 <= center_y % self.pixel_height <= 18:
                    if self.board[center_y // self.pixel_height][(center_x - margin) // self.pixel_width] < 3:
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + margin) // self.pixel_width] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns


    def in_box(self, enemies):
        """
        Verifica se os inimigos estão dentro da caixa no tabuleiro.

        Parâmetros:
        - enemies (dict): Dicionário contendo informações sobre os inimigos.

        Retorna:
        Um dicionário indicando se os inimigos estão dentro da caixa.
        """

        inside = {}
        for key, value in enemies.items():
            inside[key] = self.box.collidepoint(*value)
        return inside
    

    def draw(self, screen):
        """
        Desenha o tabuleiro na tela do jogo.

        Parâmetros:
        - screen (pygame.Surface): Superfície da tela onde o tabuleiro será desenhado.
        """

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + (0.5 * self.pixel_height)), 4)
                if self.board[i][j] == 2 :#and not flicker:
                    pygame.draw.circle(screen, 'white', (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + (0.5 * self.pixel_height)), 10)
                if self.board[i][j] == 3:
                    pygame.draw.line(screen, self.main_color, (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height),
                                    (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + self.pixel_height), 3)
                if self.board[i][j] == 4:
                    pygame.draw.line(screen, self.main_color, (j * self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)),
                                    (j * self.pixel_width + self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), 3)
                if self.board[i][j] == 5:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width - (self.pixel_width * 0.4)) - 2, (i * self.pixel_height + (0.5 * self.pixel_height)), self.pixel_width, self.pixel_height],
                                    0, PI / 2, 3)
                if self.board[i][j] == 6:
                    pygame.draw.arc(screen, self.main_color,
                                    [(j * self.pixel_width + (self.pixel_width * 0.5)), (i * self.pixel_height + (0.5 * self.pixel_height)), self.pixel_width, self.pixel_height], PI / 2, PI, 3)
                if self.board[i][j] == 7:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width + (self.pixel_width * 0.5)), (i * self.pixel_height - (0.4 * self.pixel_height)), self.pixel_width, self.pixel_height], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == 8:
                    pygame.draw.arc(screen, self.main_color,
                                    [(j * self.pixel_width - (self.pixel_width * 0.4)) - 2, (i * self.pixel_height - (0.4 * self.pixel_height)), self.pixel_width, self.pixel_height], 3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)),
                                    (j * self.pixel_width + self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), 3)
    
    gameover_img = load_image("/images/other/endgame.png", 600)
    game_won_img = load_image("/images/other/pinho.jpg", 900)

    def game_over_screen(self, screen, font) :
        
        screen.blit(self.gameover_img, (150, -20))
    
        quit_button = Button(350, 610, 200, 80, gray, "Sair", screen)

        menu_button = Button(350, 510, 200, 80, white, "Menu", screen)
        
        # Loop do gameover screen 

        gameover_state = True

        # Main game loop
        while gameover_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.rect.collidepoint(event.pos):
                        pygame.quit()
                    if menu_button.rect.collidepoint(event.pos):
                        pass                 

            # Draw the quit button
            quit_button.draw()

            # Draw the restart button
            menu_button.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)                 

    def game_won_screen(self, screen, font_big, font, points) :
        
        screen.blit(self.game_won_img, (0, 0))
    
        quit_button = Button(350, 610, 200, 80, gray, "Sair", screen)

        menu_button = Button(350, 510, 200, 80, white, "Menu", screen)
        
        # Loop do gamewon screen 

        gamewon_state = True

        # Main game loop
        while gamewon_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.rect.collidepoint(event.pos):
                        pygame.quit()
                    if menu_button.rect.collidepoint(event.pos):
                        pass                 


            # Você venceu text
        
            vc_venceu_text = font_big.render(f"Você venceu!", True, 'white')
            vc_venceu_text_rect = vc_venceu_text.get_rect()

            # Calculate the position where you want to blit the text
            sizeoftext_x = (screen.get_width() - vc_venceu_text_rect.width) // 2
            sizeoftext_y = (screen.get_height() - vc_venceu_text_rect.height - 300) // 2

            # Blit the text to the screen
            screen.blit(vc_venceu_text, (sizeoftext_x, sizeoftext_y))

            # Sua pontuação text

            pontuacao_text = font.render(f"Sua pontuação: {points}", True, 'white')
            pontuacao_text_rect = pontuacao_text.get_rect()
            
            # Calculate the position where you want to blit the text
            sizeoftext_x_2 = (screen.get_width() - pontuacao_text_rect.width) // 2
            sizeoftext_y_2 = (screen.get_height() - pontuacao_text_rect.height - 200) // 2

            # Blit the text to the screen
            screen.blit(pontuacao_text, (sizeoftext_x_2, sizeoftext_y_2))


            # Draw the quit button
            quit_button.draw()

            # Draw the restart button
            menu_button.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)       
                
        

