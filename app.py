import grandeur.device as grandeur
import time
import threading
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), FULLSCREEN)
pygame.display.set_caption('Heart Rate Monitor')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.Font(None, 36)

# Define the apiKey and Auth token
apiKey = "grandeurlvcg71200dja0jifadqx7zug"
token = "37460718c7b237cd5a252abdcf184677a881d8ef029fe20d75e5252ebe2c8a3e"
deviceID = "devicelvciwtip0isa0jif5kes0tb9"

# Event listener on connection state
def onConnection(state):
    # Print the current state
    print(state)

# Callback function to handle current state
def dataHandler(code, res):
    # Display data in GUI
    millis = res["data"]
    text = font.render(f"Millis: {millis}", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (screen_info.current_w // 2 - text.get_width() // 2, screen_info.current_h // 2 - text.get_height() // 2))
    pygame.display.flip()

# Init the SDK and get reference to the project
project = grandeur.init(apiKey, token)

# Place listener
project.onConnection(onConnection)

# Get a reference to device class
device = project.device(deviceID)

# Function to fetch data every 5 seconds
def fetchData():
    while True:
        # Get current state
        device.data().get("millis", dataHandler)
        time.sleep(5)

# Start the data fetching loop in a new thread
fetch_thread = threading.Thread(target=fetchData)
fetch_thread.daemon = True
fetch_thread.start()

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
