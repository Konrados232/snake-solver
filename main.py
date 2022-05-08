import pygame
import os
from pygame import Vector2

from Player import Player
from Direction import Direction


# prerequisites
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")


# useful consts
WHITE = (255, 255, 255)
FPS = 60
TILE_WIDTH, TILE_HEIGHT = 50, 50


# loading images
A_IMAGE = pygame.image.load(os.path.join("assets", "a.png"))
A_IMAGE = pygame.transform.scale(A_IMAGE, (TILE_WIDTH, TILE_WIDTH))

# load objects
first_pos = Vector2(0, 0)
sizes = Vector2(50, 50)
player = Player(A_IMAGE, first_pos, sizes)


def read_input(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_one_step(Direction.LEFT)
            if event.key == pygame.K_RIGHT:
                player.move_one_step(Direction.RIGHT)
            if event.key == pygame.K_DOWN:
                player.move_one_step(Direction.DOWN)
            if event.key == pygame.K_UP:
                player.move_one_step(Direction.UP)


def draw_window():
    WIN.fill(WHITE)

    for i in player.get_player_part_queue():
        WIN.blit(i.image, i.box.topleft)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        read_input(events)
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            

        draw_window()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d]:
            print("XD")


    pygame.quit()

if __name__ == "__main__":
    main()

