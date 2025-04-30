import pygame    # Import the pygame library for creating games
import sys       # Import the sys library to exit the game
import random    # Import random for generating random values (not used yet)

pygame.init()    # Initialize all imported pygame modules

# Set the screen width (SW) and screen height (SH) to 800 pixels each
SW, SH = 800, 800
BLOCK_SIZE = 50
FONT = pygame.font.SysFont("comicsansms", 100)


# Set up the game window with dimensions 800x800
screen = pygame.display.set_mode((800, 800))

# Set the caption (window title) of the game to "Snake!"
pygame.display.set_caption("Snake!")

# Create a clock object to manage the game's frame rate
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
     
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True






                
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

drawGrid()
# Start the main game loop
while True:
    # Process all events (like keyboard and mouse input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   # Uninitialize all pygame modules
            sys.exit()     

    pygame.display.update()  # Update the full display surface to the screen
    clock.tick(10)           # Limit the game loop to 10 frames per second
