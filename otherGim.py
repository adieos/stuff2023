import pygame
import os
import random
import ast
pygame.init()

# lorem ipsum dolor sit amet

with open('assets_otherGim\\boxCoords.txt', 'r') as file:
    box_coords = file.read()
 
with open('assets_otherGim\\blueDogCoords.txt', 'r') as file:
    blue_dog_coords = file.read()

 # display
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

BOX_COORDS = ast.literal_eval(box_coords)
BLUE_DOG_COORDS = ast.literal_eval(blue_dog_coords)
VEL = 60
ORANGE_CAT_MOVE = 0

# images
CAT_WIDTH = 40
CAT_HEIGHT = 40
BOX_WIDTH = 60
BOX_HEIGHT = 60
DOG_WIDTH = 60
DOG_HEIGHT = 60
CAT_RAW = pygame.image.load(os.path.join('assets_otherGim', 'cat.png'))
CAT = pygame.transform.scale(CAT_RAW, (CAT_WIDTH, CAT_HEIGHT))
ORANGE_CAT_RAW = pygame.image.load(os.path.join('assets_otherGim', 'cat.png'))
ORANGE_CAT = pygame.transform.scale(ORANGE_CAT_RAW, (CAT_WIDTH, CAT_HEIGHT))
BOX_RAW = pygame.image.load(os.path.join('assets_otherGim', 'box.png'))
BOX = pygame.transform.scale(BOX_RAW, (BOX_WIDTH, BOX_HEIGHT))
BLUEDOG_RAW = pygame.image.load(os.path.join('assets_otherGim', 'blueDog.png'))
BLUEDOG = pygame.transform.scale(BLUEDOG_RAW, (DOG_WIDTH, DOG_HEIGHT))

class BlueDog:
    def __init__(self, rect, status):
        self.rect = rect
        self.status = status

def draw_window(cat, orange_cat, boxes, blue_dogs):
    draw_grid()
    WIN.blit(CAT, (cat.x, cat.y))
    WIN.blit(ORANGE_CAT, (orange_cat.x, orange_cat.y)) # Turning this off will simply make the orange_cat invisible
    for dog in blue_dogs:
        WIN.blit(BLUEDOG, (dog.x, dog.y))
        if cat.colliderect(dog): 
            print("COLLIDED WITH DOG WOOF WOOF!")
    for box in boxes:
        WIN.blit(BOX, (box.x, box.y))
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

def move_cat(keys_pressed, cat, boxes):
    if keys_pressed[pygame.K_a] and cat.x - VEL > 0:
        cat.x -= VEL
        for box in boxes:
            if cat.colliderect(box): cat.x += VEL
    elif keys_pressed[pygame.K_d] and cat.x + VEL < WIDTH:
        cat.x += VEL
        for box in boxes:
            if cat.colliderect(box): cat.x -= VEL
    elif keys_pressed[pygame.K_w] and cat.y - VEL > 0:
        cat.y -= VEL
        for box in boxes:
            if cat.colliderect(box): cat.y += VEL
    elif keys_pressed[pygame.K_s] and cat.y + VEL < HEIGHT:
        cat.y += VEL
        for box in boxes:
            if cat.colliderect(box): cat.y -= VEL

def move_orange_cat(orange_cat):
    move = random.randint(1,4) # LEFT, UP, RIGHT, DOWN
    if not ORANGE_CAT_MOVE : return
    if move == 1 and orange_cat.x - VEL > 0:
        orange_cat.x -= VEL
    if move == 2 and orange_cat.y - VEL > 0:
        orange_cat.y -= VEL
    if move == 3 and orange_cat.x + VEL < WIDTH:
        orange_cat.x += VEL
    if move == 4 and orange_cat.y + VEL < HEIGHT:
        orange_cat.y += VEL

def move_blue_dog(blue_dog):
    if blue_dog.status == "vertical":
        pass

def main():
    cat = pygame.Rect(10,10, CAT_WIDTH, CAT_HEIGHT)
    orange_cat = pygame.Rect(WIDTH-50, HEIGHT-50, CAT_WIDTH, CAT_HEIGHT)
    boxes = []
    blue_dogs = []
    for i in BOX_COORDS:
        boxes.append(pygame.Rect(i, (BOX_WIDTH, BOX_HEIGHT)))
    bluedogindex = 0
    for i in BLUE_DOG_COORDS:
        blue_dogs.append(pygame.Rect(i[0], i[1], DOG_WIDTH, DOG_WIDTH))
        #blue_dogs[bluedogindex].status = i[2]
        bluedogindex += 1

    cat_HP = 10
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        keys_pressed = pygame.key.get_pressed()
        move_cat(keys_pressed, cat, boxes)
        move_orange_cat(orange_cat)
        draw_window(cat, orange_cat, boxes, blue_dogs)

        if cat.colliderect(orange_cat) :
            cat_HP -= 1 # WIP
            print("COLLIDED! WITH CAT")

if __name__ == "__main__":
    main()
    # note 1: when making levels, update BOX_COORDS constant