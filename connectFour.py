import numpy as np
import pygame
import os
pygame.init()

WIDTH, HEIGHT = 600, 700
BOARD = np.zeros((6,7))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BLUE = (0,0,255)

COIN_WIDTH, COIN_HEIGHT = 70,70
PLACE = pygame.image.load(os.path.join('assets_connectFour', "window.png"))
COIN_PLACE = pygame.transform.scale(PLACE, (COIN_WIDTH, COIN_HEIGHT))

def isWin(player):
    # Check horizontally
    for i in range(6):
        for j in range(4):
            if BOARD[i][j] == player and BOARD[i][j+1] == player and BOARD[i][j+2] == player and BOARD[i][j+3] == player:
                return True

    # Check vertically
    for i in range(3):
        for j in range(7):
            if BOARD[i][j] == player and BOARD[i+1][j] == player and BOARD[i+2][j] == player and BOARD[i+3][j] == player:
                return True

    # Check diagonally
    for i in range(3):
        for j in range(3,7):
            if BOARD[i][j] == player and BOARD[i+1][j-1] == player and BOARD[i+2][j-2] == player and BOARD[i+3][j-3] == player:
                return True
            
def draw_window():
    WIN.fill(BLUE)


def main():
    running = True
    turn = 1
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        ans = input("Player 1: ") if turn % 2 else input("Player 2: ") 
        if ans == "e": 
            # game_over = True
            print("Game ended by request.")
            break
        elif ans == "q":
            # EVAL CODE GOES HERE
            BOARD[0][3] = 30
            print(BOARD)
        symbol = 1 if turn % 2 else 2

        try:        
            if int(ans) <= 0: raise IndexError
            ans = int(ans) - 1
            for i in range(1,7):
                if BOARD[0][ans] != 0: raise IndexError # if top row is not empty but mf still force it, raise error
                if BOARD[-i][ans] == 0:
                    BOARD[-i][ans] = symbol
                    break
            print(BOARD)
            if isWin(symbol):
                player = 1 if turn % 2 else 2
                print(f"Player {str(player)} won on turn {turn}! GG!")
                break
            turn += 1
        except IndexError:
            print("Out of range, idiot!")
        except ValueError:
            print("Input a valid number dumbass")
    pygame.quit()