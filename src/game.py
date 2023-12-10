import pygame
from pygame import font
from player import Player
from enemies import Enemies
from board import Board
import pygame_menu
import json
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
import os


from utils import load_board, load_image

def load_high_scores(filename='highscores.json'):
    project_root = os.path.dirname(os.path.dirname(__file__))  # Obtém o diretório raiz do projeto
    filepath = os.path.join(project_root, filename)  # Constrói o caminho até o arquivo
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_high_scores(high_scores, filename='highscores.json'):
    project_root = os.path.dirname(os.path.dirname(__file__))  # Obtém o diretório raiz do projeto
    filepath = os.path.join(project_root, filename)  # Constrói o caminho até o arquivo
    with open(filepath, 'w') as file:
        json.dump(high_scores, file, indent=4)

class Game():
    """Esta classe controla a lógica principal do jogo."""

    WIDTH = 900
    HEIGHT = 900

    FPS = 60

    # pygame.font.init()
    # font = pygame.font.Font(None, 20)

    def __init__(self, ):
        """
        Inicializa a classe Game, responsável pelo controle principal do jogo.

        Configura a janela do jogo, cria instâncias de personagens, inimigos e define variáveis de estado do jogo.
        """

        pygame.init()

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
        )
        self.sprites_group.add(self.player)

        self.enemies = Enemies(board["ghostsStart"])
        self.enemies.add_to_group(self.sprites_group)

        self.powerup = {
            "active": False,
            "counter": 0,
            "duration": 5,
        }
        self.eaten_ghosts = [False, False, False, False]
        self.moving = False
        self.start_counter = 2
        self.game_over = False
        self.game_won = False
        self.direction_command = 0
        self.lives = 3

        self.score = 0

        self.coracao = load_image('/images/other/heart.png', 20)
        self.high_scores = load_high_scores()
        self.player_name = 'Player'

    
    ##### MENU #####
    
    def set_player_name(self, name):
        self.player_name = name

    def start_the_game(self):
        self.run()

    def show_menu(self):
        main_menu = pygame_menu.Menu('Welcome', self.WIDTH, self.HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
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
        # Criar um menu para mostrar as pontuações mais altas
        high_score_menu = pygame_menu.Menu('High Scores', self.WIDTH, self.HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

        for score in self.high_scores:
            high_score_menu.add.label(f"{score['name']} : {score['score']}")

        high_score_menu.add.button('Back', pygame_menu.events.BACK)
        return high_score_menu

######## END MENU ########
    

    def start(self, ):
        """Inicia o loop principal do jogo."""
        # self.show_menu()
        self.run()
    
    def restart(self, ):
        """Reinicia algumas variáveis do jogo para recomeçar."""
        self.moving = False
        self.start_counter = 2
        self.player.restart()
        for ghost in self.enemies.ghosts.values():
            ghost.restart()

    def run(self, ):
        """Loop principal do jogo, controla a lógica do jogo."""
        running = True
        while running:
            self.dt = self.clock.tick(self.FPS) / 1000.0

            if self.powerup["active"]:
                if self.powerup["counter"] < self.powerup["duration"]:
                    self.powerup["counter"] += self.dt
                else:
                    self.powerup["active"] = False
                    self.powerup["counter"] = 0
                    self.eaten_ghosts = [False, False, False, False]
            
            if self.start_counter > 0 and not self.game_over and not self.game_won:
                self.start_counter -= self.dt
                self.moving = False
            else:
                self.moving = True
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.direction_command = 0
                    if event.key == pygame.K_a:
                        self.direction_command = 1
                    if event.key == pygame.K_w:
                        self.direction_command = 2
                    if event.key == pygame.K_s:
                        self.direction_command = 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d and self.direction_command == 0:
                        self.direction_command = self.player.direction
                    if event.key == pygame.K_a and self.direction_command == 1:
                        self.direction_command = self.player.direction
                    if event.key == pygame.K_w and self.direction_command == 2:
                        self.direction_command = self.player.direction
                    if event.key == pygame.K_s and self.direction_command == 3:
                        self.direction_command = self.player.direction
            if self.direction_command == 0 and self.player.turns[0]:
                self.player.direction = 0
            if self.direction_command == 1 and self.player.turns[1]:
                self.player.direction = 1
            if self.direction_command == 2 and self.player.turns[2]:
                self.player.direction = 2
            if self.direction_command == 3 and self.player.turns[3]:
                self.player.direction = 3

            self.screen.fill("black")
            self.board.draw(self.screen)
            self.sprites_group.draw(self.screen)

            self.score, self.powerup["active"], self.powerup["counter"], self.eaten_ghosts = self.board.check_collision_points(
                self.player.rect.centerx,
                self.player.rect.centery,
                self.powerup["active"],
                self.powerup["counter"],
                self.score,
                self.eaten_ghosts,
            )

            self.enemies.set_spooked(self.powerup["active"])
            
            self.player.turns = self.board.check_postion(*self.player.rect.center, self.player.turns, self.player.direction)

            self.enemies.revive(self.board.in_box(self.enemies.get_pos()))

            self.sprites_group.update()
            self.game_won = self.board.available_fruits_and_dots <= 0

            if self.moving:
                self.player.move()

                for ghost in self.enemies.ghosts.values():
                    ghost.turns, ghost.in_box = self.board.check_collision_ghost(ghost.rect.centerx, ghost.rect.centery, ghost.turns, ghost.in_box, ghost.direction)

                self.get_targets()

                for ghost in self.enemies.ghosts.values():
                    ghost.move()

            if not self.powerup["active"] and self.check_collision_player_ghosts():
                if self.lives > 0:
                    self.lives -= 1
                    self.restart()
                else:
                    self.moving = False
                    self.game_over = True
        

            if self.powerup["active"]:
                self.check_eat_ghost()

            self.draw_stats(self.font, self.score, self.screen, self.lives, self.coracao)

            if self.game_over or self.game_won:
                # self.running = False
                self.screen.fill("black")
                self.update_high_scores()
                self.board.game_over_screen(self.screen, self.font)

            if self.game_won :
                self.screen.fill("black")
                self.board.game_won_screen(self.screen, self.font_big, self.font_mid, self.score)

            pygame.display.flip()

        pygame.quit()

    def draw_stats(self, font, score, screen, lives, heart_image):
        score_text = font.render(f"Pontuação: {score}", True, 'white')
        screen.blit(score_text, (10, 880))

        lives_text = font.render(f"Vidas restantes: {lives}", True, 'white')
        screen.blit(lives_text, (120, 880))

        pos_heart = [300,875]
        for i in range(lives) :
            screen.blit(heart_image, pos_heart)
            pos_heart[0] = pos_heart[0] + 25

        percentage = str((256 - self.board.available_fruits_and_dots)*100//256)
        progress = font.render(f"Progresso: {percentage}%", True, 'white')
        screen.blit(progress, (700, 880))

    def check_collision_player_ghosts(self, ):
        """Verifica se houve colisão entre o jogador e os fantasmas."""
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.dead:
                return True

        return False
    
    def check_eat_ghost(self, ):
        """Verifica se o jogador comeu um fantasma e atualiza a pontuação."""
        i = 0
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.dead:
                ghost.dead = True
                self.score += (2 ** self.eaten_ghosts.count(True)) * 100
                self.eaten_ghosts[i] = True
                i += 1
    
    def get_targets(self):
        """Define os alvos dos fantasmas com base na posição do jogador e no mapa."""
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
            if not blinky.dead and not blinky.eaten:
                blinky_target = (runaway_x, runaway_y)
            elif not blinky.dead and blinky.eaten:
                if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                    blinky_target = (400, 100)
                else:
                    blinky_target = (player_x, player_y)
            else:
                blinky_target = return_target
            if not inky.dead and not pinky.eaten:
                inky_target = (runaway_x, player_y)
            elif not inky.dead and pinky.eaten:
                if 340 < inky_x < 560 and 340 < inky_y < 500:
                    inky_target = (400, 100)
                else:
                    inky_target = (player_x, player_y)
            else:
                inky_target = return_target
            if not pinky.dead:
                pinky_target = (player_x, runaway_y)
            elif not pinky.dead and inky.eaten:
                if 340 < pinky_x < 560 and 340 < pinky_y < 500:
                    pinky_target = (400, 100)
                else:
                    pinky_target = (player_x, player_y)
            else:
                pinky_target = return_target
            if not clyde.dead and not clyde.eaten:
                clyde_target = (450, 450)
            elif not clyde.dead and clyde.eaten:
                if 340 < clyde_x < 560 and 340 < clyde_y < 500:
                    clyde_target = (400, 100)
                else:
                    clyde_target = (player_x, player_y)
            else:
                clyde_target = return_target
        else:
            if not blinky.dead:
                if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                    blinky_target = (400, 100)
                else:
                    blinky_target = (player_x, player_y)
            else:
                blinky_target = return_target
            if not inky.dead:
                if 340 < inky_x < 560 and 340 < inky_y < 500:
                    inky_target = (400, 100)
                else:
                    inky_target = (player_x, player_y)
            else:
                inky_target = return_target
            if not pinky.dead:
                if 340 < pinky_x < 560 and 340 < pinky_y < 500:
                    pinky_target = (400, 100)
                else:
                    pinky_target = (player_x, player_y)
            else:
                pinky_target = return_target
            if not clyde.dead:
                if 340 < clyde_x < 560 and 340 < clyde_y < 500:
                    clyde_target = (400, 100)
                else:
                    clyde_target = (player_x, player_y)
            else:
                clyde_target = return_target

        self.enemies.ghosts["blinky"].target = blinky_target
        self.enemies.ghosts["inky"].target = inky_target
        self.enemies.ghosts["pinky"].target = pinky_target
        self.enemies.ghosts["clyde"].target = clyde_target

if __name__ == "__main__":
    game = Game()
    game.show_menu()
    game.start()
