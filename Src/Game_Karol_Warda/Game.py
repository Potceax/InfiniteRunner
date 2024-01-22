"""Main file of the module, used to create game instance
"""

import pygame

import os
import sys

game_path = sys.path.insert(0, os.path.abspath(".."))

import Game_Karol_Warda.Player as Player
from Game_Karol_Warda.Constants import ASSET_DICT, BACKGROUND, FPS, GAME_SPEED, GAME_SPEED_MAX, BUTTON_RESTART, BUTTON_QUIT
from Game_Karol_Warda.Screen import Screen
from Game_Karol_Warda.Input import InputHandler

class Game:
    def __init__(self) -> None:
        """Initialize the Game object."""
        pygame.init()

        self.is_running = True
        self.has_started = False
        self.has_ended = False
        self.clock = pygame.time.Clock()
        self.game_speed = GAME_SPEED
        self.score = 0
        self.hight_score = 0

        self.screen: Screen = None
        self.input: InputHandler = None
        self.player: Player.Dinosaur = None
    
    def on_init(self) -> None:
        """Initialize additional variables."""
        self.has_ended = False
        self.has_started = False
        self.game_speed = GAME_SPEED
        self.score = 0

        self.player = Player.Dinosaur()
        self.input = InputHandler()
        self.screen = Screen(self.player)
        
        self.input.on_startup()
        self.screen.on_startup()
        self.player.on_startup()
    
    def on_event(self, event):
        """Handle events during the game.

        Args:
            event: The event to handle.
        """
        if event.type == pygame.QUIT:
            self.is_running = False
        if event.type == pygame.KEYDOWN and not self.has_started: # first input starts the game
            self.has_started = True

        if event.type == pygame.KEYDOWN and self.has_started and self.has_ended: # first input starts the game            
            key = self.input.get_keyboard_input()
            if key[BUTTON_RESTART]:
                self.on_init()
            
        if event.type == pygame.KEYDOWN:
            key = self.input.get_keyboard_input()
            if key[BUTTON_QUIT]:
                self.is_running = False


    def on_loop(self):
        """Update the game state in each game loop iteration."""
        self.clock.tick(FPS) # 30 fps

        # add speed
        if self.has_started and not self.has_ended:
            if self.score % 100 == 0 and self.game_speed < GAME_SPEED_MAX:
                self.game_speed = self.game_speed + 1

            key = self.input.get_keyboard_input()
            self.player.on_loop(key)

            self.screen.on_loop(self)
            self.score = self.score + 1


    def on_render(self):
        """Render the game state."""
        if not self.has_ended:
            self.player.on_render(self.screen.screen_surface)
            self.screen.on_render(self)
        else:
            self.screen.on_render(self)

    
    def on_cleanup(self):
        """Clean up and quit the game."""
        pygame.quit()
        self.is_running = False

    def on_exec(self):
        """Execute the main game loop.
        This function initializes the game, enters a loop to handle events, update the game state, and render the screen,
        and finally cleans up before exiting the loop.
        """
        if self.on_init() == False:
            self.is_running = False
        while(self.is_running):
            for event in pygame.event.get():
                self.on_event(event)

            # check if QUIT was executed
            if self.is_running == False:
                break

            self.on_loop()
            self.on_render()
        self.on_cleanup()

def play():
    """Main function to activate the game
    """
    game = Game()
    game.on_exec()


if __name__ == "__main__":
    play()

