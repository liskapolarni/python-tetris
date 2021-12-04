import pygame
import random
import shapes

pygame.init()

# screen settings
screen_width = 450
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# tile settings
tiles_x, tiles_y = 10, 20
tile_size = 30

# game settings
framerate = 60
speed = 5

# game variables
class Score:
    def __init__(self):
        self.value = 0

    def __str__(self):
        return str(self.value)

    def reset(self):
        self.value = 0

    def increase(self, value):
        self.value += value

score = Score()

# game map
class GameMap:
    def __init__(self):
        self.map = [[0 for y in range(tiles_y)] for x in range(tiles_x)]
        self.full = False

    def __str__(self):
        return self.map

    def get_rows(self):
        rows = [[self.map[x][y] for x in range(tiles_x)] for y in range(tiles_y)]
        return rows

    def clear_row(self, row_id):
        # update rows
        rows = self.get_rows()
        rows.pop(row_id)
        rows.insert(0, [0 for x in range(tiles_x)])

        # change map based on new rows
        self.map = [[rows[y][x] for y in range(tiles_y)] for x in range(tiles_x)]
    
    def check_rows(self):
        # get all rows of the current map
        rows = self.get_rows()

        full_rows = []

        # loop through the rows, check if any row is full
        for row_id, row in enumerate(rows):
            row_full = all(tile != 0 for tile in row)

            # if the row is full, add it to a clear list
            if row_full:
                full_rows.append(row_id)

        # clear marked rows
        for row_id in full_rows:
            self.clear_row(row_id)

        # if any rows were deleted, increase the score
        if len(full_rows) > 0:
            score_add = 50
            for multiplier in range(1, len(full_rows) + 1):
                score_add *= multiplier
            
            score.increase(score_add)

    def is_full(self):
        top_row = self.get_rows()[0]
        return top_row.count(0) != tiles_x

game_map = GameMap()

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
        self.move_vector = (0,0)

        # brick position
        self.x = 3 if self.width >= 3 else 4
        self.y = 0

    def get_brick_positions(self, model = False):
        # use a custom model if passed in
        loop_model = self.model if not model else model

        # loop through model, keep coordinates if tile's value isn't 0
        brick_positions = [(tile_x, tile_y) for tile_x in range(self.width) for tile_y in range(self.height) if loop_model[tile_y][tile_x] != 0]
        return brick_positions

    def move(self, x, y):
        # check if the brick isn't locked
        if not self.locked:
            # check if can move down
            if self.y+self.height+y <= tiles_y:
                tile_below = False

                for (bx, by) in self.get_brick_positions():
                    # if there's a placed tile below one of the bottom tiles, lock the brick
                    if self.x + bx < tiles_x and self.y + by + 1 < tiles_y:
                        if game_map.map[self.x + bx][self.y + by + 1] != 0:
                            tile_below = True

                if not tile_below:
                    self.y += y
                else:
                    self.lock()
            else:
                self.lock()

            # check if can move to side
            if self.x+self.width+x <= tiles_x and self.x+x >= 0:
                tile_sideby = False

                for (sx, sy) in self.get_brick_positions():
                    if game_map.map[self.x + sx + (1 if x > 0 else -1)][self.y + sy] != 0:
                        tile_sideby = True

                if not tile_sideby:
                    self.x += x

    def lock(self):
        self.locked = True

        # put the brick on game map
        for (tx, ty) in self.get_brick_positions():
            game_map.map[self.x+tx][self.y+ty] = self.type

    def push_down(self):
        while not self.locked:
            self.move(0,1)

    def rotate(self):
        # create a rotated model
        rotated_model = [[self.model[y][x] for y in range(self.height)] for x in range(self.width)]
        # reverse its rows in order to make it 90deg
        rotated_model = [list(reversed(row)) for row in rotated_model]

        # properties of rotated brick
        rm_width, rm_height = len(rotated_model[0]), len(rotated_model)
        width_diff, height_diff = self.width - rm_width, self.height - rm_height
        new_x, new_y = self.x + width_diff, self.y + height_diff

        # check if the rotation is possible
        can_rotate = True

        for rx in range(rm_width):
            for ry in range(rm_height):
                if new_x + rx >= 0 and new_x + rx < tiles_x and new_y + ry < tiles_y:
                    if game_map.map[new_x + rx][new_y + ry] != 0:
                        can_rotate = False
                else:
                    can_rotate = False

        # if the rotation is possible, update brick's properties
        if can_rotate:
            self.width, self.height = rm_width, rm_height
            self.x, self.y = new_x, new_y
            self.model = rotated_model

# create first brick
brick = Brick()

# create next brick
next_brick = Brick()

# draw tile
def draw_tile(x, y, color):
    pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))

# text
class Text:
    def __init__(self, text, font_size, color = (255, 255 ,255)):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font('./fonts/inter.ttf', font_size)
        self.color = color

        self.update_surface()

    def update_surface(self):
        self.width, self.height = self.font.size(self.text)
        self.surface = self.font.render(self.text, True, self.color)

    def set_text(self, text):
        self.text = text
        self.update_surface()

    def center_pos(self, start = 0, end = screen_width):
        total_width = end - start
        margin = (total_width - self.width) / 2
        pos = start + margin
        return pos

next_brick_text = Text('Next brick:', 24)
score_text = Text(f'Score: {score}', 20)

# game loop
clock = pygame.time.Clock()
rendered_frames = 0
running = True

pygame.font.init()
font = pygame.font.Font('./fonts/inter.ttf', 24)

while running:
    # dark background
    screen.fill((0, 0, 0))

    # grid
    for gx in range(1, tiles_x):
        pygame.draw.rect(screen, (50, 50, 50), (gx * tile_size, 0, 1, screen_height))
    for gy in range(1, tiles_y):
        pygame.draw.rect(screen, (50, 50, 50), (0, gy * tile_size, tiles_x * tile_size, 1))

    # game and info divider
    pygame.draw.rect(screen, (255, 255, 255), (300, 0, 2, screen_height))

    # next brick
    screen.blit(next_brick_text.surface, (next_brick_text.center_pos(300), 10))

    nbox_offset_x = ((150 - (next_brick.width * tile_size + 20)) / 2)
    nbox_x, nbox_y = screen_width - 150 + nbox_offset_x, 50
    pygame.draw.rect(screen, (255, 255, 255), (nbox_x, nbox_y, (next_brick.width*tile_size)+20, (next_brick.height*tile_size)+20), 1)
    for (nx, ny) in next_brick.get_brick_positions():
        draw_tile(nbox_x+(nx*tile_size)+10, nbox_y+(ny*tile_size)+10, next_brick.color)

    # score
    score_text.set_text(f'Score: {score}')
    screen.blit(score_text.surface, (score_text.center_pos(300), screen_height - 40))

    # draw the current brick
    for (tx, ty) in brick.get_brick_positions():
        draw_tile((brick.x+tx)*tile_size, (brick.y+ty)*tile_size, brick.color)

    # draw placed tiles
    placed_tiles = [(tx, ty) for tx in range(tiles_x) for ty in range(tiles_y) if game_map.map[tx][ty] != 0]
    for (tx, ty) in placed_tiles:
        tile_type = game_map.map[tx][ty]
        tile_color = shapes.colors[tile_type]

        draw_tile(tx*tile_size, ty*tile_size, tile_color)

    # check for keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                brick.move_vector = (-1,0)
            elif event.key == pygame.K_RIGHT:
                brick.move_vector = (1,0)
            elif event.key == pygame.K_DOWN:
                brick.move_vector = (0,1)
            elif event.key == pygame.K_UP:
                brick.rotate()
            elif event.key == pygame.K_SPACE:
                brick.push_down()
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
                brick.move_vector = (0,0)

    rendered_frames += 1

    # auto-move
    if rendered_frames % (framerate / speed) == 0:
        brick.move(0, 1)

        # check if it is possible to generate a new brick
        if brick.locked and not game_map.is_full():
            brick = next_brick
            next_brick = Brick()

    # apply movement
    if rendered_frames % (framerate / (speed * 4)) == 0:
        if brick.move_vector != (0,0):
            (x, y) = brick.move_vector
            brick.move(x, y)

    # check for full rows, if any row is full, it is removed
    game_map.check_rows()

    # check if the game is over
    if game_map.is_full():
        screen.fill((0, 0, 0))
        game_over_text = Text('Game over!', 48)
        screen.blit(game_over_text.surface, (game_over_text.center_pos(), 20))
        screen.blit(score_text.surface, (score_text.center_pos(), 80))

    pygame.display.update()
    clock.tick(framerate)