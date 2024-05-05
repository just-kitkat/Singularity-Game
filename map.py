import pygame
import random
from typing import List
from utils import BACKGROUND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT, Planet


MAPS: List[List[List[int]]] = [
    # Map 1
    [
        [750, 250, 150],
        [840, 420, 80],
        [950, 450, 80],
        [1090, 650, 125],
        [1100, 220, 120],
        [350, 250, 100],
        [600, 180, 100],
        [520, 500, 170],
        [200, 450, 100],
    ]
]


def parse_map(map):
    # Planet(x, y, image, radius)
    return [Planet(i[0], i[1], f"assets/planets/{random.randint(1,8)}.png", i[2]) for i in map]


def generate_random_map(num_planets, min_radius, max_radius):
    """
    Generate a random map with non-colliding planets.
    """
    pygame.init()

    # Set up the window
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def generate_non_colliding_coords():
        """
        Generate random non-colliding coordinates for planets.
        """
        planets = []
        while len(planets) < num_planets:
            x = random.randint(max_radius, SCREEN_WIDTH - max_radius)
            y = random.randint(max_radius, SCREEN_HEIGHT - max_radius)
            radius = random.randint(min_radius, max_radius)
            new_planet = [x, y, radius]
            # Check if the new planet collides with existing planets
            if all(((x - px) ** 2 + (y - py) ** 2) >= (radius + pr) ** 2 for px, py, pr in planets):
                planets.append(new_planet)
        return planets

    def create_planets():
        """
        Create Planet objects from generated coordinates.
        """
        planet_coords = generate_non_colliding_coords()
        return [Planet(x, y, f"assets/planets/{random.randint(1,9)}.png", radius) for x, y, radius in planet_coords]

    # Generate random map
    planets = create_planets()
    print()
    return planets

if __name__ == "__main__":
    # Example usage:
    num_planets = random.randint(5, 10)  # Random number of planets
    min_radius, max_radius = 20, 50  # Define min and max radius for planets
    generated_planets = generate_random_map(num_planets, min_radius, max_radius)
    print(len(generated_planets), "planets generated.")
