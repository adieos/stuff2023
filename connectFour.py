import numpy as np
import pygame


board = np.zeros((6,7))
game_over = False
turn = 1
# odd = player 1
# even = player 2

def isWin(player):
    # Check horizontally
    for i in range(6):
        for j in range(4):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True

    # Check vertically
    for i in range(3):
        for j in range(7):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True

    # Check diagonally
    for i in range(3):
        for j in range(3,7):
            if board[i][j] == player and board[i+1][j-1] == player and board[i+2][j-2] == player and board[i+3][j-3] == player:
                return True
while not game_over:
    # Ask for players' input
    ans = input("Player 1: ") if turn % 2 else input("Player 2: ") 
    if ans == "e": 
        # game_over = True
        print("Game ended by request.")
        break
    elif ans == "q":
        # EVAL CODE GOES HERE
        board[0][3] = 30
        print(board)
    symbol = 1 if turn % 2 else 2

    try:        
        if int(ans) <= 0: raise IndexError
        ans = int(ans) - 1
        for i in range(1,7):
            if board[0][ans] != 0: raise IndexError # if top row is not empty but mf still force it, raise error
            if board[-i][ans] == 0:
                board[-i][ans] = symbol
                break
        print(board)
        if isWin(symbol):
            player = 1 if turn % 2 else 2
            print(f"Player {str(player)} won on turn {turn}! GG!")
            break
        turn += 1
    except IndexError:
        print("Out of range, idiot!")
    except ValueError:
        print("Input a valid number dumbass")