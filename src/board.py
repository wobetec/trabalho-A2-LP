import copy
from math import pi as PI
import pygame
from button import QuitButton
import sys

from utils import load_image, load_sound

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

    BLINK_RATE = 10 # frames
    MARGIN = 15

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
        self.blink = 0

        self.available_fruits_and_dots = 0
        self.count_fruits_and_dots()

        self.sounds= {
            "fruit": load_sound("eatfruit"),
            "dot": load_sound("chomp"),
        }
    
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

    def get_turns_ghost(self, ghost):
        """
        Verifica colisões com os fantasmas no tabuleiro.

        Parâmetros:

        Retorna:
        Uma lista indicando se há colisão em direções específicas e se o personagem está dentro ou fora da caixa.
        """
        center_x, center_y = ghost.get_center()
        dead = ghost.is_dead()
        in_box = ghost.is_in_box()
        direction = ghost.get_direction()
        
        
        turns = [False, False, False, False]
        if 0 < center_x // 30 < 29:
            if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9:
                turns[2] = True
            if self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] < 3 \
                    or (self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[1] = True
            if self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] < 3 \
                    or (self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[0] = True
            if self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                    or (self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[3] = True
            if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                    or (self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                    in_box or dead)):
                turns[2] = True

            if direction == 2 or direction == 3:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[3] = True
                    if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
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
                    if self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[3] = True
                    if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3 \
                            or (self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[2] = True
                if 12 <= center_y % self.pixel_height <= 18:
                    if self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] < 3 \
                            or (self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] == 9 and (
                            in_box or dead)):
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True
            
        return turns


    def check_collision_points(self, center_x, center_y, powerup, power_count, score):
        """
        Verifica colisões com os pontos no tabuleiro.

        Parâmetros:
        - center_x (int): Coordenada x do centro do personagem.
        - center_y (int): Coordenada y do centro do personagem.
        - powerup (bool): Indica se há um power-up ativo ou não.
        - power_count (int): Contagem do power-up.
        - score (int): Pontuação atual.

        Retorna:
        Atualiza o score, powerups e fantasmas comidos.
        """

        if 0 < center_x < 870:
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 1:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 10
                if not pygame.mixer.get_busy():
                    self.sounds["dot"].play()
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 2:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 50
                powerup = True
                power_count = 0
                self.sounds["fruit"].play()
        return score, powerup, power_count


    def get_turns_player(self, player):
        """
        Verifica a posição do personagem no tabuleiro e possíveis colisões.

        Parâmetros:

        Retorna:
        Uma lista indicando direções permitidas para o movimento.
        """
        center_x, center_y = player.get_center()
        direction = player.get_direction()

        turns = [False, False, False, False]
        # check collisions based on center x and center y of player +/- fudge number
        if center_x // 30 < 29:
            if direction == 0:
                if self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] < 3:
                    turns[1] = True
            if direction == 1:
                if self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] < 3:
                    turns[0] = True
            if direction == 2:
                if self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3:
                    turns[3] = True
            if direction == 3:
                if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3:
                    turns[2] = True

            if direction == 2 or direction == 3:
                if 12 <= center_x % self.pixel_width <= 18:
                    if self.board[(center_y + self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3:
                        turns[3] = True
                    if self.board[(center_y - self.MARGIN) // self.pixel_height][center_x // self.pixel_width] < 3:
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
                    if self.board[center_y // self.pixel_height][(center_x - self.MARGIN) // self.pixel_width] < 3:
                        turns[1] = True
                    if self.board[center_y // self.pixel_height][(center_x + self.MARGIN) // self.pixel_width] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns


    def in_box(self, rect):
        return self.box.colliderect(rect)


    def draw(self, screen):
        """
        Desenha o tabuleiro na tela do jogo.

        Parâmetros:
        - screen (pygame.Surface): Superfície da tela onde o tabuleiro será desenhado.
        """

        self.blink += 1
        if self.blink == 2*self.BLINK_RATE:
            self.blink = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + (0.5 * self.pixel_height)), 4)

                elif self.board[i][j] == 2 and self.blink < self.BLINK_RATE:
                    pygame.draw.circle(screen, 'white', (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + (0.5 * self.pixel_height)), 10)
                
                elif self.board[i][j] == 3:
                    pygame.draw.line(screen, self.main_color, (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height), (j * self.pixel_width + (0.5 * self.pixel_width), i * self.pixel_height + self.pixel_height), 3)

                elif self.board[i][j] == 4:
                    pygame.draw.line(screen, self.main_color, (j * self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), (j * self.pixel_width + self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), 3)

                elif self.board[i][j] == 5:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width - (self.pixel_width * 0.4)) - 2, (i * self.pixel_height + (0.5 * self.pixel_height)), self.pixel_width, self.pixel_height], 0, PI / 2, 3)

                elif self.board[i][j] == 6:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width + (self.pixel_width * 0.5)), (i * self.pixel_height + (0.5 * self.pixel_height)), self.pixel_width, self.pixel_height], PI / 2, PI, 3)

                elif self.board[i][j] == 7:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width + (self.pixel_width * 0.5)), (i * self.pixel_height - (0.4 * self.pixel_height)), self.pixel_width, self.pixel_height], PI, 3 * PI / 2, 3)

                elif self.board[i][j] == 8:
                    pygame.draw.arc(screen, self.main_color, [(j * self.pixel_width - (self.pixel_width * 0.4)) - 2, (i * self.pixel_height - (0.4 * self.pixel_height)), self.pixel_width, self.pixel_height], 3 * PI / 2, 2 * PI, 3)
                
                elif self.board[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), (j * self.pixel_width + self.pixel_width, i * self.pixel_height + (0.5 * self.pixel_height)), 3)
    

    gameover_img = load_image("/images/other/endgame.png", 300)

    def game_over_screen(self, screen, font) :
        
        screen.blit(self.gameover_img, (self.height//2, self.width//2))
    
        button = QuitButton(350, 410, 200, 80, gray, "Sair", screen)
        
        # # loop do gameover screen 

        gameover_state = True

        # Main game loop
        while gameover_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.rect.collidepoint(event.pos):
                        pygame.quit()

            # Draw the button
            button.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)                 
                        
                
        

