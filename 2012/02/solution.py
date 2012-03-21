#!/usr/bin/env python3
import os
import time
from random import Random

BOARD_SIZE = 48

def print_board(board, wait = False, sleep = False):
    os.system(['clear','cls'][os.name == 'nt'])
    print('=' * (BOARD_SIZE + 2), end = '|\n')
    for row in board:
       print(*['X' if x else ' ' for x in row], end = ' |\n', sep = '')

    print([[x & 1 for x in row] for row in board])
    input("Press enter to continue.")

def create_board(fill_rate = 0.3):
    rand = Random()
    return [[int(x and x != BOARD_SIZE + 1 and y and y != BOARD_SIZE + 1
             and rand.normalvariate(0.5,0.2) < fill_rate) for x in range(0,BOARD_SIZE + 2)] for y in range(0,BOARD_SIZE + 2)]

def step_board(board):
    pass # Пишете тук

if __name__ == '__main__':
    board = create_board()
    while True:
        step_board(board)
        print_board(board)
