import pygame
import os

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


player = Player(A_IMAGE, (10, 10), (50, 50))


def draw_window():
    WIN.fill(WHITE)
    player.move_one_step(Direction.RIGHT)
    WIN.blit(player.image, player.box.topleft)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d]:
            print("XD")


    pygame.quit()

if __name__ == "__main__":
    main()

