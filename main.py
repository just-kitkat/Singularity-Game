import sys
import pygame
import random
from pygame.locals import *
from utils import Player, Planet
from map import generate_random_map

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 697
PLAYER_X, PLAYER_Y = 50, 50
FPS = 60.0

def update(dt, player):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary.
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    elif keys[pygame.K_RIGHT]:
        player.move("right")

    player.float([])

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw(screen, background, objects):
    """
    Draw objects to the screen. Called once per frame.
    """
    screen.blit(background, (0, 0))  # Draw the background
    for obj in objects:
        obj.draw(screen)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load background image
    background = pygame.image.load("background.jpg").convert()

    num_planets = random.randint(5, 10)  # Random number of planets
    min_radius, max_radius = 20, 50  # Define min and max radius for planets
    generated_planets = generate_random_map(num_planets, min_radius, max_radius)
    # index 0 is list of objects, index 1 is list of coordinates

    # Set up game objects
    player = Player(PLAYER_X, PLAYER_Y, image="test_player.png")
    objects = generated_planets[0] + [player]

    # Game loop
    dt = 1 / FPS
    while True:
        update(dt, player)
        draw(screen, background, objects)
        pygame.display.flip()
        dt = clock.tick(FPS)

if __name__ == "__main__":
    main()
