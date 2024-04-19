from typing import List
import pygame

PLAYER_MOVEMENT_SHIFT = 2 # velocity of player
INITIAL_GRAVITY = 1


class Player:
    def __init__(self, x: int, y: int, image: str) -> None:
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.image_rect = self.image.get_rect()
        self.gravity = INITIAL_GRAVITY

    def move(self, dir: str) -> None:
        """
        When the user moves the player
        """
        if dir == "left":
            self.x -= PLAYER_MOVEMENT_SHIFT
        elif dir == "right":
            self.x += PLAYER_MOVEMENT_SHIFT
        else:
            raise ValueError(f"Invalid direction: {dir}")
        

    def float(self, planets: List[List[int]]) -> None:
        """
        Handles normal player movement
        planets -- [[x, y, radius], ...]
        """

        # Brute force nearest planet (if any)

        # If planet not above player, move down by `gravity`
        if 1: # temp condition
            self.y += self.gravity

        
        # Move toward the planet (if any)

        # Gravitate downwards  and sideways towards the blackhole below 
        # (if player did not move up)

    
    def draw(self, screen):
        """
        Draws the player onto the screen
        """
        self.image_rect.x, self.image_rect.y = self.x, self.y
        screen.blit(self.image, self.image_rect)

class Blackhole(Player):
    """
    The blackhole should be a large circle with only 1/4 of 
    it visible from the bottom of the screen.
    """
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

class Planet(Player):
    """
    Planet should be a small circle with a predefined radius indicating the area of effect
    """
    def __init__(self, x: int, y: int, image: str, radius: int) -> None:
        super().__init__(x, y, image)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.radius = radius

    def draw(self, screen):
        super().draw(screen)
        # pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)

    def get_coords_and_radius(self):
        """
        Returns the coordinates (x, y) and radius of the planet.
        """
        return [self.x, self.y, self.radius]
