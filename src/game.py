import pygame
from pygame import font
from player import Player
from enemies import Enemies
from board import Board

from utils import load_board, load_image, load_sound

class Game():
    """Esta classe controla a lógica principal do jogo."""

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
        
        self.font = pygame.font.Font(None, 20)

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

    def start(self, ):
        """Inicia o loop principal do jogo."""
        self.run()
    
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
            self.dt = self.clock.tick(self.FPS) / 1000.0

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
                if self.lives > 0:
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

            if self.game_over :
                self.screen.fill("black")
                self.board.game_over_screen(self.screen, self.font)

            pygame.display.flip()

        pygame.quit()

    def draw_stats(self, font, score, screen, lives, heart_image):
        score_text = self.font.render(f"Pontuação: {score}", True, 'white')
        screen.blit(score_text, (10, 880))

        lives_text = self.font.render(f"Vidas restantes: {lives}", True, 'white')
        screen.blit(lives_text, (120, 880))

        pos_heart = [300,875]
        for i in range(lives) :
            screen.blit(heart_image, pos_heart)
            pos_heart[0] = pos_heart[0] + 25


    def check_collision_player_ghosts(self, ):
        """Verifica se houve colisão entre o jogador e os fantasmas."""
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.is_dead():
                return True

        return False
    

    def check_eat_ghost(self, ):
        """Verifica se o jogador comeu um fantasma e atualiza a pontuação."""
        i = 0
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.is_dead():
                ghost.set_dead(True)
                self.sounds["ghost"].play()
                self.score += (2 ** i) * 100
                i += 1
    

    def get_targets(self, ):
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
        for ghost in self.enemies.ghosts.values():
            in_box = self.board.in_box(ghost.get_rect())
            ghost.set_in_box(in_box)
        

if __name__ == "__main__":
    game = Game()
    game.start()
