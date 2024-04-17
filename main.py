import sys

import pygame
from pygame.locals import *
from utils import Player


PLAYER_X, PLAYER_Y = 50, 50

 
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

    # Loop through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            
 

def draw(screen, player):
    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((0, 0, 0)) # Fill the screen with black.
    
    player.draw(screen)
    
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def main():
    
    pygame.init()
    
    fps = 60.0
    clock = pygame.time.Clock()
    
    # Set up the window.
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    # Set up game
    player = Player(PLAYER_X, PLAYER_Y, image="test_player.png")
    
    # Game loop
    dt = 1/fps # dt is the time since last frame.
    while True: # Loop forever!
        update(dt, player)
        draw(screen, player)
        
        dt = clock.tick(fps)


main()