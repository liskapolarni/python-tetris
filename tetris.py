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

        # movement
        self.locked = False

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

    def move(self, x, y):
        # check if the brick isn't locked
        if not self.locked:
            # check if can move down
            if self.y+self.height+y <= tiles_y:
                self.y += y
            else:
                self.lock()

            # check if can move to side
            if self.x+self.width+x <= tiles_x and self.x+x >= 0:
                self.x += x

    def lock(self):
        self.locked = True

        for (tx, ty) in self.get_brick_positions():
            game_map[self.x+tx][self.y+ty] = self.type

brick = Brick()

# game loop
clock = pygame.time.Clock()
rendered_frames = 0
running = True

while running:
    # dark background
    screen.fill((0, 0, 0))

    # game and info divider
    pygame.draw.rect(screen, (255, 255, 255), (300, 0, 2, screen_height))

    # draw the current brick
    for (tx, ty) in brick.get_brick_positions():
        pygame.draw.rect(screen, brick.color, ((brick.x + tx) * tile_size, (brick.y + ty) * tile_size, tile_size, tile_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                brick.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                brick.move(1, 0)

    rendered_frames += 1
    if rendered_frames % 15 == 0:
        brick.move(0, 1)

        if brick.locked:
            brick = Brick()

    pygame.display.update()
    clock.tick(60)