"""File containing all constant values used in the game, also is used to load assets from folder named "Images"
"""

import pygame
from typing import List, Dict
import os

def read_asset(asset_path: str) -> tuple[str, List[pygame.Surface]]:
    """Read the folder and extract all files that are accepted as an image
       use folder name as a tag for the assets

    Args:
        asset_path (str): asset folder path

    Returns:
        tuple[str, List[pygame.Surface]]: list of images with the folder tag name
    """
    asset_list: List[pygame.Surface] = []
    asset_name = os.path.basename(asset_path)

    for filename in os.listdir(asset_path):
        file_path = os.path.join(asset_path, filename)

        # pass on the paths that are folders
        if os.path.isdir(file_path):
            continue

        try:
            file_data = pygame.image.load(file_path)
            asset_list.append(file_data)
        except pygame.error:
            print(f"Skipping non-image file: {filename}")

    return asset_name, asset_list


def load_asset(root_path: str) -> Dict[str, List[pygame.Surface]]:
    """Look through the folders/files in the root_path. 
       From the found folders extract list of files to coresponding key (folder name)
       If found folders contain other folders repeat the process.   

    Args:
        root_path (str): path to the folder containing assets

    Returns:
        Dict[str, List[pygame.Surface]]: container for image files belonging to coresponding folder name
    """
    asset_dict: Dict[str, List[pygame.Surface]] = {}

    # List all items in the root directory
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)

        # Check if the item is a folder
        if os.path.isdir(item_path):
            key, surfaces = read_asset(item_path)
            asset_dict[key] = surfaces

            # do this until there are no child folders left
            # at the end merge them
            asset_dict = {**asset_dict, **load_asset(item_path)}

    return asset_dict


current_dir = os.path.dirname(os.path.abspath(__file__))
# Constants
#   Game
DISPLAY_NAME = "Dino Game"
DISPLAY_FONT = os.path.join(current_dir, "PressStart2P-Regular.ttf")
FPS = 30
GAME_SPEED = 11 
GAME_SPEED_MAX = 20
ANIM_FRAME = 5
#   Assets
ASSET_FOLDER_PATH = os.path.join(current_dir, "Images")
ASSET_DICT = load_asset(ASSET_FOLDER_PATH)
#   Screen 
WIDTH = 1100
HEIGHT = 600
FULL_SCREEN = False
BACKGROUND = (255,255,255)
CLOUD_NUM = 3
FONT_SIZE = 20
#   Buttons
BUTTON_JUMP = "jump"
BUTTON_DUCK = "duck"
BUTTON_QUIT = "quit"
BUTTON_RESTART = "restart"
BUTTON_LIST = [BUTTON_JUMP, BUTTON_DUCK, BUTTON_QUIT, BUTTON_RESTART]
#   Player position
DINO_POSITION_X = HEIGHT / 7.5
DINO_POSITION_Y = WIDTH / 3.5 + 2
DINO_DUCK_POSITION_Y = DINO_POSITION_Y + 30
DINO_JUMPING = 8.5
DINO_JUMP_ACC = 5
DINO_JUMP_GRAV = 0.8
#   Backgorund position
BG_POSITION_X = 0
BG_POSITION_Y = 380
#   Object position
POSITION_OBJECT_X = 500
POSITION_S_CACTUS_Y = 325 + 2
POSITION_L_CACTUS_Y = 300 + 2
POSITION_BIRD_Y = 250
#   Score position
POSITION_SCORE_Y = 30
POSITION_SCORE_X = 950
POSITION_HIGH_SCORE_Y = 30
POSITION_HIGH_SCORE_X = 750
#   Restart position
POSITION_RESTART_Y = HEIGHT / 2
POSITION_RESTART_X = WIDTH / 2
