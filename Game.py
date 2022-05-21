import pygame
import os
from pygame import Vector2
from Fruit import Fruit

from Player import Player
from Direction import Direction
from InputDirection import InputDirection

class Game():
    def __init__(self, width, height):
        # prerequisites
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Solver")

        # useful consts
        self.WHITE = (255, 255, 255)
        self.FPS = 60
        
        self.BOARD_WIDTH, self.BOARD_HEIGHT = 20, 15
        self.BOARD_SIZES = (self.BOARD_WIDTH, self.BOARD_HEIGHT)
        
        TILE_WIDTH, TILE_HEIGHT = 50, 50
        self.TILE_SIZES = (TILE_WIDTH, TILE_HEIGHT)
        self.sizes = Vector2(50, 50)

        self.SPEED = 20
        self.score = 0

        # RL variables
        self.reward = 0
        self.stagnate_steps = 0

        # loading images
        self.A_IMAGE = pygame.image.load(os.path.join("assets", "a.png"))
        self.A_IMAGE = pygame.transform.scale(self.A_IMAGE, (TILE_WIDTH, TILE_WIDTH))
        self.FRUIT_IMAGE = pygame.image.load(os.path.join("assets", "fruit.png"))
        self.FRUIT_IMAGE = pygame.transform.scale(self.FRUIT_IMAGE, (TILE_WIDTH, TILE_WIDTH))

        # font
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_sur = self.my_font.render(str(self.score), False, (0,0,0))

        # load objects
        self.first_pos = Vector2(0, 0)
        self.player = Player(self.A_IMAGE, self.first_pos, self.sizes)
        self.first_fruit_pos = Vector2((int)(self.BOARD_HEIGHT/2), (int)(self.BOARD_WIDTH/2))
        self.fruit = Fruit(self.FRUIT_IMAGE, self.first_fruit_pos, self.sizes)


    def main(self):
        # input

        # move to the next direction

        # check game over
        # place next food

        # update ui and clock

        # return game over and score


        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            events = pygame.event.get()
            self.read_input(events)
            
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                
            if not self.can_move():
                self.reset()
            

            self.draw_window()

        pygame.quit()


    # UI-related methods

    def draw_window(self):
        self.WIN.fill(self.WHITE)

        self.draw_game_elements()
        self.draw_score()
        self.draw_lines()

        pygame.display.update()

    def draw_game_elements(self):
        for i in self.player.get_player_part_queue():
            self.WIN.blit(i.image, i.box_info.box.topleft)

        self.WIN.blit(self.fruit.image, self.fruit.box_info.box.topleft)
    
    def draw_score(self):
        text_sur = self.my_font.render(str(self.score), False, (0,0,0))
        self.WIN.blit(text_sur, (1000, 200))

    def draw_lines(self):
        pygame.draw.line(self.WIN, (50,50,50), (0, 0), (1000, 0), 1)
        pygame.draw.line(self.WIN, (50,50,50), (0, 750), (1000, 750), 1)
        pygame.draw.line(self.WIN, (50,50,50), (1000, 0), (1000, 750), 1)

    # game logic related methods

    def reset(self):
        self.player.reset()
        self.fruit.reset()
        self.score = 0
        self.stagnate_steps = 0
        
    def read_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.is_next_move_possible(self.player.get_current_head_pos(), self.player.get_player_part_queue(), Direction.LEFT):
                        self.player.move_one_step(Direction.LEFT)
                        if self.does_player_hit_fruit(self.player.get_current_head_pos(), self.fruit.get_fruit_pos()):
                            self.do_fruit()
                if event.key == pygame.K_RIGHT:
                    if self.is_next_move_possible(self.player.get_current_head_pos(), self.player.get_player_part_queue(), Direction.RIGHT):
                        self.player.move_one_step(Direction.RIGHT)
                        if self.does_player_hit_fruit(self.player.get_current_head_pos(), self.fruit.get_fruit_pos()):
                            self.do_fruit()
                if event.key == pygame.K_DOWN:
                    if self.is_next_move_possible(self.player.get_current_head_pos(), self.player.get_player_part_queue(), Direction.DOWN):
                        self.player.move_one_step(Direction.DOWN)
                        if self.does_player_hit_fruit(self.player.get_current_head_pos(), self.fruit.get_fruit_pos()):
                            self.do_fruit()
                if event.key == pygame.K_UP:
                    if self.is_next_move_possible(self.player.get_current_head_pos(), self.player.get_player_part_queue(), Direction.UP):
                        self.player.move_one_step(Direction.UP)
                        if self.does_player_hit_fruit(self.player.get_current_head_pos(), self.fruit.get_fruit_pos()):
                            self.do_fruit()

                # alternative way of moving (testing)
                if event.key == pygame.K_a:
                    standardized_input = self.convert_input_to_direction(InputDirection.TURN_COUNTERCLOCKWISE, current_dir=self.player.get_current_direction())
                    self.do_move(standardized_input)
                if event.key == pygame.K_w:
                    standardized_input = self.convert_input_to_direction(InputDirection.FORWARD, current_dir=self.player.get_current_direction())
                    self.do_move(standardized_input)
                if event.key == pygame.K_d:
                    standardized_input = self.convert_input_to_direction(InputDirection.TURN_CLOCKWISE, current_dir=self.player.get_current_direction())
                    self.do_move(standardized_input)


    def convert_input_to_direction(self, input_dir, current_dir):
        if input_dir == InputDirection.FORWARD:
            new_dir = current_dir
        elif input_dir == InputDirection.TURN_CLOCKWISE:
            new_dir = Direction.get_clockwise(current_dir)
        elif input_dir == InputDirection.TURN_COUNTERCLOCKWISE:
            new_dir = Direction.get_counterclockwise(current_dir)

        return new_dir


    def do_move(self, direction):
        if self.is_next_move_possible(self.player.get_current_head_pos(), self.player.get_player_part_queue(), direction):
            self.player.move_one_step(direction)
            if self.does_player_hit_fruit(self.player.get_current_head_pos(), self.fruit.get_fruit_pos()):
                self.do_fruit()


    # temporary func
    def do_fruit(self):
        self.score += 1
        self.fruit.set_random_pos(self.player.get_player_part_queue(), self.BOARD_SIZES)
        self.player.increase_in_size_by_one()


    # TO-DO refactor
    def is_next_point_possible(self, point_pos):
        return not self.does_player_hit_itself(point_pos.x, point_pos.y, self.player.get_player_part_queue()) and self.is_within_board(point_pos.x, point_pos.y, self.BOARD_WIDTH, self.BOARD_HEIGHT)


    def is_next_move_possible(self, player_pos, player_parts_queue, direction):
        next_pos_x = player_pos.x + direction.value[0]
        next_pos_y = player_pos.y + direction.value[1]

        return not self.does_player_hit_itself(next_pos_x, next_pos_y, player_parts_queue) and self.is_within_board(next_pos_x, next_pos_y, self.BOARD_WIDTH, self.BOARD_HEIGHT)


    def is_within_board(self, next_pos_x, next_pos_y, board_width, board_height):
        return next_pos_x >= 0 and next_pos_x < board_width and next_pos_y >= 0 and next_pos_y < board_height


    def does_player_hit_itself(self, next_pos_x, next_pos_y, player_parts_queue):
        for part in player_parts_queue:
            part_grid_pos = part.get_grid_pos()
            if next_pos_x == part_grid_pos.x and next_pos_y == part_grid_pos.y:
                return True

        return False


    def does_player_hit_fruit(self, player_pos, fruit_pos):
        return player_pos.x == fruit_pos.x and player_pos.y == fruit_pos.y


    def can_move(self):
        result = False

        player_pos = self.player.get_current_head_pos()
        player_parts_queue = self.player.get_player_part_queue()
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        for direction in directions:
            if(self.is_next_move_possible(player_pos, player_parts_queue, direction)):
                result = True

        return result