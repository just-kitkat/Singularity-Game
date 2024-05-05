from typing import List
import pygame

# Constants
PLAYER_MOVEMENT_SHIFT = 2 # velocity of player
INITIAL_GRAVITY = 1.4
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768
PLAYER_X, PLAYER_Y = SCREEN_WIDTH / 2, 50
BLACKHOLE_X, BLACKHOLE_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT + 30
FPS = 30

# Assets
BACKGROUND_IMAGE = "assets/background.jpg"
IDLE = "assets/player/idle.png"
FLY_UP = "assets/player/fly_up.png"
FLY_LEFT = "assets/player/fly_left.png"
FLY_RIGHT = "assets/player/fly_right.png"
ASTEROID = "assets/asteroid.png"


def blitlines(surf, text, renderer, color, x, y):
    """
    Renders multiple lines on the surface at once
    """
    h = renderer.get_height()
    lines = text.split('\n')
    for i, ll in enumerate(lines):
        txt_surface = renderer.render(ll, True, color)
        surf.blit(txt_surface, (x, y+(i*h*1.2)))


class Player():
    def __init__(self, x: int, y: int, image: str) -> None:
        self.x = x
        self.y = y
        self.state = "idle"
        self.id = "player"
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.gravity = INITIAL_GRAVITY
        self.states = states
        self.game_state = "playing"


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
        

    def float(self, planets, blackhole) -> None:
        """
        Handles normal player movement
        planets -- [[x, y, radius], ...]
        """

        # Brute force nearest planet (if any)
        nearest_planet = None
        for planet in [(i.x, i.y, i.radius) for i in planets]:
            x, y, radius = planet
            if (abs(self.x - x)**2 + abs(self.y - y)**2)**0.5 < radius:
                nearest_planet = planet
        
        # Check if player has reached blackhole
        if self.y > BLACKHOLE_Y//2 and pygame.sprite.collide_mask(self, blackhole):
            self.game_state = "won"
            return

        if nearest_planet is not None: # Planet exists
            p_X, p_Y, _ = nearest_planet

            # Check for collision
            for planet in planets:
                if pygame.sprite.collide_mask(self, planet):
                    self.game_state = "lost"
                    return

            # Move toward the planet (x-axis)
            if p_X > self.x: self.x += abs(self.x - nearest_planet[0]) / abs(self.x - p_X)
            elif p_X < self.x: self.x -= abs(self.x - nearest_planet[0]) / abs(self.x - p_X)

        else:
            # Gravitate sideways towards the blackhole below
            if BLACKHOLE_X > self.x: self.x += 1 * (abs(self.x - BLACKHOLE_X) / max(0.01, abs(self.y - BLACKHOLE_Y)))
            elif BLACKHOLE_X < self.x: self.x -= 1 * (abs(self.x - BLACKHOLE_X) / max(0.01, abs(self.y - BLACKHOLE_Y)))

        # If player is able to move down (no planet or planet below)
        self.gravity = max(0.4, INITIAL_GRAVITY * (abs((abs(self.y - BLACKHOLE_Y)**2 + abs(self.x - BLACKHOLE_X)**2) ** 0.5) / BLACKHOLE_Y))
        if nearest_planet is None:
            self.y += self.gravity
            self.state = "idle"
        elif nearest_planet[1] > self.y:
            self.y += abs(self.y - nearest_planet[1]) / abs(self.y - p_Y)
        else:
            # Move upwards to the planet slowly (proportional to dist from planet)
            self.y -= abs(self.y - nearest_planet[1]) / abs(self.y - p_Y)

    
    def draw(self, screen):
        """
        Draws the player onto the screen
        """
        self.image = self.states[self.state].convert_alpha()
        if self.id == "player":
            self.image.fill(
                (min(255, round(255 * (BLACKHOLE_Y/(abs(self.y-BLACKHOLE_Y)+120) - 0.9), 0)), 0, 0, 0),
                special_flags=pygame.BLEND_ADD
            )
        image_size = self.image.get_size()
        self.rect.x, self.rect.y = self.x - image_size[0]/2, self.y - image_size[1]/2
        screen.blit(self.image, self.rect)


class Blackhole(Player):
    """
    The blackhole should be a large circle with only 1/4 of 
    it visible from the bottom of the screen.
    """
    def __init__(self, x: int, y: int, image: str) -> None:
        # Redifine coords
        x, y = BLACKHOLE_X, BLACKHOLE_Y
        super().__init__(x, y, image)
        self.state = "blackhole"
        self.id = "blackhole"
        self.states = {"blackhole": pygame.image.load(image)}
        self.states[self.state] = pygame.transform.scale(self.states[self.state], (1000, 400))
        self.image = self.states["blackhole"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()


class Planet(Player):
    """
    Planet should be a small circle with a predefined radius indicating the area of effect
    """
    def __init__(self, x: int, y: int, image: str, radius: int) -> None:
        super().__init__(x, y, image)
        self.state = "planet"
        self.id = "planet"
        self.states = {"planet": pygame.image.load(image)}
        # self.states["planet"] = pygame.transform.scale(self.states["planet"], (30, 30))
        scale = 5 # scale factor for astronaut
        for state in self.states:
            n = scale if image.split("/")[2][0] not in "678" else scale-2
            add = (-1 if radius-100<0 else 1) * (((radius - 100)/5.5) ** 2)
            self.states[state] = pygame.transform.scale(
                self.states[state], 
                (
                    self.states[state].get_width()/n + add, 
                    self.states[state].get_height()/n + add
                )
            )
        self.image = self.states["planet"]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = radius

    def draw(self, screen):
        # Debug: display planet radius
        # pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, width=1)

        super().draw(screen)

    def get_coords_and_radius(self):
        """
        Returns the coordinates (x, y) and radius of the planet.
        """
        return [self.x, self.y, self.radius]
