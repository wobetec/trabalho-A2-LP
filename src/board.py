import copy
from math import pi as PI
import pygame

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

class Board():

    AVAILABLE_TILES = [0, 1, 2]
    ENEMIE_AVAILABLE_TILES = [0, 1, 2, 9]

    def __init__(self, board, height, width, box):
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
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1 or self.board[i][j] == 2:
                    self.available_fruits_and_dots += 1


    def check_collision_ghost(self, center_x, center_y, dead, in_box, direction):
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
        if 0 < center_x < 870:
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 1:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 10
            if self.board[center_y // self.pixel_height][center_x // self.pixel_width] == 2:
                self.board[center_y // self.pixel_height][center_x // self.pixel_width] = 0
                score += 50
                powerup = True
                power_count = 0
                eaten_ghosts = [False, False, False, False]
        return score, powerup, power_count, eaten_ghosts


    def check_postion(self, center_x, center_y, turns, direction):
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
        inside = {}
        for key, value in enemies.items():
            inside[key] = self.box.collidepoint(*value)
        return inside
    

    def draw(self, screen):
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

