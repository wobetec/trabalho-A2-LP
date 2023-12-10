import pygame
from pygame import font
from player import Player
from enemies import Enemies
from board import Board
import pygame_menu
import json
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
import os
import sys
from button import Button

from utils import load_board, load_image, load_sound

def load_high_scores(filename='highscores.json'):
    """
    Carrega as pontuações mais altas de um arquivo JSON.

    Parameters:
        filename (str): O caminho do arquivo JSON para carregar as pontuações.

    Returns:
        list: Uma lista de dicionários contendo as pontuações mais altas e os nomes dos jogadores.
    """
    project_root = os.path.dirname(os.path.dirname(__file__))  # Obtém o diretório raiz do projeto
    filepath = os.path.join(project_root, filename)  # Constrói o caminho até o arquivo
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_high_scores(high_scores, filename='highscores.json'):
    """
    Salva as pontuações mais altas em um arquivo JSON.

    Parameters:
        high_scores (list): Uma lista de dicionários contendo as pontuações mais altas e os nomes dos jogadores.
        filename (str): O caminho do arquivo JSON onde as pontuações serão salvas.

    Returns:
        None
    """
    project_root = os.path.dirname(os.path.dirname(__file__))  # Obtém o diretório raiz do projeto
    filepath = os.path.join(project_root, filename)  # Constrói o caminho até o arquivo
    with open(filepath, 'w') as file:
        json.dump(high_scores, file, indent=4)

class Game():
    """
    Classe principal do jogo, gerenciando a lógica principal e o estado do jogo.

    Attributes:
        WIDTH (int): Largura da tela do jogo.
        HEIGHT (int): Altura da tela do jogo.
        FPS (int): Frames por segundo do jogo.
        screen (pygame.Surface): A superfície principal onde o jogo é renderizado.
        clock (pygame.time.Clock): O relógio do jogo para controle de tempo.
        font (pygame.font.Font): Fonte pequena para renderização de texto.
        font_mid (pygame.font.Font): Fonte de tamanho médio para renderização de texto.
        font_big (pygame.font.Font): Fonte grande para renderização de texto.
        sprites_group (pygame.sprite.Group): Grupo que contém todos os sprites do jogo.
        board (Board): O tabuleiro do jogo, contendo informações sobre layout e colisões.
        player (Player): O jogador controlado pelo usuário.
        enemies (Enemies): O grupo de inimigos no jogo.
        powerup (dict): Dicionário contendo informações sobre o power-up (se está ativo, contador, duração).
        moving (bool): Flag para controlar se os sprites estão se movendo.
        start_counter (float): Contador para o início do jogo.
        game_over (bool): Flag que indica se o jogo terminou (perda).
        game_won (bool): Flag que indica se o jogo foi vencido.
        direction_command (int): Direção atual comandada pelo jogador.
        lives (int): Número de vidas do jogador.
        score (int): Pontuação atual do jogador.
        coracao (pygame.Surface): Imagem representando a vida do jogador.
        sounds (dict): Dicionário contendo os efeitos sonoros do jogo.
        high_scores (list): Lista de pontuações mais altas.
        player_name (str): Nome do jogador.
        gameover_img (pygame.Surface): Imagem da tela de 'game over'.
        game_won_img (pygame.Surface): Imagem da tela de vitória.
        white (tuple): Cor branca em RGB.
        black (tuple): Cor preta em RGB.
        gray (tuple): Cor cinza em RGB.
    """

    WIDTH = 900
    HEIGHT = 900

    FPS = 60


    def __init__(self, ):
        """
        Inicializa a classe Game, responsável pelo controle principal do jogo.

        Configura a janela do jogo, cria instâncias de personagens, inimigos e define variáveis de estado do jogo.
        """
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Pacman')

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        

        # SETAR AS FONTES 
        self.font = pygame.font.Font(None, 20)
        self.font_mid = pygame.font.Font(None, 50)
        self.font_big = pygame.font.Font(None, 100)

        self.sprites_group = pygame.sprite.Group()
        
        board = load_board("originalBoard")
        self.board = Board(board["board"], self.WIDTH, self.HEIGHT, board["box"])

        self.player = Player(
            board["playerStart"]["x"],
            board["playerStart"]["y"],
            board["playerStart"]["direction"],
            self.WIDTH,
            self.HEIGHT,
        )
        self.sprites_group.add(self.player)

        self.enemies = Enemies(board["ghostsStart"], self.WIDTH, self.HEIGHT)
        self.enemies.add_to_group(self.sprites_group)

        self.powerup = {
            "active": False,
            "counter": 0,
            "duration": 5,
        }

        self.moving = False
        self.start_counter = 4
        self.game_over = False
        self.game_won = False
        self.direction_command = 0
        self.lives = 3
        self.score = 0
        self.coracao = load_image('/images/other/heart.png', 20)
        self.sounds = {
            "start": load_sound("beginning"),
            "death": load_sound("death"),
            "ghost": load_sound("eatghost"),
        }
        self.high_scores = load_high_scores()
        self.player_name = 'Player'

    
    ##### MENU #####
    
    def set_player_name(self, name):
        """
        Define o nome do jogador.

        Parameters:
            name (str): O nome do jogador a ser definido.
        """
        self.player_name = name

    def start_the_game(self):
        """
        Inicia o loop principal do jogo.
        """
        self.run()

    def show_menu(self):
        """
        Exibe o menu principal do jogo, permitindo ao jogador iniciar o jogo, ver pontuações mais altas ou sair.
        """
        main_menu = pygame_menu.Menu('Welcome', self.WIDTH, self.HEIGHT, theme=pygame_menu.themes.THEME_DARK)
        high_score_menu = self.show_high_scores()

        main_menu.add.text_input('Name :', default='Player 1', onchange=self.set_player_name)
        main_menu.add.button('Play', self.start_the_game)
        main_menu.add.button('High Scores', high_score_menu)
        main_menu.add.button('Quit', pygame_menu.events.EXIT)

        current_menu = main_menu

        while True:
            if current_menu.is_enabled():
                current_menu.mainloop(self.screen)
            if current_menu == main_menu and not high_score_menu.is_enabled():
                break
    

    def update_high_scores(self):
        """
        Atualiza a lista de pontuações mais altas com a pontuação atual do jogador.
        """

        # Verificar se o nome do jogador foi definido
        if hasattr(self, 'player_name'):
            # Adicionar a pontuação atual e o nome do jogador às pontuações mais altas
            self.high_scores.append({'name': self.player_name, 'score': self.score})
            # Ordenar a lista de pontuações mais altas em ordem decrescente
            self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)
            # Manter apenas as 10 melhores pontuações
            self.high_scores = self.high_scores[:10]
            # Salvar as pontuações mais altas atualizadas
            save_high_scores(self.high_scores)
    
    def show_high_scores(self):
        """
        Exibe um menu com as pontuações mais altas do jogo.

        Returns:
            pygame_menu.Menu: Um objeto de menu contendo as pontuações mais altas.
        """

        # Criar um menu para mostrar as pontuações mais altas
        high_score_menu = pygame_menu.Menu('High Scores', self.WIDTH, self.HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

        for score in self.high_scores:
            high_score_menu.add.label(f"{score['name']} : {score['score']}")

        high_score_menu.add.button('Back', pygame_menu.events.BACK)
        return high_score_menu

######## END MENU ########
    
    def restart(self, ):
        """Reinicia algumas variáveis do jogo para recomeçar."""
        self.moving = False
        self.start_counter = 2
        self.player.restart()
        self.enemies.restart()

    def run(self, ):
        """Loop principal do jogo, controla a lógica do jogo."""
        running = True
        self.sounds["start"].play()
        while running:
            t_dt = self.clock.tick(self.FPS) / 1000.0
            self.dt = min(t_dt, 0.018)

            if self.powerup["active"]:
                if self.powerup["counter"] < self.powerup["duration"]:
                    self.powerup["counter"] += self.dt
                else:
                    self.powerup["active"] = False
                    self.powerup["counter"] = 0
                    self.enemies.set_eaten(False)
            
            if self.start_counter > 0 and not self.game_over and not self.game_won:
                self.start_counter -= self.dt
                self.moving = False
            else:
                self.moving = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.player.get_input()

            self.screen.fill("black")
            self.board.draw(self.screen)
            self.sprites_group.draw(self.screen)

            self.score, self.powerup["active"], self.powerup["counter"] = self.board.check_collision_points(
                *self.player.get_center(),
                self.powerup["active"],
                self.powerup["counter"],
                self.score,
            )

            self.enemies.set_spooked(self.powerup["active"])
            
            self.player.set_turns(self.board.get_turns_player(self.player))

            self.verify_in_box()

            self.sprites_group.update()

            self.game_won = self.board.available_fruits_and_dots <= 0

            if self.moving:
                self.player.move()

                self.get_targets()

                for ghost in self.enemies.ghosts.values():
                    ghost.set_turns(self.board.get_turns_ghost(ghost))
                    ghost.move()

            if not self.powerup["active"] and self.check_collision_player_ghosts():
                if self.lives > 1:
                    self.sounds["death"].play()
                    pygame.time.wait(1000)
                    self.lives -= 1
                    self.restart()
                else:
                    self.moving = False
                    self.game_over = True
        
            if self.powerup["active"]:
                self.check_eat_ghost()

            self.draw_stats(self.font, self.score, self.screen, self.lives, self.coracao)

            if self.game_over:
                self.screen.fill("black")
                self.update_high_scores()
                if self.game_over_screen(self.screen, self.font):
                    self.show_menu()  # Mostra o menu principal se o usuário escolher 'Menu'
                    break  # Encerra o loop do jogo

            if self.game_won:
                self.screen.fill("black")
                self.update_high_scores()
                if self.game_won_screen(self.screen, self.font_big, self.font_mid, self.score):
                    self.show_menu()  # Mostra o menu principal se o usuário escolher 'Menu'
                    break  # Encerra o loop do jogo

            pygame.display.flip()

        pygame.quit()

    def draw_stats(self, font, score, screen, lives, heart_image):
        """
        Desenha as estatísticas do jogo, incluindo pontuação e vidas, na tela.

        Parameters:
            font (pygame.font.Font): A fonte a ser usada para desenhar o texto.
            score (int): A pontuação atual do jogador.
            screen (pygame.Surface): A superfície onde as estatísticas serão desenhadas.
            lives (int): O número de vidas restantes do jogador.
            heart_image (pygame.Surface): A imagem de um coração a ser usada para representar vidas.
        """
        score_text = self.font.render(f"Pontuação: {score}", True, 'white')
        screen.blit(score_text, (10, 880))

        lives_text = self.font.render(f"Vidas restantes: {lives}", True, 'white')
        screen.blit(lives_text, (120, 880))

        pos_heart = [300,875]
        for i in range(lives) :
            screen.blit(heart_image, pos_heart)
            pos_heart[0] = pos_heart[0] + 25

        percentage = str((256 - self.board.available_fruits_and_dots)*100//256)
        progress = font.render(f"Progresso: {percentage}%", True, 'white')
        screen.blit(progress, (700, 880))

    def check_collision_player_ghosts(self, ):
        """
        Verifica se houve colisão entre o jogador e os fantasmas.

        Returns:
            bool: Verdadeiro se houve colisão, falso caso contrário.
        """
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.is_dead():
                return True

        return False
    

    def check_eat_ghost(self, ):
        """
        Verifica se o jogador comeu um fantasma e atualiza a pontuação.
        """
        i = 0
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.is_dead():
                ghost.set_dead(True)
                self.sounds["ghost"].play()
                self.score += (2 ** i) * 100
                i += 1
    

    def get_targets(self, ):
        """
        Define os alvos dos fantasmas com base na posição do jogador e no estado do jogo.
        """
        blinky = self.enemies.ghosts["blinky"]
        blinky_x, blinky_y = blinky.rect.center

        inky = self.enemies.ghosts["inky"]
        inky_x, inky_y = inky.rect.center

        pinky = self.enemies.ghosts["pinky"]
        pinky_x, pinky_y = pinky.rect.center

        clyde = self.enemies.ghosts["clyde"]
        clyde_x, clyde_y = clyde.rect.center

        player_x, player_y = self.player.rect.center

        if player_x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if player_y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (380, 400)
        if self.powerup["active"]:
            if not blinky.is_dead() and not blinky.is_eaten():
                blinky_target = (runaway_x, runaway_y)
            elif not blinky.is_dead() and blinky.is_eaten():
                if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                    blinky_target = (400, 100)
                else:
                    blinky_target = (player_x, player_y)
            else:
                blinky_target = return_target
            if not inky.is_dead() and not pinky.is_eaten():
                inky_target = (runaway_x, player_y)
            elif not inky.is_dead() and pinky.is_eaten():
                if 340 < inky_x < 560 and 340 < inky_y < 500:
                    inky_target = (400, 100)
                else:
                    inky_target = (player_x, player_y)
            else:
                inky_target = return_target
            if not pinky.is_dead():
                pinky_target = (player_x, runaway_y)
            elif not pinky.is_dead() and inky.is_eaten():
                if 340 < pinky_x < 560 and 340 < pinky_y < 500:
                    pinky_target = (400, 100)
                else:
                    pinky_target = (player_x, player_y)
            else:
                pinky_target = return_target
            if not clyde.is_dead() and not clyde.is_eaten():
                clyde_target = (450, 450)
            elif not clyde.is_dead() and clyde.is_eaten():
                if 340 < clyde_x < 560 and 340 < clyde_y < 500:
                    clyde_target = (400, 100)
                else:
                    clyde_target = (player_x, player_y)
            else:
                clyde_target = return_target
        else:
            if not blinky.is_dead():
                if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                    blinky_target = (400, 100)
                else:
                    blinky_target = (player_x, player_y)
            else:
                blinky_target = return_target
            if not inky.is_dead():
                if 340 < inky_x < 560 and 340 < inky_y < 500:
                    inky_target = (400, 100)
                else:
                    inky_target = (player_x, player_y)
            else:
                inky_target = return_target
            if not pinky.is_dead():
                if 340 < pinky_x < 560 and 340 < pinky_y < 500:
                    pinky_target = (400, 100)
                else:
                    pinky_target = (player_x, player_y)
            else:
                pinky_target = return_target
            if not clyde.is_dead():
                if 340 < clyde_x < 560 and 340 < clyde_y < 500:
                    clyde_target = (400, 100)
                else:
                    clyde_target = (player_x, player_y)
            else:
                clyde_target = return_target

        self.enemies.ghosts["blinky"].set_target(blinky_target)
        self.enemies.ghosts["inky"].set_target(inky_target)
        self.enemies.ghosts["pinky"].set_target(pinky_target)
        self.enemies.ghosts["clyde"].set_target(clyde_target)


    def verify_in_box(self, ):
        """
        Verifica se os fantasmas estão na 'caixa' de início e ajusta seu estado.
        """
        for ghost in self.enemies.ghosts.values():
            in_box = self.board.in_box(ghost.get_rect())
            ghost.set_in_box(in_box)

    #### FINAL SCREENS ####

    gameover_img = load_image("/images/other/endgame.png", 600)
    game_won_img = load_image("/images/other/pinho.jpg", 900)

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (200, 200, 200)

    def game_over_screen(self, screen, font) :
        """
        Exibe a tela de fim de jogo quando o jogador perde todas as vidas.

        Parameters:
            screen (pygame.Surface): A superfície onde a tela de fim de jogo será desenhada.
            font (pygame.font.Font): A fonte a ser usada para desenhar o texto.

        Returns:
            bool: Verdadeiro se o jogador escolher retornar ao menu principal, falso caso contrário.
        """
        
        screen.blit(self.gameover_img, (150, -20))
    
        quit_button = Button(350, 610, 200, 80, self.gray, "Sair", screen)

        menu_button = Button(350, 510, 200, 80, self.white, "Menu", screen)
        
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
                        sys.exit()
                    if menu_button.rect.collidepoint(event.pos):
                        return_to_menu = True  # Define a flag para retornar ao menu
                        gameover_state = False                   

            # Draw the quit button
            quit_button.draw()

            # Draw the restart button
            menu_button.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)
        return return_to_menu                 

    def game_won_screen(self, screen, font_big, font, points):

        """
        Exibe a tela de vitória quando o jogador vence o jogo.

        Parameters:
            screen (pygame.Surface): A superfície onde a tela de vitória será desenhada.
            font_big (pygame.font.Font): A fonte grande para o texto principal.
            font (pygame.font.Font): A fonte para o texto secundário.
            points (int): A pontuação final do jogador.

        Returns:
            bool: Verdadeiro se o jogador escolher retornar ao menu principal, falso caso contrário.
        """
        
        screen.blit(self.game_won_img, (0, 0))
    
        quit_button = Button(350, 610, 200, 80, self.gray, "Sair", screen)

        menu_button = Button(350, 510, 200, 80, self.white, "Menu", screen)
        
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
                        sys.exit()
                    if menu_button.rect.collidepoint(event.pos):
                        return_to_menu = True  # Define a flag para retornar ao menu
                        gamewon_state = False              


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

        return return_to_menu  



if __name__ == "__main__":
    game = Game()
    game.show_menu()
