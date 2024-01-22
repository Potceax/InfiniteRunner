"""File for input handle
"""

import pygame
from Constants import BUTTON_JUMP, BUTTON_DUCK, BUTTON_QUIT, BUTTON_RESTART

class InputHandler:
    def __init__(self):
        """Initialize InputHandler instance.

        Initialize and setup joysticks for input handling.
        """
        #joystick prep
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()


    def on_startup(self):
        ...


    def get_keyboard_input(self):
        """Get the state of keyboard input.

        Returns:
            dict: A dictionary representing the state of keyboard input for specified buttons.
                  Keys are button constants, and values are boolean indicating whether the button is pressed.
        """
        keys = pygame.key.get_pressed()
        return {
            BUTTON_JUMP: keys[pygame.K_SPACE],
            BUTTON_DUCK: keys[pygame.K_s],
            BUTTON_RESTART: keys[pygame.K_r],
            BUTTON_QUIT: keys[pygame.K_ESCAPE]
        }