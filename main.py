import sys
import pygame
import random
from pygame.locals import *

# Constants 
from utils import (
    blitlines,
    SCREEN_WIDTH, SCREEN_HEIGHT, 
    PLAYER_X, PLAYER_Y, 
    BLACKHOLE_X, BLACKHOLE_Y,
    FPS,
    IDLE, FLY_UP, FLY_LEFT, FLY_RIGHT,
    ASTEROID, BACKGROUND_IMAGE
)
# Classes
from utils import Player, Blackhole

from map import MAPS, parse_map, generate_random_map


debug_mode = False # press "p" key in-game to toggle. when enabled, radius of planets will be displayed


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
    elif keys[pygame.K_UP]:
        player.move("up")
    else:
        player.move("idle")

    if player.game_state == "lost":
        return False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw(screen, player, background, objects, player_time):
    """
    Draw objects to the screen. Called once per frame.
    """
    distance_from_blackhole = (abs(player.y - BLACKHOLE_Y)**2 + abs(player.x - BLACKHOLE_X)**2) ** 0.5 * 10
    screen.blit(background, (0, 0))  # Draw the background
    font = pygame.font.SysFont("Comic Sans MS", 20)
    screen.blit(
            font.render(f'DEV: Speed {round(player.gravity, 2)}', True, (255, 255, 255)), 
            (SCREEN_WIDTH/1.23, 5)
        )
    screen.blit(
            font.render(f'Time elapsed: {round(player_time, 1)}s', True, (255, 255, 255)), 
            (20, 20)
        )
    screen.blit(
            font.render(f"""Distance from blackhole {
round(distance_from_blackhole, 2)
}km""", True, (255, 255, 255)
), 
            (20, 50)
        )
    for obj in objects:
        obj.draw(screen, debug_mode=debug_mode)
    
    # return change in time (depending on blackhole distance)
    return 1/FPS * min(1, (player.gravity ** 4))#((distance_from_blackhole**2)/(10000**2))


def main():
    pygame.init()

    while True:
        clock = pygame.time.Clock()

        # Set up the window
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load images
        background = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

        num_planets = random.randint(8, 10)  # Random number of planets
        min_radius, max_radius = 80, 150  # Define min and max radius for planets
        generated_planets = parse_map(random.choice(MAPS))
        blackhole = Blackhole(BLACKHOLE_X, BLACKHOLE_Y, image="assets/blackhole.png") # Blackhole should be slightly below the visible screen
        planets = generated_planets
        # index 0 is list of objects, index 1 is list of coordinates

        # Set up game objects
        player = Player(PLAYER_X, PLAYER_Y, image=IDLE)
        objects = generated_planets + [player] + [blackhole]

        # Game loop
        dt = 1 / FPS

        # Home screen
        font_title = pygame.font.Font("assets/font.ttf", 40)
        font_normal = pygame.font.SysFont("Comic Sans MS", 25)
        font_small = pygame.font.SysFont("Comic Sans MS", 18)

        # Get highscore
        with open("highscore.txt", "r") as f:
            highscore = float(f.readline())        

        run_start_screen = True
        floater = Player(10, 200, IDLE)
        while run_start_screen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run_start_screen = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            screen.blit(background, (0,0))
            title = font_title.render("SINGULARITY X NYRCS", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5))
            screen.blit(title, title_rect)

            start_text = font_normal.render("Press any key to start", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.6))
            screen.blit(start_text, start_text_rect)

            start_text = font_small.render(f"Highscore: {highscore}s", True, (255, 255, 255))
            screen.blit(start_text, (20, 20))

            blitlines(
                screen, 
                """
Questions:
1. Why does time slow down?
2. Why does the player turn red?""",
                font_normal, 
                (255, 255, 255), 
                SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2
                )
            
            blitlines(
                screen, 
                """Devs: E-Ket and Zhi Rui
Artists: Ethan and Kia Leng""",
                font_small, 
                (255, 255, 255), 
                SCREEN_WIDTH / 1.22, SCREEN_HEIGHT / 1.1
                )
            
            # center = floater.x-floater.image.get_size()[0]/2, floater.y-floater.image.get_size()[1]/2
            # floater.states["idle"] = pygame.transform.rotate(floater.states["idle"], 2)
            # floater.rect = floater.states["idle"].get_rect(center=floater.rect.center)
            # screen.blit(floater.states["idle"], floater.rect)
            # floater.draw(screen, redshift=False)
            pygame.display.flip()

            dt = clock.tick(FPS)

        # Main game
        player_time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(f"DEBUG: Mouse position: {pygame.mouse.get_pos()}")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    print(f"DEBUG MODE TOGGLED")
                    global debug_mode
                    debug_mode = not debug_mode
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            try:
                update(dt, player, planets, blackhole)
                if player.game_state != "playing": #player wins or lost
                    break
                player_time += draw(screen, player, background, objects, player_time)
            except Exception:
                pass
            pygame.display.flip()
            dt = clock.tick(FPS)


        if player.game_state == "lost":
            screen.blit(background, (0, 0))

            start_text = font_normal.render("You lost...", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5))
            screen.blit(start_text, start_text_rect)

            start_text = font_normal.render("Press any key to go back home!", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5))
            screen.blit(start_text, start_text_rect)

        elif player.game_state == "won":
            player_time = round(player_time, 1)

            # Update highscore
            if player_time < highscore:
                with open("highscore.txt", "w") as f:
                    f.write(str(player_time))

            screen.blit(background.convert(), (0, 0))

            start_text = font_normal.render("YOU WIN", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
            screen.blit(start_text, start_text_rect)

            start_text = font_normal.render(f"Time taken: {player_time}s", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.8))
            screen.blit(start_text, start_text_rect)

            start_text = font_normal.render("Press any key to go back home", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))
            screen.blit(start_text, start_text_rect)
        
        pygame.display.flip()
        
        run_exit_screen = True
        while run_exit_screen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run_exit_screen = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = clock.tick(FPS)

if __name__ == "__main__":
    main()
