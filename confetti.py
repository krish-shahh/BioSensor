import pygame
import random

# Initialize Pygame
pygame.init()
infoObject = pygame.display.Info()  # Fetch the current screen resolution
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Confetti Simulation")
clock = pygame.time.Clock()

# Confetti class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size = random.randint(5, 15)

    def fall(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Create a list to hold confetti particles
confetti_list = [Confetti(random.randint(0, infoObject.current_w), random.randint(-400, 0)) for _ in range(100)]

def draw():
    screen.fill((0, 0, 0))  # Clear the screen with black
    for confetti in confetti_list:
        confetti.fall()
        confetti.draw(screen)
        # Reset confetti when it falls out of view
        if confetti.y > infoObject.current_h:  # Use screen height for reset
            confetti.y = random.randint(-50, 0)
            confetti.x = random.randint(0, infoObject.current_w)  # Use screen width
    pygame.display.flip()  # Update the full display

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for ESC key
                    running = False

        draw()
        clock.tick(30)  # Limit to 30 frames per second

    pygame.quit()

if __name__ == '__main__':
    main()
