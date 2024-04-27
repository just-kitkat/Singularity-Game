from typing import List
import pygame

# Constants
PLAYER_MOVEMENT_SHIFT = 2 # velocity of player
INITIAL_GRAVITY = 0.3
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 697
PLAYER_X, PLAYER_Y = SCREEN_WIDTH / 2, 50
BLACKHOLE_X, BLACKHOLE_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT + 20
FPS = 30

# Assets
BACKGROUND_IMAGE = "background.jpg"
IDLE = "assets/idle.png"
FLY_UP = "assets/fly_up.png"
FLY_LEFT = "assets/fly_left.png"
FLY_RIGHT = "assets/fly_right.png"
ASTEROID = "assets/asteroid.png"


class Player:
    def __init__(self, x: int, y: int, image: str) -> None:
        self.x = x
        self.y = y
        self.state = "idle"
        self.player_action = False
        # Load assets
        states = {
            "idle": pygame.image.load(IDLE),
            "fly_up": pygame.image.load(FLY_UP),
            "fly_left": pygame.image.load(FLY_LEFT),
            "fly_right": pygame.image.load(FLY_RIGHT),
        }
        n = 6.5 # scale factor for astronaut
        for state in states:
            states[state] = pygame.transform.scale(states[state], (states[state].get_width()/n, states[state].get_height()/n))
        self.image = states["idle"]
        self.image_rect = self.image.get_rect()
        self.gravity = INITIAL_GRAVITY
        self.states = states

    def move(self, dir: str) -> None:
        """
        When the user moves the player
        """
        if dir == "left":
            self.x -= PLAYER_MOVEMENT_SHIFT
            self.state = "fly_left"
            self.player_action = True
        elif dir == "right":
            self.x += PLAYER_MOVEMENT_SHIFT
            self.state = "fly_right"
            self.player_action = True
        else:
            self.state = "idle"
            self.player_action = False
        

    def float(self, planets: List[List[int]], blackhole) -> None:
        """
        Handles normal player movement
        planets -- [[x, y, radius], ...]
        """

        # Brute force nearest planet (if any)
        nearest_planet = None
        for planet in planets[1]:
            x, y, radius = planet
            if (abs(self.x - x)**2 + abs(self.y - y)**2)**0.5 < radius:
                nearest_planet = planet
        
        if nearest_planet is not None: # Planet exists
            p_X, _, _ = nearest_planet

            # Move toward the planet (x-axis)
            if p_X > self.x: self.x += 0.5
            elif p_X < self.x: self.x -= 0.5

        else:
            # Gravitate sideways towards the blackhole below
            if blackhole.x > self.x: self.x += abs(self.x - BLACKHOLE_X) / abs(self.y - BLACKHOLE_Y)
            elif blackhole.x < self.x: self.x -= abs(self.x - BLACKHOLE_X) / abs(self.y - BLACKHOLE_Y)

        # If player is able to move down (no planet or planet below)
        if nearest_planet is None:
            self.y += self.gravity
            self.state = "idle"
        elif nearest_planet[1] > self.y:
            self.y += abs(self.y - nearest_planet[1]) // abs(self.x - p_X)
        elif self.x - p_X != 0: # check for division by 0
            # Move upwards to the planet slowly (proportional to dist from planet)
            self.y -= abs(self.y - nearest_planet[1]) // abs(self.x - p_X)

    
    def draw(self, screen):
        """
        Draws the player onto the screen
        """
        self.image = self.states[self.state]
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
        self.state = "planet"
        self.states = {"planet": pygame.image.load("circle.jpg")}
        self.states["planet"] = pygame.transform.scale(self.states["planet"], (30, 30))
        self.image = self.states["planet"]
        self.radius = radius

    def draw(self, screen):
        super().draw(screen)
        # pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)

    def get_coords_and_radius(self):
        """
        Returns the coordinates (x, y) and radius of the planet.
        """
        return [self.x, self.y, self.radius]
