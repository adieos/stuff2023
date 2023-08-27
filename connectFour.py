import numpy as np
import pygame

board = np.zeros((6,7))
game_over = False
turn = 1
# odd = player 1
# even = player 2
class InvalidSlot(Exception):
    pass

while not game_over:
    # Ask for players' input
    ans = input("Player 1: ") if turn % 2 else input("Player 2: ") 
    if ans == "e": 
        game_over = True
        break
    symbol = 1 if turn % 2 else 2

    try:        
        if int(ans) <= 0: raise IndexError
        ans = int(ans) - 1
        for i in range(1,7):
            if board[0][ans] != 0: raise IndexError
            if board[-i][ans] == 0:
                board[-i][ans] = symbol
                break
        print(board)
        turn += 1
    except IndexError:
        print("Out of range, idiot!")
    except ValueError:
        print("Input a valid number dumbass")