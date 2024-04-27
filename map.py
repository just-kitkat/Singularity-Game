import pygame
import random
from utils import BACKGROUND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT, Planet


def generate_random_map(num_planets, min_radius, max_radius):
    """
    Generate a random map with non-colliding planets.
    """
    pygame.init()

    # Set up the window
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load background image
    background = pygame.image.load(BACKGROUND_IMAGE).convert()

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
        return [Planet(x, y, "circle.jpg", radius) for x, y, radius in planet_coords], planet_coords

    # Generate random map
    planets = create_planets()

    return planets

if __name__ == "__main__":
    # Example usage:
    num_planets = random.randint(5, 10)  # Random number of planets
    min_radius, max_radius = 20, 50  # Define min and max radius for planets
    generated_planets = generate_random_map(num_planets, min_radius, max_radius)
    print(len(generated_planets), "planets generated.")
