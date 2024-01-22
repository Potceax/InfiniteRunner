"""File used for all objects that are shown on the screen
"""


import pygame as pg
from pygame import display, Vector2
from typing import Any, List, Tuple, Type
from Object import Object, ObjectHandler, Bird
from Player import Dinosaur

import random
from Constants import WIDTH, HEIGHT, FULL_SCREEN, DISPLAY_NAME, BACKGROUND, ASSET_DICT
from Constants import BG_POSITION_X, BG_POSITION_Y, POSITION_S_CACTUS_Y, POSITION_L_CACTUS_Y, POSITION_BIRD_Y, CLOUD_NUM, DISPLAY_FONT
from Constants import POSITION_SCORE_Y, POSITION_SCORE_X, POSITION_RESTART_Y, POSITION_RESTART_X, POSITION_HIGH_SCORE_X, POSITION_HIGH_SCORE_Y, FONT_SIZE

class Cloud(pg.sprite.Sprite):
    def __init__(self, x, y):
        """Initialize Cloud instance.

        Args:
            x (int): Initial x-coordinate of the cloud.
            y (int): Initial y-coordinate of the cloud.
        """
        pg.sprite.Sprite.__init__(self)
        self.image = ASSET_DICT["Cloud"][0]

        #Rect and position
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.x = x + WIDTH
        self.y = y

        self.fixed_speed = random.randint(-1,0)

    def update(self, game_speed):
        """Update the cloud's position based on the game speed.

        Args:
            game_speed (int): Current game speed.
        """
        self.x = self.x - (game_speed + self.fixed_speed)
        if self.x < -self.width:
            self.y = random.randint(50, 150)
            self.x = random.randint(1000, 3000) + WIDTH

    def draw(self, screen):
        """Draw the cloud on the screen.

        Args:
            screen: The screen to draw on.
        """
        screen.blit(self.image, (self.x, self.y))


class UIElement:
    def __init__(self, x, y) -> None:
        """Initialize UIElement instance.

        Args:
            x (int): Initial x-coordinate of the UI element.
            y (int): Initial y-coordinate of the UI element.
        """
        self.x = x
        self.y = y

    def update(self, game):
        """Update the UI element.

        Args:
            game: The game instance.
        """
        pass

    def draw(self, screen):
        """Draw the UI element on the screen.

        Args:
            screen: The screen to draw on.
        """
        pass

class Score(UIElement):
    def __init__(self, x, y, size) -> None:
        """Initialize Score instance.

        Args:
            x (int): Initial x-coordinate of the score UI element.
            y (int): Initial y-coordinate of the score UI element.
            size (int): Font size for the score UI element.
        """
        super().__init__(x, y)
        self.score = 0
        self.font = pg.font.Font(DISPLAY_FONT, size)

        self.text = self.font.render("HI: " + str(self.score), True, (0,0,0))
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)

    def update(self, game, is_highScore: bool = False):
        """Update the score UI element.

        Args:
            game: The game instance.
            is_highScore (bool, optional): Whether to update high score. Defaults to False.
        """
        if is_highScore:
            self.score = game.hight_score
        else:
            self.score = game.score
        self.text = self.font.render("HI: " + str(self.score), True, (0,0,0))
    def draw(self, screen: pg.surface.Surface):
        """Draw the score UI element on the screen.

        Args:
            screen (pg.surface.Surface): The screen to draw on.
        """
        screen.blit(self.text, self.rect)


class Restart(UIElement):
    def __init__(self, x, y, img: pg.Surface, size) -> None:
        """Initialize Restart instance.

        Args:
            x (int): Initial x-coordinate of the restart UI element.
            y (int): Initial y-coordinate of the restart UI element.
            img (pg.Surface): Image for the restart UI element.
            size (int): Font size for the restart UI element.
        """
        super().__init__(x, y)
        self.font = pg.font.Font(DISPLAY_FONT, size)

        self.text = self.font.render("Press R to restart", True, (0,0,0))
        self.rect = self.text.get_rect()
        self.rect.center = (x,y)

        self.img = img
        self.img_rect = self.img.get_rect()
        self.img_rect.center = (x, y+ 75)

    def update(self, game):
        """Update the restart UI element.

        Args:
            game: The game instance.
        """
        pass

    def draw(self, screen: pg.Surface):
        """Draw the restart UI element on the screen.

        Args:
            screen (pg.Surface): The screen to draw on.
        """
        screen.blit(self.img, self.img_rect)
        screen.blit(self.text, self.rect)


class Screen:
    def __init__(self, player: Dinosaur) -> None:
        """Initialize Screen instance.

        Args:
            player (Dinosaur): The player's class.
        """
        # screen info - width, height and surface
        self.screen_info = display.Info()
        self.set_screen_size(WIDTH, HEIGHT, FULL_SCREEN)
        self.screen_surface = display.set_mode(self.screen_size)
        display.set_caption(DISPLAY_NAME)

        # background setup
        self.bg_pos = BG_POSITION_X

        # Player Info
        self.player = player
        # score UI
        self.score_ui = Score(POSITION_SCORE_X, POSITION_SCORE_Y, FONT_SIZE)
        self.high_score_ui = Score(POSITION_HIGH_SCORE_X, POSITION_HIGH_SCORE_Y, FONT_SIZE)
        self.restart_ui = Restart(POSITION_RESTART_X, POSITION_RESTART_Y, ASSET_DICT["Icons"][1], 10)

        # Object handler init
        self.object_handler: ObjectHandler = ObjectHandler(player)
        #   Cactus
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][0], POSITION_L_CACTUS_Y))
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][1], POSITION_L_CACTUS_Y))
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][2], POSITION_L_CACTUS_Y))
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][3], POSITION_S_CACTUS_Y))
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][4], POSITION_S_CACTUS_Y))
        self.object_handler.add_type((Object, ASSET_DICT["Cactus"][5], POSITION_S_CACTUS_Y))
        #   Bird
        self.object_handler.add_type((Bird, ASSET_DICT["Bird"], POSITION_BIRD_Y))

        # cloud init
        self.cloud_sprites: List[Cloud] = []
        for count in range(CLOUD_NUM):
            cloud = Cloud(random.randint(250,1000), random.randint(50,100))
            for other in self.cloud_sprites:
                other_v = Vector2()
                cloud_v = Vector2()

                other_v.xy = other.x, other.y
                cloud_v.xy = cloud.x, cloud_v.y
                if cloud_v.distance_to(other_v) < 300:
                    count -= 1
                    continue
            self.cloud_sprites.append(cloud)
        
        # load assets
        self.cloud = ASSET_DICT["Cloud"][0]
        self.track = ASSET_DICT["Background"][0]
        self.icons = ASSET_DICT["Icons"]   

        # display info
        # print("Screen width:", self.screen_size[0])
        # print("Screen height:", self.screen_size[1])

    def on_startup(self):
        """Create startup canvas for game
        """
        self.screen_surface.fill(BACKGROUND)
        self.screen_surface.blit(self.track, (self.bg_pos,BG_POSITION_Y))
        self.object_handler.create_object(how_much=2)


    def on_loop(self, game):
        """Update the screen in each game loop iteration.

        Args:
            game: The game instance.
        """
        if game.has_ended:
            return
        
        self.screen_surface.fill(BACKGROUND)
        self.object_handler.update(game.game_speed)
        if self.object_handler.collision_check():
            game.has_ended = True
            if game.hight_score < game.score:
                game.hight_score = game.score
            return

        #update score
        self.score_ui.update(game)
        self.high_score_ui.update(game, is_highScore=True)

        #draw clouds
        for cloud in self.cloud_sprites:
            cloud.draw(self.screen_surface)
        
        # get positions of the bg image
        img_width = self.track.get_width()
        self.bg_pos = self.bg_pos - game.game_speed

        # print bg on screen
        self.screen_surface.blit(self.track, (self.bg_pos,BG_POSITION_Y))
        self.screen_surface.blit(self.track, (self.bg_pos + img_width,BG_POSITION_Y))

        # loop the bg
        if abs(self.bg_pos) > img_width:
            self.bg_pos = 0
            self.screen_surface.blit(self.track, (self.bg_pos + img_width,BG_POSITION_Y))

    
    def on_render(self, game):
        """Render the screen.

        Args:
            game: The game instance.
        """
        if not game.has_ended:     
            self.object_handler.draw(self.screen_surface)
            #draw score
            self.score_ui.draw(self.screen_surface)
            self.high_score_ui.draw(self.screen_surface)

            #update clouds
            for cloud in self.cloud_sprites:
                cloud.update(game.game_speed)
        else:
            self.restart_ui.draw(self.screen_surface)

        display.update()

    def set_screen_size(self, width: float = 1, height: float = 1, is_fullscreen: bool = False):
        """
        Screen size settings

        Args:
            width (float, optional): screen width. Defaults to 1.
            height (float, optional): screen height. Defaults to 1.
            is_fullscreen (bool, optional): defines if game should be fullscreen. Defaults to False.
        """
        if(is_fullscreen):
            self.screen_size = [self.screen_info.current_w, self.screen_info.current_h]
        else:
            self.screen_size = [width, height]
    
    def set_background(self):
        """Set the background (placeholder)."""
        ...