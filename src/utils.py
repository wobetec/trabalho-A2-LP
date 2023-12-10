import os 
import pygame
import json


def load_image(filename, size=45):
    """
    Carrega uma imagem do arquivo especificado e redimensiona para o tamanho fornecido.

    Parameters:
        filename (str): O nome do arquivo da imagem a ser carregada.
        size (int, opcional): O tamanho desejado para a imagem. O padrão é 45x45.

    Returns:
        pygame.Surface: Uma superfície contendo a imagem carregada e redimensionada.
    """
    path = os.path.join(os.path.dirname(__file__), f'../assets{filename}')
    return pygame.transform.scale(pygame.image.load(path), (size, size))

def load_board(board_name):
    """
    Carrega um arquivo JSON que representa um tabuleiro de jogo.

    Parameters:
        board_name (str): O nome do arquivo JSON do tabuleiro a ser carregado.

    Returns:
        dict: Um dicionário contendo os dados do tabuleiro carregado do arquivo JSON.
    """
    path = os.path.join(os.path.dirname(__file__), f"../assets/boards/{board_name}.json")
    with open(path, "r") as f:
        return json.load(f)
    
def load_sound(sound_name):
    """
    Carrega um arquivo de som.

    Parameters:
        sound_name (str): O nome do arquivo de som a ser carregado.

    Returns:
        pygame.mixer.Sound: Um objeto Sound do pygame contendo o som carregado.
    """
    path = os.path.join(os.path.dirname(__file__), f"../assets/sounds/{sound_name}.wav")
    return pygame.mixer.Sound(path)