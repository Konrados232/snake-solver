from enum import Enum
from time import sleep
import pygame
import os
from pygame import Vector2
from Fruit import Fruit

from Player import Player
from Direction import Direction
from InputDirection import InputDirection
from BoxInfo import BoxInfo


# prerequisites
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Solver")


# useful consts
WHITE = (255, 255, 255)
FPS = 60
TILE_WIDTH, TILE_HEIGHT = 50, 50
TILE_SIZES = (TILE_WIDTH, TILE_HEIGHT)
BOARD_WIDTH, BOARD_HEIGHT = 20, 15
BOARD_SIZES = (BOARD_WIDTH, BOARD_HEIGHT)

SPEED = 20
score = [0]


# loading images
A_IMAGE = pygame.image.load(os.path.join("assets", "a.png"))
A_IMAGE = pygame.transform.scale(A_IMAGE, (TILE_WIDTH, TILE_WIDTH))
FRUIT_IMAGE = pygame.image.load(os.path.join("assets", "fruit.png"))
FRUIT_IMAGE = pygame.transform.scale(FRUIT_IMAGE, (TILE_WIDTH, TILE_WIDTH))


# load objects

first_pos = Vector2(0, 0)
sizes = Vector2(50, 50)
player = Player(A_IMAGE, first_pos, sizes)
first_fruit_pos = Vector2((int)(BOARD_HEIGHT/2), (int)(BOARD_WIDTH/2))
fruit = Fruit(FRUIT_IMAGE, first_fruit_pos, sizes)


# font
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_sur = my_font.render(str(score), False, (0,0,0))




def read_input(events):
    for event in events:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if is_next_move_possible(player.get_current_head_pos(), player.get_player_part_queue(), Direction.LEFT):
                    player.move_one_step(Direction.LEFT)
                    if does_player_hit_fruit(player.get_current_head_pos(), fruit.get_fruit_pos()):
                        do_fruit(score)
            if event.key == pygame.K_RIGHT:
                if is_next_move_possible(player.get_current_head_pos(), player.get_player_part_queue(), Direction.RIGHT):
                    player.move_one_step(Direction.RIGHT)
                    if does_player_hit_fruit(player.get_current_head_pos(), fruit.get_fruit_pos()):
                        do_fruit(score)
            if event.key == pygame.K_DOWN:
                if is_next_move_possible(player.get_current_head_pos(), player.get_player_part_queue(), Direction.DOWN):
                    player.move_one_step(Direction.DOWN)
                    if does_player_hit_fruit(player.get_current_head_pos(), fruit.get_fruit_pos()):
                        do_fruit(score)
            if event.key == pygame.K_UP:
                if is_next_move_possible(player.get_current_head_pos(), player.get_player_part_queue(), Direction.UP):
                    player.move_one_step(Direction.UP)
                    if does_player_hit_fruit(player.get_current_head_pos(), fruit.get_fruit_pos()):
                        do_fruit(score)

            # alternative way of moving (testing)
            if event.key == pygame.K_a:
                standardized_input = convert_input_to_direction(InputDirection.TURN_COUNTERCLOCKWISE, current_dir=player.get_current_direction())
                do_move(standardized_input)
            if event.key == pygame.K_w:
                standardized_input = convert_input_to_direction(InputDirection.FORWARD, current_dir=player.get_current_direction())
                do_move(standardized_input)
            if event.key == pygame.K_d:
                standardized_input = convert_input_to_direction(InputDirection.TURN_CLOCKWISE, current_dir=player.get_current_direction())
                do_move(standardized_input)


def convert_input_to_direction(input_dir, current_dir):
    if input_dir == InputDirection.FORWARD:
        new_dir = current_dir
    elif input_dir == InputDirection.TURN_CLOCKWISE:
        new_dir = Direction.get_clockwise(current_dir)
    elif input_dir == InputDirection.TURN_COUNTERCLOCKWISE:
        new_dir = Direction.get_counterclockwise(current_dir)

    return new_dir


def do_move(direction):
    if is_next_move_possible(player.get_current_head_pos(), player.get_player_part_queue(), direction):
        player.move_one_step(direction)
        if does_player_hit_fruit(player.get_current_head_pos(), fruit.get_fruit_pos()):
            do_fruit(score)


# temporary func
def do_fruit(score):
    score[0] += 1
    print(score)
    fruit.set_random_pos(player.get_player_part_queue(), BOARD_SIZES)
    player.increase_in_size_by_one()


def update_score(score):
    text_sur = my_font.render(str(score[0]), False, (0,0,0))
    WIN.blit(text_sur, (1000, 200))


def draw_window():
    WIN.fill(WHITE)

    for i in player.get_player_part_queue():
        WIN.blit(i.image, i.box_info.box.topleft)

    WIN.blit(fruit.image, fruit.box_info.box.topleft)

    update_score(score=score)


    pygame.display.update()

def draw_again():
    global fruit
    global player
    fruit = Fruit(FRUIT_IMAGE, first_fruit_pos, sizes)
    player = Player(A_IMAGE, first_pos, sizes)
    score[0] = 0
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

        if is_stuck():
            draw_again()
            

        keys_pressed = pygame.key.get_pressed()

    pygame.quit()


def is_next_move_possible(player_pos, player_parts_queue, direction):
    next_pos_x = player_pos.x + direction.value[0]
    next_pos_y = player_pos.y + direction.value[1]

    return not does_player_hit_itself(next_pos_x, next_pos_y, player_parts_queue) and is_within_board(next_pos_x, next_pos_y)


def is_within_board(next_pos_x, next_pos_y):
    return next_pos_x >= 0 and next_pos_x < BOARD_WIDTH and next_pos_y >= 0 and next_pos_y < BOARD_HEIGHT


def does_player_hit_itself(next_pos_x, next_pos_y, player_parts_queue):
    for part in player_parts_queue:
        part_grid_pos = part.get_grid_pos()
        if next_pos_x == part_grid_pos.x and next_pos_y == part_grid_pos.y:
            return True

    return False


def does_player_hit_fruit(player_pos, fruit_pos):
    return player_pos.x == fruit_pos.x and player_pos.y == fruit_pos.y


def is_stuck():
    player_pos = player.get_current_head_pos()
    player_parts_queue = player.get_player_part_queue()
    directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
    for dir in directions:
        if(is_next_move_possible(player_pos, player_parts_queue, dir)): #sprawdzać jeszcze brzegi
            return False

    return True


if __name__ == "__main__":
    main()

