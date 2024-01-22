"""file used for player character creation (dinosaur)
"""

from Game_Karol_Warda.Constants import ASSET_DICT, DINO_POSITION_X,DINO_POSITION_Y, DINO_DUCK_POSITION_Y, BUTTON_JUMP, BUTTON_DUCK, ANIM_FRAME
from Game_Karol_Warda.Constants import DINO_JUMPING, DINO_JUMP_GRAV, DINO_JUMP_ACC
import pygame
from abc import ABC, abstractmethod
from typing import Dict, List

class Action(ABC):
    def __init__(self):
        """Initialize an Action object.

        Attributes:
            is_activated (bool): Indicates if the action is currently activated.
        """
        self.is_activated = False

    @abstractmethod
    def action(self, player) -> None:
        """Abstract method for defining the action behavior.

        Args:
            player: The player object to apply the action to.
        """
        pass

    def activate(self):
        """Activate the action."""
        self.is_activated = True
    def deactivate(self):
        """Deactivate the action."""
        self.is_activated = False

class Run(Action):
    def __init__(self, image: List[pygame.Surface]):
        """Initialize a Run action.

        Args:
            image (List[pygame.Surface]): List of images for the running action animation.
        """
        super().__init__()
        self.image = image

    def action(self, player):
        """Define the running action.

        Args:
            player: The player object.
        """
        player.image = self.image[player.draw_frame // ANIM_FRAME]

        player.draw_frame += 1

        player.rect = player.image.get_rect()
        player.rect.y = DINO_POSITION_Y
        player.rect.x = DINO_POSITION_X


class Duck(Action):
    def __init__(self, image: List[pygame.Surface]):
        """Initialize a Duck action.

        Args:
            image (List[pygame.Surface]): List of images for the ducking action animation.
        """
        super().__init__()
        self.image = image

    def action(self, player):
        """Define the ducking action.

        Args:
            player: The player object.
        """
        player.image = self.image[player.draw_frame // ANIM_FRAME]

        player.draw_frame += 1

        player.rect = player.image.get_rect()
        player.rect.y = DINO_DUCK_POSITION_Y
        player.rect.x = DINO_POSITION_X


class Jump(Action):
    def __init__(self, image: pygame.Surface):
        """Initialize a Jump action.

        Args:
            image (pygame.Surface): Image for the jumping action.
        """
        super().__init__()
        self.image = image
        self.velocity = DINO_JUMPING

    def action(self, player):
        """Define the jumping action.

        Args:
            player: The player object.
        """
        player.image = self.image

        if self.is_activated:
            player.rect.y = player.rect.y - self.velocity * DINO_JUMP_ACC
            self.velocity = self.velocity - DINO_JUMP_GRAV
        if abs(self.velocity) > DINO_JUMPING:
            self.deactivate()
            self.velocity = DINO_JUMPING


class ActionHandler:
    def __init__(self, player) -> None:
        """Initialize an ActionHandler object.

        Args:
            player: The player object.
        """
        self.player = player
        self.actions: Dict[str, Action] = {}
    
    def add_action(self, action: Action) -> None:
        """Add an action to the handler.

        Args:
            action (Action): The action to add.
        """
        if action is not None:
            name = action.__class__.__name__
            self.actions[name] = action

    def is_action_activated(self, actionType: str) -> bool:
        """Check if a specific action is currently activated.

        Args:
            actionType (str): The type of action to check.

        Returns:
            bool: True if the action is activated, False otherwise.
        """
        action = self.actions[actionType]
        return action.is_activated

    def handle(self, actionType: str) -> None:
        """Handle the activation (activate/deactivate) of a specific action.

        Args:
            actionType (str): The type of action to handle.
        """
        action = self.actions[actionType]
        if action is not None and not action.is_activated:
            action.activate()

            for value in self.actions.values():
                if value is not action:
                    value.deactivate()
    
    def activate(self):
        """Activate the current action for the player."""
        for value in self.actions.values():
            if value.is_activated:
                value.action(self.player)

class Dinosaur:
    def __init__(self):
        """Initialize a player object."""
        #assets
        self.duck_img = ASSET_DICT["DinoDuck"]
        self.run_img = ASSET_DICT["DinoRun"]
        self.jump_img = ASSET_DICT["DinoJump"]

        # current anim frame
        self.draw_frame = 0

        self.action_handler = ActionHandler(self)
        self.action_handler.add_action(Run(self.run_img))
        self.action_handler.add_action(Duck(self.duck_img))
        self.action_handler.add_action(Jump(self.jump_img[0]))

    def on_startup(self):
        """Perform additional actions when the game starts."""
        self.image = ASSET_DICT["Dino"][1] # idle state image
        self.rect = self.image.get_rect()
        self.rect.x = DINO_POSITION_X
        self.rect.y = DINO_POSITION_Y

    # use actionHandler here to set which action will be active
    def on_loop(self, input):
        """Update the Dinosaur's state based on user input.

        Args:
            input (dict): Dictionary representing the state of input buttons.
        """
        if input[BUTTON_JUMP] and not self.action_handler.is_action_activated("Jump"):
            self.action_handler.handle("Jump")
        elif input[BUTTON_DUCK] and not self.action_handler.is_action_activated("Jump"):
            self.action_handler.handle("Duck")
        elif not input[BUTTON_DUCK] and not self.action_handler.is_action_activated("Jump"):
            self.action_handler.handle("Run")

    def on_render(self, screen):
        """Render the Dinosaur on the screen.

        Args:
            screen: The screen to render on.
        """
        self.update()
        self.draw(screen)

    def update(self):
        """Update the player's state."""
        self.action_handler.activate()
        self.draw_frame = self.draw_frame % 10

    def draw(self, screen):
        """Draw the Dinosaur on the screen.

        Args:
            screen: The screen to draw on.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))