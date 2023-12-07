import pygame
from player import Player
from enemies import Enemies
from board import Board

from utils import load_board

class Game():

    WIDTH = 900
    HEIGHT = 900

    FPS = 60

    def __init__(self, ):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
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

    def start(self, ):
        self.run()
    
    def restart(self, ):
        self.moving = False
        self.start_counter = 2
        self.player.restart()
        for ghost in self.enemies.ghosts.values():
            ghost.restart()

    def run(self, ):
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


            pygame.display.flip()

        pygame.quit()

    def check_collision_player_ghosts(self, ):
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.dead:
                return True

        return False
    
    def check_eat_ghost(self, ):
        i = 0
        for ghost in self.enemies.ghosts.values():
            if self.player.rect.colliderect(ghost.rect) and not ghost.dead:
                ghost.dead = True
                self.score += (2 ** self.eaten_ghosts.count(True)) * 100
                self.eaten_ghosts[i] = True
                i += 1
    
    def get_targets(self):
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
    game.start()
