from random import choice
import pygame
from utils import load_image
from character import Character

class Enemies:

    GHOSTS_NAMES = ["blinky", "pinky", "inky", "clyde"]

    def __init__(self, ghosts_start):
        """Inicializa os fantasmas no jogo."""
        self.ghosts = { 
            x: Ghost(
                x,
                ghosts_start[x]["x"],
                ghosts_start[x]["y"],
                ghosts_start[x]["direction"],
            ) for x in self.GHOSTS_NAMES
        }
        self.powerup = False
        self.targets = []
    
    def add_to_group(self, group):
        """Adiciona os fantasmas a um grupo de sprites."""
        for ghost in self.ghosts.values():
            group.add(ghost)

    def get_pos(self,):
        """Retorna a posição atual de cada fantasma."""
        return {x: (self.ghosts[x].rect.x, self.ghosts[x].rect.y) for x in self.GHOSTS_NAMES}

    def revive(self, in_box):
        """Revive os fantasmas que estão na caixa."""
        for key, value in in_box.items():
            if value:
                self.ghosts[key].dead = False

    def set_spooked(self, powerup):
        """Define se os fantasmas estão assustados ou não."""
        for ghost in self.ghosts.values():
            if powerup:
                ghost.spooked = True
            else:
                ghost.spooked = False
                ghost.dead = False


class Ghost(Character):
    """Esta classe define os fantasmas do jogo."""

    SPOOKED_IMG = load_image("/images/ghost/spooked.png")
    DEAD_IMG = load_image("/images/ghost/dead.png")

    def __init__(self, name, start_x, start_y, start_direction):
        """Inicializa um fantasma com suas características."""
        super().__init__(start_x, start_y, start_direction)
        self.name = name

        self.images = [load_image(f"/images/ghost/{self.name}.png")]
        self.image.blit(self.images[0], (0, 0))

        self.in_box = False
        self.dead = False
        self.spooked = False
        self.slow = False
        self.eaten = False

        self.target = [0, 0]

    def restart(self, ):
        """Reinicia o estado do fantasma para recomeçar."""
        self.rect.center = self.start_pos
        self.direction = self.start_direction
        self.dead = False
        self.spooked = False
        self.slow = False
        self.eaten = False
        self.speed = 3

    def set_speed(self, ):
        """Define a velocidade do fantasma com base em seu estado."""
        if self.spooked:
            self.speed = 1
        if self.eaten:
            self.speed = 2
        if self.dead:
            self.speed = 4
        
    def set_image(self, ):
        """Define a imagem do fantasma com base em seu estado."""
        self.image.fill((0, 0, 0))
        if (not self.spooked and not self.dead) or (self.eaten and self.spooked and not self.dead):
            self.image.blit(self.images[0], (0, 0))
        elif self.spooked and not self.dead and not self.eaten:
            self.image.blit(self.SPOOKED_IMG, (0, 0))
        else:
            self.image.blit(self.DEAD_IMG, (0, 0))

    def update(self, ):
        """Atualiza a imagem e velocidade do fantasma."""
        self.set_image()
        self.set_speed()

    def move(self, ):
        """Move o fantasma no jogo."""
        if self.name == "clyde":
            # clyde is going to turn whenever advantageous for pursuit

            if self.direction == 0:
                if self.target[0] > self.rect.centerx and self.turns[0]:
                    self.rect.centerx += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    if self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    else:
                        self.rect.centerx += self.speed
            elif self.direction == 1:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.rect.centerx and self.turns[1]:
                    self.rect.centerx -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    if self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    else:
                        self.rect.centerx -= self.speed
            elif self.direction == 2:
                if self.target[0] < self.rect.centerx and self.turns[1]:
                    self.direction = 1
                    self.rect.centerx -= self.speed
                elif self.target[1] < self.rect.centery and self.turns[2]:
                    self.direction = 2
                    self.rect.centery -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    else:
                        self.rect.centery -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.rect.centery += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    else:
                        self.rect.centery += self.speed

        elif self.name == "blinky":
            # blinky is going to turn whenever colliding with walls, otherwise continue straight

            if self.direction == 0:
                if self.target[0] > self.rect.centerx and self.turns[0]:
                    self.rect.centerx += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[0]:
                    self.rect.centerx += self.speed
            elif self.direction == 1:
                if self.target[0] < self.rect.centerx and self.turns[1]:
                    self.rect.centerx -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[1]:
                    self.rect.centerx -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.rect.centery and self.turns[2]:
                    self.direction = 2
                    self.rect.centery -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[2]:
                    self.rect.centery -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.rect.centery += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[3]:
                    self.rect.centery += self.speed

        elif self.name == "inky":
            # inky self.turns up or down at any point to pursue, but left and right only on collision

            if self.direction == 0:
                if self.target[0] > self.rect.centerx and self.turns[0]:
                    self.rect.centerx += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    if self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    else:
                        self.rect.centerx += self.speed
            elif self.direction == 1:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.rect.centerx and self.turns[1]:
                    self.rect.centerx -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    if self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    else:
                        self.rect.centerx -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.rect.centery and self.turns[2]:
                    self.direction = 2
                    self.rect.centery -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[2]:
                    self.rect.centery -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.rect.centery += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[3]:
                    self.rect.centery += self.speed

        elif self.name == "pinky":
            # inky is going to turn left or right whenever advantageous, but only up or down on collision

            if self.direction == 0:
                if self.target[0] > self.rect.centerx and self.turns[0]:
                    self.rect.centerx += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                elif self.turns[0]:
                    self.rect.centerx += self.speed
            elif self.direction == 1:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.rect.centerx and self.turns[1]:
                    self.rect.centerx -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[1]:
                    self.rect.centerx -= self.speed
            elif self.direction == 2:
                if self.target[0] < self.rect.centerx and self.turns[1]:
                    self.direction = 1
                    self.rect.centerx -= self.speed
                elif self.target[1] < self.rect.centery and self.turns[2]:
                    self.direction = 2
                    self.rect.centery -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] > self.rect.centery and self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.rect.centery += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[2]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    else:
                        self.rect.centery -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.rect.centery and self.turns[3]:
                    self.rect.centery += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.target[1] < self.rect.centery and self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.rect.centery -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.rect.centerx and self.turns[0]:
                        self.direction = 0
                        self.rect.centerx += self.speed
                    elif self.target[0] < self.rect.centerx and self.turns[1]:
                        self.direction = 1
                        self.rect.centerx -= self.speed
                    else:
                        self.rect.centery += self.speed

        if self.rect.centerx < 0:
            self.rect.centerx = 900
        elif self.rect.centerx > 900:
            self.rect.centerx =0

        