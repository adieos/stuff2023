import pygame
import os
import random
pygame.init()

WIDTH, HEIGHT = 900, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 5
pygame.display.set_caption("stupid cat game")
pygame.display.set_icon(pygame.image.load(os.path.join('assets_otherGim', 'cat.png')))

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LGREEN = (37, 196, 45)
DGREEN = (29, 153, 35)

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
VEL = 60

CAT_WIDTH = 40
CAT_HEIGHT = 40
CAT_RAW = pygame.image.load(os.path.join('assets_otherGim', 'cat.png'))
CAT = pygame.transform.scale(CAT_RAW, (CAT_WIDTH, CAT_HEIGHT))
ENEMY_RAW = CAT_RAW = pygame.image.load(os.path.join('assets_otherGim', 'cat.png'))
ENEMY = pygame.transform.scale(ENEMY_RAW, (CAT_WIDTH, CAT_HEIGHT))

def draw_window(cat, enemy):
    draw_grid()
    WIN.blit(CAT, (cat.x, cat.y))
    WIN.blit(ENEMY, (enemy.x, enemy.y))
    pygame.display.update()

def draw_grid():
    # each tile is now 60x60
    width_blocks = 15
    height_blocks = 9
    var = 1
    for x in range(0, WIDTH, WIDTH//width_blocks):
        for y in range(0, HEIGHT, HEIGHT//height_blocks):
            rect = pygame.Rect(x, y, WIDTH//width_blocks, HEIGHT//height_blocks)
            if var%2:
                pygame.draw.rect(WIN,LGREEN, rect)
            else:
                pygame.draw.rect(WIN, DGREEN, rect)
            var += 1

def move_cat(keys_pressed, cat):
    if keys_pressed[pygame.K_a] and cat.x - VEL > 0:
        cat.x -= VEL
    elif keys_pressed[pygame.K_d] and cat.x + VEL < WIDTH:
        cat.x += VEL
    elif keys_pressed[pygame.K_w] and cat.y - VEL > 0:
        cat.y -= VEL
    elif keys_pressed[pygame.K_s] and cat.y + VEL < HEIGHT:
        cat.y += VEL

def move_enemy(enemy):
    move = random.randint(1,4) # LEFT, UP, RIGHT, DOWN
    if move == 1 and enemy.x - VEL > 0:
        enemy.x -= VEL
    if move == 2 and enemy.y - VEL > 0:
        enemy.y -= VEL
    if move == 3 and enemy.x + VEL < WIDTH:
        enemy.x += VEL
    if move == 4 and enemy.y + VEL < HEIGHT:
        enemy.y += VEL

def main():
    cat = pygame.Rect(10,10, CAT_WIDTH, CAT_HEIGHT)
    enemy = pygame.Rect(WIDTH-50, HEIGHT-50, CAT_WIDTH, CAT_HEIGHT)

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        keys_pressed = pygame.key.get_pressed()
        move_cat(keys_pressed, cat)
        move_enemy(enemy)
        draw_window(cat, enemy)

if __name__ == "__main__":
    main()