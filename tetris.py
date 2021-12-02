import pygame
import random
import shapes

pygame.init()

# screen settings
screen_width = 450
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# tile settings
tiles_x, tiles_y = 10, 20
tile_size = 30

# game map
game_map = [[0 for y in range(20)] for x in range(10)]

# bricks
class Brick:
    def __init__(self):
        # brick info
        self.type = random.choice(shapes.types)
        self.model = shapes.models[self.type]
        self.color = shapes.colors[self.type]
        (self.width, self.height) = shapes.dimensions[self.type]

        # brick position
        self.x = 3 if self.width >= 3 else 4
        self.y = 0

    def place_brick(self):
        pass

    def get_brick_positions(self):
        # check if model exists, we need something to loop through
        if type(self.model) == tuple:
            # loop through model, keep coordinates if tile's value isn't 0
            brick_positions = [(tile_x, tile_y) for tile_x in range(self.width) for tile_y in range(self.height) if self.model[tile_y][tile_x] != 0]

            return brick_positions
        else:
            return []

brick = Brick()

# game loop
running = True
while running:
    # dark background
    screen.fill((0, 0, 0))

    # game and info divider
    pygame.draw.rect(screen, (255, 255, 255), (300, 0, 2, screen_height))

    # draw the current brick
    for brick_tile in brick.get_brick_positions():
        (tx, ty) = brick_tile

        pygame.draw.rect(screen, brick.color, ((brick.x + tx) * tile_size, (brick.y + ty) * tile_size, tile_size, tile_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()