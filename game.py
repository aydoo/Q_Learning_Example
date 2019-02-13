import numpy as np
import random
import matplotlib.pyplot as plt

class Game:
    EMPTY = 0
    PLAYER = 1
    FOOD = 2

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, board_shape = (5,5)):
        self.board_shape = board_shape
        self.board = np.full(board_shape, self.EMPTY, dtype='uint8')

        self.player_pos = (self.random_pos())
        self.board[self.player_pos] = self.PLAYER

        self.board[self.random_pos(self.player_pos)] = self.FOOD
        self.score = 0

    #returns -1 for invalid, 0 for valid non-scoring and 1 for valid scoring move
    def move(self, d):
        new_pos = (self.player_pos[0] + d[0], self.player_pos[1] + d[1])
        if new_pos[0] < 0 or new_pos[1] < 0:
            #print('Invalid Move:', d)

            return -1

        scored = 0
        try:
            if self.board[new_pos] == self.FOOD:
#                print('Food found!')
                self.score += 1
                scored += 1
                new_food_pos = self.random_pos(new_pos)
#                print('New Food at', new_food_pos)
                self.board[new_food_pos] = self.FOOD
            self.board[new_pos] = self.PLAYER
            self.board[self.player_pos] = self.EMPTY if self.board[self.player_pos] != self.FOOD else self.FOOD
            self.player_pos = new_pos
            return scored
            #self.plot_board()

        except:
           # print('Invalid Move:', d)
            return -1

    def random_pos(self, except_pos = None):
        done = False
        while not done:
            x = random.randint(0, self.board_shape[0]-1)
            y = random.randint(0, self.board_shape[1]-1)
            if except_pos is None or x != except_pos[0] or y != except_pos[1]:
                done = True
        return (x,y)

    def plot_board(self):
        plt.matshow(self.board)

    def print_board(self):
        print(self.board)

    def num_to_dir(self, num):
        if num == 0: return self.UP
        elif num == 1: return self.DOWN
        elif num == 2: return self.LEFT
        elif num == 3: return self.RIGHT
        else: return None
