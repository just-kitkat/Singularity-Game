import sys
import pygame
import random
from pygame.locals import *

# Constants 
from utils import (
    SCREEN_WIDTH, SCREEN_HEIGHT, 
    PLAYER_X, PLAYER_Y, 
    BLACKHOLE_X, BLACKHOLE_Y,
    FPS,
    IDLE, FLY_UP, FLY_LEFT, FLY_RIGHT,
    ASTEROID, BACKGROUND_IMAGE
)
# Classes
from utils import Player, Blackhole

from map import generate_random_map


def update(dt, player, planets, blackhole_coords):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary.
    """
    player.float(planets, blackhole_coords)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    elif keys[pygame.K_RIGHT]:
        player.move("right")
    else:
        player.move("idle")

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

    # Load images
    background = pygame.image.load("background.jpg").convert()

    num_planets = random.randint(8, 10)  # Random number of planets
    min_radius, max_radius = 80, 150  # Define min and max radius for planets
    generated_planets = generate_random_map(num_planets, min_radius, max_radius)
    blackhole_coords = Blackhole(BLACKHOLE_X, BLACKHOLE_Y, image="circle.jpg") # Blackhole should be slightly below the visible screen
    # index 0 is list of objects, index 1 is list of coordinates

    # Set up game objects
    player = Player(PLAYER_X, PLAYER_Y, image=IDLE)
    objects = generated_planets[0] + [player]

    # Game loop
    dt = 1 / FPS

    # Home screen
    font = pygame.font.Font("assets/font.ttf", 45)
    screen.blit(
        pygame.image.load(BACKGROUND_IMAGE).convert(),
        (0, 0)
    )
    screen.blit(
        font.render('SINGULARITY', True, (255, 255, 255)), 
        (SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 3)
    )
    screen.blit(
        font.render('PRESS ANY KEY TO START', True, (255, 255, 255)), 
        (SCREEN_WIDTH / 3.75, SCREEN_HEIGHT / 2)
    )
    pygame.display.flip()

    while True:
        # print(list(pygame.key.get_pressed()))
        flag = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                flag = 1
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if flag: break
        dt = clock.tick(FPS)

    # Main game
    while True:
        update(dt, player, generated_planets, blackhole_coords)
        draw(screen, background, objects)
        pygame.display.flip()
        dt = clock.tick(FPS)

if __name__ == "__main__":
    main()
