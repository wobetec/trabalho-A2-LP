import os 
import pygame
import json


def load_image(filename, size=45):
    path = os.path.join(os.path.dirname(__file__), f'../assets{filename}')
    return pygame.transform.scale(pygame.image.load(path), (size, size))

def load_board(board_name):
    path = os.path.join(os.path.dirname(__file__), f"../assets/boards/{board_name}.json")
    with open(path, "r") as f:
        return json.load(f)