import random
from Game_Karol_Warda.Player import Dinosaur
from pygame import Surface, surface
from typing import List, Tuple, Type
from Game_Karol_Warda.Constants import WIDTH, ANIM_FRAME, POSITION_OBJECT_X, GAME_SPEED_MAX

class Object:
    def __init__(self, img: surface.Surface, pos_y: int, pos_x: int = 0) -> None:
        """Initialize Object instance.

        Args:
            img (surface.Surface): The image of the object.
            pos_y (int): The y-coordinate of the object.
            pos_x (int, optional): The x-coordinate of the object. Defaults to 0.
        """
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.x_dist = pos_x
        self.rect.x = WIDTH + GAME_SPEED_MAX * 16 + pos_x

    def update(self, game_speed: int):
        """Update the object's position based on the game speed.

        Args:
            game_speed (int): Current game speed.
        """
        self.rect.x = self.rect.x - game_speed
    
    def draw(self, screen: surface.Surface, pos) -> None:
        """Draw the object on the screen.

        Args:
            screen (surface.Surface): The screen to draw on.
            pos: Position tuple for drawing.
        """
        screen.blit(self.image, pos)

class Bird(Object):
    def __init__(self, img: List[Surface], pos_y: int, pos_x: int = 0) -> None:
        """Initialize Bird instance.

        Args:
            img (List[Surface]): List of images for animation.
            pos_y (int): The y-coordinate of the bird.
            pos_x (int, optional): The x-coordinate of the bird. Defaults to 0.
        """
        super().__init__(img[0], pos_y, pos_x)
        self.image = img
        self.draw_frame = 0
    
    def draw(self, screen: Surface, pos):
        """Draw the bird on the screen with animation.

        Args:
            screen (Surface): The screen to draw on.
            pos: Position tuple for drawing.
        """
        self.draw_frame = self.draw_frame % 10
        screen.blit(self.image[self.draw_frame // ANIM_FRAME], pos)
        self.draw_frame = self.draw_frame + 1


class ObjectHandler:
    def __init__(self, player: Dinosaur) -> None:
        """Initialize ObjectHandler instance.

        Args:
            player (Dinosaur): The player's class
        """
        self.object_type_list: List[Tuple[Type[Object], surface.Surface, int]] = []
        self.object_list: List[Object] = []

        if player is not None:
            self.player: Dinosaur = player  

        self.game_speed = 0
    
    def add_type(self, type_t: Tuple[Type[Object], surface.Surface, int]) -> None:
        """Add tuple type that is not in the type_list to list

        Args:
            type_t (Tuple[Type[Object], surface.Surface]): tuple type to add
        """
        if not type_t in self.object_type_list:
            self.object_type_list.append(type_t)

    def add_types(self, type_t: List[Tuple[Type[Object], surface.Surface, int]]) -> None:
        """join the argument list with the tuple type list

        Args:
            type_t (List[Tuple[Type[Object], surface.Surface]]): type list to join
        """
        self.object_type_list = list(set(type_t + self.object_type_list))

    def create_object(self, how_much: int = 1, is_init: bool = True, prev_x: int = 0) ->None:
        """Take a random tuple from the object_type_list and create an object from it.

        Args:
            how_much (int, optional): Number of objects to create. Defaults to 1.
            is_init (bool, optional): Whether it is the initial object creation. Defaults to True.
            prev_x (int, optional): Previous x-coordinate. Defaults to 0.
        """
        for _ in range(how_much):
            # list is full (ONLY 2 OBJECTS) 
            if len(self.object_list) == 2:
                return

            # choose random object type
            random_object = random.choice(self.object_type_list)
            if len(self.object_list) == 0: # first object placement
                # Generate the tuple(object, distance) and put it into a queue
                self.object_list.append(random_object[0](random_object[1], random_object[2], 0))
            elif len(self.object_list) >= 1: # 2nd object placement
                #calculate distance between objects before pop
                obj_dist = abs(prev_x - self.object_list[0].rect.x)
                multiplayer = self.game_speed * 15
                if is_init:                  # check if objects are build at the startup
                    dist =  500
                elif not is_init and obj_dist <= 300 + multiplayer: # small end dist == bigger gap for 2nd object
                    dist = random.randint(-GAME_SPEED_MAX * 16, -multiplayer - GAME_SPEED_MAX)
                elif not is_init and obj_dist > 300 + multiplayer:  # normal dist distribution
                    dist = random.randint(GAME_SPEED_MAX + multiplayer, GAME_SPEED_MAX * 16)
                self.object_list.append(random_object[0](random_object[1], random_object[2], dist))


    def collision_check(self) -> bool:
        """Check each obj element in object_list for player collision.

        Returns:
            bool: Whether collision is detected.
        """
        for obj  in self.object_list:
            if self.player.rect.colliderect(obj.rect):
                return True
            
        return False
        
    
    def update(self, game_speed: int) -> None:
        """update every object in the list
           if they are out of the screen drop them from the list

        Args:
            game_speed (int): current game speed
        """
        self.game_speed = game_speed
        for obj in self.object_list:
            obj.update(game_speed)
            if obj.rect.x < - obj.rect.width:
                
                self.create_object(is_init=False, prev_x=self.object_list.pop(0).rect.x)


    def draw(self, screen: surface.Surface) ->None:
        """Draw every object in the list
            Args:
            screen (surface.Surface): Screen to add to
        """
        for obj in self.object_list:
            obj.draw(screen, (obj.rect.x, obj.rect.y))