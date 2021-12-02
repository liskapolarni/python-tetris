import pygame

pygame.init()

# screen settings
screen_width = 450
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False