import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Mountain")

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)

# Function to draw a single peak of the mountain
def draw_peak(surface, color, x, y, height):
    pygame.draw.polygon(surface, color, [(x, y), (x + height, y - height * 2), (x + height * 2, y)], 0)

# Function to draw the mountain with multiple peaks
def draw_mountain(surface):
    x = -300
    y = screen_height - 100
    for i in range(10):
        height = random.randint(100, 300)
        color = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
        draw_peak(surface, color, x, y, height)
        x += 100
        y += random.randint(-50, 50)

# Function to move the mountain to the left
def move_mountain(surface):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SKY_BLUE)
        draw_mountain(surface)
        pygame.display.flip()
        surface.scroll(-2, 0)
        clock.tick(60)

# Main function
def main():
    surface = pygame.Surface((screen_width * 2, screen_height))
    move_mountain(surface)

if __name__ == "__main__":
    main()
