import pygame
import os
import random
import ast
pygame.init()
pygame.mixer.init()
pygame.font.init()
# NOTE: do the death() function and maybe key?

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
RED = (255,0,0)

# others
BOX_COORDS = ast.literal_eval(box_coords)
BLUE_DOG_COORDS = ast.literal_eval(blue_dog_coords)
VEL = 60
DOG_VEL = 25
ORANGE_CAT_MOVE = 0
HIT_BLUE_DOG_EVENT = pygame.USEREVENT + 1
DEATH_FONT = pygame.font.SysFont('comicsans', 80)

# sounds
BAKSO_MALAM_OST = pygame.mixer.Sound(os.path.join('assets_otherGim', 'baksoMalam.mp3'))
BAKSO_PAGI_OST = pygame.mixer.Sound(os.path.join('assets_otherGim', 'baksoPagi.mp3'))
BAKSO_PAGI_OST.set_volume(0.25)
HIT_BLUE_DOG_SFX = pygame.mixer.Sound(os.path.join('assets_otherGim', 'vineBoom.mp3'))
KEY_PICKUP_SFX = pygame.mixer.Sound(os.path.join('assets_otherGim', 'keyPick.mp3'))

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
    def __init__(self, rect, status, initial):
        self.rect = rect
        self.status = status
        self.initial = initial

def draw_window(cat, orange_cat, boxes, blue_dogs):
    draw_grid()
    WIN.blit(CAT, (cat.x, cat.y))
    WIN.blit(ORANGE_CAT, (orange_cat.x, orange_cat.y)) # Turning this off will simply make the orange_cat invisible
    for dog in blue_dogs:
        WIN.blit(BLUEDOG, (dog.rect.x, dog.rect.y))
        if cat.colliderect(dog):  # COLLISION !! COLLISION !! COLLISION !!
            pygame.event.post(pygame.event.Event(HIT_BLUE_DOG_EVENT))
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

def move_blue_dog(blue_dogs, boxes):
    for dog in blue_dogs:
        if dog.status == "vertical":
            if dog.initial == "UP":
                dog.rect.y -= DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.y - DOG_VEL  + 38 < 0 :
                        dog.rect.y += DOG_VEL
                        dog.initial = "DOWN"
            elif dog.initial == "DOWN":
                dog.rect.y += DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.y + 30 + DOG_VEL > HEIGHT:
                        dog.rect.y -= DOG_VEL
                        dog.initial = "UP"
        elif dog.status == "horizontal":
            if dog.initial == "LEFT":
                dog.rect.x -= DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.x - DOG_VEL < 0 :
                        dog.rect.x += DOG_VEL
                        dog.initial = "RIGHT"
            elif dog.initial == "RIGHT":
                dog.rect.x += DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.x + dog.rect.width + DOG_VEL > WIDTH:
                        dog.rect.x -= DOG_VEL
                        dog.initial = "LEFT"

def death(text):
    draw_text = DEATH_FONT.render(text, 1, RED)
    background_text = pygame.Surface((draw_text.get_width(), draw_text.get_height()))
    background_text.fill(BLACK)
    background_text.blit(draw_text, (0,0))
    WIN.blit(background_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
            
            

def main():
    BAKSO_PAGI_OST.play()
    cat = pygame.Rect(10,10, CAT_WIDTH, CAT_HEIGHT)
    orange_cat = pygame.Rect(WIDTH-50, HEIGHT-50, CAT_WIDTH, CAT_HEIGHT)
    boxes = []
    blue_dogs = []
    for i in BOX_COORDS:
        boxes.append(pygame.Rect(i, (BOX_WIDTH, BOX_HEIGHT)))
    for i in BLUE_DOG_COORDS:
        dog = BlueDog(pygame.Rect(i[0], i[1], DOG_WIDTH, DOG_HEIGHT), i[2], i[3])
        blue_dogs.append(dog)

    cat_HP = 10
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            
            if event.type == HIT_BLUE_DOG_EVENT:
                HIT_BLUE_DOG_SFX.play()
                BAKSO_PAGI_OST.stop()
                death("YOU DIED!")
                main()

        keys_pressed = pygame.key.get_pressed()
        move_cat(keys_pressed, cat, boxes)
        move_orange_cat(orange_cat)
        move_blue_dog(blue_dogs, boxes)
        draw_window(cat, orange_cat, boxes, blue_dogs)

        if cat.colliderect(orange_cat) :
            cat_HP -= 1 # WIP COLLISION !! COLLISION !! COLLISION !!
            print("COLLIDED! WITH CAT")

if __name__ == "__main__":
    main()
    # note 1: when making levels, update BOX_COORDS constant