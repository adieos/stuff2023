import pygame
import os
import random
import ast
pygame.init()
pygame.mixer.init()
pygame.font.init()
MODE = "SMOOTH" # "ROUGH" or "SMOOTH"
# FINISHING: finish.mp3 and finish.png, and maybe reposition the finish tile?

with open('assets_catMaze\\boxCoords.txt', 'r') as file:
    box_coords = file.read()
 
with open('assets_catMaze\\blueDogCoords.txt', 'r') as file:
    blue_dog_coords = file.read()

 # display
WIDTH, HEIGHT = 900, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 5
pygame.display.set_caption("stupid cat game")
pygame.display.set_icon(pygame.image.load(os.path.join('assets_catMaze', 'cat.png')))

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LGREEN = (37, 196, 45)
DGREEN = (29, 153, 35)
RED = (255,0,0)
GREEN = (0, 255, 0)

# coords
BOX_COORDS = ast.literal_eval(box_coords)
BLUE_DOG_COORDS = ast.literal_eval(blue_dog_coords)
BLUE_KEY_COORD = (360, 360)
GHOST_BOX_COORDS = [(540, 420), (660, 420), (840, 420)]

# others
last_trigger = 0 # for the red dog movement bleeehhh
move = 1
VEL = 60
DOG_VEL = 25
RED_DOG_VEL = 30
ORANGE_CAT_MOVE = 1
DEATH_FONT = pygame.font.SysFont('comicsans', 80)
RED_DOG_MOVE_DELAY = 1500

# events
HIT_BLUE_DOG_EVENT = pygame.USEREVENT + 1
BLUE_KEY_PICK_EVENT = pygame.USEREVENT + 2
BLUE_LOCK_UNLOCK_EVENT = pygame.USEREVENT + 3
MOVE_RED_DOG_EVENT = pygame.USEREVENT + 4
RED_KEY_PICK_EVENT = pygame.USEREVENT + 5
RED_LOCK_UNLOCK_EVENT = pygame.USEREVENT + 6
WIN_EVENT = pygame.USEREVENT + 7

# sounds
BAKSO_MALAM_OST = pygame.mixer.Sound(os.path.join('assets_catMaze', 'baksoMalam.mp3'))
BAKSO_PAGI_OST = pygame.mixer.Sound(os.path.join('assets_catMaze', 'baksoPagi.mp3'))
LAGU = BAKSO_PAGI_OST
LAGU.set_volume(0.25)
HIT_BLUE_DOG_SFX = pygame.mixer.Sound(os.path.join('assets_catMaze', 'vineBoom.mp3'))
KEY_PICKUP_SFX = pygame.mixer.Sound(os.path.join('assets_catMaze', 'keyPick.mp3'))
LOCK_UNLOCK_SFX = pygame.mixer.Sound(os.path.join('assets_catMaze', 'unlock.mp3'))
WIN_SFX = pygame.mixer.Sound(os.path.join('assets_catMaze', 'finish.mp3'))
WIN_SFX.set_volume(0.60)

# images
CAT_WIDTH = 40
CAT_HEIGHT = 40
BOX_WIDTH = 60
BOX_HEIGHT = 60
DOG_WIDTH = 50
DOG_HEIGHT = 50
KEY_WIDTH, KEY_HEIGHT = 60, 60

CAT_RAW = pygame.image.load(os.path.join('assets_catMaze', 'cat.png'))
CAT = pygame.transform.scale(CAT_RAW, (CAT_WIDTH, CAT_HEIGHT))
ORANGE_CAT_RAW = pygame.image.load(os.path.join('assets_catMaze', 'cat.png'))
ORANGE_CAT = pygame.transform.scale(ORANGE_CAT_RAW, (CAT_WIDTH, CAT_HEIGHT))
BOX_RAW = pygame.image.load(os.path.join('assets_catMaze', 'box.png'))
BOX = pygame.transform.scale(BOX_RAW, (BOX_WIDTH, BOX_HEIGHT))
BLUEDOG_RAW = pygame.image.load(os.path.join('assets_catMaze', 'blueDog.png'))
BLUEDOG = pygame.transform.scale(BLUEDOG_RAW, (DOG_WIDTH, DOG_HEIGHT))
REDDOG_RAW = pygame.image.load(os.path.join('assets_catMaze', 'redDog.png'))
REDDOG = pygame.transform.scale(REDDOG_RAW, (DOG_WIDTH, DOG_HEIGHT))
BLUEKEY_RAW = pygame.image.load(os.path.join('assets_catMaze', 'blueKey.png'))
BLUEKEY = pygame.transform.scale(BLUEKEY_RAW, (KEY_WIDTH, KEY_HEIGHT))
BLUELOCK_RAW = pygame.image.load(os.path.join('assets_catMaze', 'blueLock.png'))
BLUELOCK = pygame.transform.scale(BLUELOCK_RAW, (KEY_WIDTH, KEY_HEIGHT))
REDKEY_RAW = pygame.image.load(os.path.join('assets_catMaze', 'redKey.png'))
REDKEY = pygame.transform.scale(REDKEY_RAW, (KEY_WIDTH, KEY_HEIGHT))
REDLOCK_RAW = pygame.image.load(os.path.join('assets_catMaze', 'redLock.png'))
REDLOCK = pygame.transform.scale(REDLOCK_RAW, (KEY_WIDTH, KEY_HEIGHT))
FINISH_RAW = pygame.image.load(os.path.join('assets_catMaze', 'finish.png'))
FINISH = pygame.transform.scale(FINISH_RAW, (60, 60))

class BlueDog:
    def __init__(self, rect, status, initial):
        self.rect = rect
        self.status = status
        self.initial = initial

def draw_window(cat, orange_cat, boxes, blue_dogs, blue_key, blue_lock, red_key, red_lock, finish):
    draw_grid()
    if (blue_key) : WIN.blit(BLUEKEY, (blue_key.x, blue_key.y))
    if (blue_lock) : WIN.blit(BLUELOCK, (blue_lock.x, blue_lock.y))
    if (red_key) : WIN.blit(REDKEY, (red_key.x, red_key.y))
    if (red_lock) : WIN.blit(REDLOCK, (red_lock.x, red_lock.y))
    WIN.blit(FINISH, (finish.x, finish.y))
    WIN.blit(CAT, (cat.x, cat.y))
    WIN.blit(REDDOG, (orange_cat.x, orange_cat.y)) # Turning this off will simply make the orange_cat invisible
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
    elif keys_pressed[pygame.K_d] and cat.x + VEL + CAT_WIDTH < WIDTH:
        cat.x += VEL
        for box in boxes:
            if cat.colliderect(box): cat.x -= VEL
    elif keys_pressed[pygame.K_w] and cat.y - VEL > 0:
        cat.y -= VEL
        for box in boxes:
            if cat.colliderect(box): cat.y += VEL
    elif keys_pressed[pygame.K_s] and cat.y + VEL + CAT_HEIGHT < HEIGHT:
        cat.y += VEL
        for box in boxes:
            if cat.colliderect(box): cat.y -= VEL

def move_red_dog(orange_cat, boxes, blue_lock, red_lock, ghost_boxes):
    global last_trigger
    global move
    blue_lock_gone = False
    red_lock_gone = False
    time_now = pygame.time.get_ticks()
    if (time_now-last_trigger) > RED_DOG_MOVE_DELAY:
        last_trigger = time_now
        move = random.randint(1,4)
        
    if not ORANGE_CAT_MOVE : return
    if not blue_lock: blue_lock_gone = True
    if not red_lock: red_lock_gone = True
    blue_collision = orange_cat.colliderect(blue_lock) if not blue_lock_gone else False
    red_collision = orange_cat.colliderect(red_lock) if not red_lock_gone else False
    if move == 1 and orange_cat.x - RED_DOG_VEL > 0:
        orange_cat.x -= RED_DOG_VEL
        for box in boxes:
            if orange_cat.colliderect(box) or blue_collision or red_collision:
                orange_cat.x += RED_DOG_VEL+5
                move = random.randint(1, 4)
    if move == 2 and orange_cat.y - RED_DOG_VEL > 0:
        orange_cat.y -= RED_DOG_VEL
        for box in boxes:
            if orange_cat.colliderect(box) or blue_collision or red_collision:
                orange_cat.y += RED_DOG_VEL+5
                move = random.randint(1, 4)
    if move == 3 and orange_cat.x + RED_DOG_VEL + DOG_WIDTH < WIDTH:
        orange_cat.x += RED_DOG_VEL
        for box in boxes:
            if orange_cat.colliderect(box) or blue_collision or red_collision:
                orange_cat.x -= RED_DOG_VEL+5
                move = random.randint(1, 4)
    if move == 4 and orange_cat.y + RED_DOG_VEL + DOG_HEIGHT < HEIGHT:
        orange_cat.y += RED_DOG_VEL
        for box in boxes:
            if orange_cat.colliderect(box) or blue_collision or red_collision:
                orange_cat.y -= RED_DOG_VEL+5
                move = random.randint(1, 4)
        for gbox in ghost_boxes:
            if orange_cat.colliderect(gbox):
                orange_cat.y -= VEL

def move_blue_dog(blue_dogs, boxes):
    for dog in blue_dogs:
        if dog.status == "vertical":
            if dog.initial == "UP":
                dog.rect.y -= DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.y - DOG_VEL < 0 :
                        dog.rect.y += DOG_VEL
                        dog.initial = "DOWN"
            elif dog.initial == "DOWN":
                dog.rect.y += DOG_VEL
                for box in boxes:
                    if dog.rect.colliderect(box) or dog.rect.y + 60 + DOG_VEL > HEIGHT:
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
            
def pickupBlue(cat, blue_key): # handles item pickup
    if not blue_key: return
    if cat.colliderect(blue_key):
        pygame.event.post(pygame.event.Event(BLUE_KEY_PICK_EVENT))

def pickupRed(cat, red_key):
    if not red_key: return
    if cat.colliderect(red_key):
        pygame.event.post(pygame.event.Event(RED_KEY_PICK_EVENT))
        
def unlockBlue(cat, blue_lock, has_blue_key):
    if not blue_lock: return
    if cat.colliderect(blue_lock):
        if has_blue_key:
            pygame.event.post(pygame.event.Event(BLUE_LOCK_UNLOCK_EVENT))
        else:
            cat.x -= VEL

def unlockRed(cat,  red_lock, has_red_key):
    if not red_lock: return
    if cat.colliderect(red_lock):
        if has_red_key:
            pygame.event.post(pygame.event.Event(RED_LOCK_UNLOCK_EVENT))
        else:
            cat.x += VEL

def draw_win(text):
    draw_text = DEATH_FONT.render(text, 1, GREEN)
    background_text = pygame.Surface((draw_text.get_width(), draw_text.get_height()))
    background_text.fill(BLACK)
    background_text.blit(draw_text, (0,0))
    WIN.blit(background_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    LAGU.play()
    cat = pygame.Rect(10,10, CAT_WIDTH, CAT_HEIGHT)
    orange_cat = pygame.Rect(720, 240, CAT_WIDTH, CAT_HEIGHT)
    boxes = []
    blue_dogs = []
    ghost_boxes = []
    blue_key = pygame.Rect(360, 360, KEY_WIDTH, KEY_HEIGHT)
    blue_lock = pygame.Rect(240, 180, BOX_WIDTH, BOX_HEIGHT)
    red_key = pygame.Rect(840, 0, KEY_WIDTH, KEY_HEIGHT)
    red_lock = pygame.Rect(780, 480, BOX_WIDTH, BOX_HEIGHT)
    finish = pygame.Rect(480, 480, 20, 20)

    for i in BOX_COORDS:
        boxes.append(pygame.Rect(i, (BOX_WIDTH, BOX_HEIGHT)))
    for i in BLUE_DOG_COORDS:
        dog = BlueDog(pygame.Rect(i[0], i[1], DOG_WIDTH, DOG_HEIGHT), i[2], i[3])
        blue_dogs.append(dog)
    for i in GHOST_BOX_COORDS:
        ghost_boxes.append(pygame.Rect(i, (BOX_WIDTH, BOX_HEIGHT)))

    has_blue_key = False
    has_red_key = False
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == HIT_BLUE_DOG_EVENT:
                HIT_BLUE_DOG_SFX.play()
                LAGU.stop()
                death("YOU DIED!")
                main()
            
            if event.type == BLUE_KEY_PICK_EVENT:
                KEY_PICKUP_SFX.play()
                blue_key = None
                has_blue_key = True

            if event.type == BLUE_LOCK_UNLOCK_EVENT:
                LOCK_UNLOCK_SFX.play()
                blue_lock = None
            
            if event.type == RED_KEY_PICK_EVENT:
                KEY_PICKUP_SFX.play()
                red_key = None
                has_red_key = True

            if event.type == RED_LOCK_UNLOCK_EVENT:
                LOCK_UNLOCK_SFX.play()
                red_lock = None
            
            if event.type == WIN_EVENT:
                WIN_SFX.play()
                LAGU.stop()
                draw_win("YOU WIN!")
                pygame.quit()
                quit()

        keys_pressed = pygame.key.get_pressed()
        move_cat(keys_pressed, cat, boxes)
        move_red_dog(orange_cat, boxes, blue_lock, red_lock, ghost_boxes)
        move_blue_dog(blue_dogs, boxes)
        pickupBlue(cat, blue_key)
        pickupRed(cat, red_key)
        unlockBlue(cat, blue_lock, has_blue_key)
        unlockRed(cat, red_lock, has_red_key)
        draw_window(cat, orange_cat, boxes, blue_dogs, blue_key, blue_lock, red_key, red_lock, finish)

        if cat.colliderect(orange_cat):
            pygame.event.post(pygame.event.Event(HIT_BLUE_DOG_EVENT))
        if cat.colliderect(finish):
            pygame.event.post(pygame.event.Event(WIN_EVENT))

if __name__ == "__main__":
    if MODE == "SMOOTH": FPS, VEL, DOG_VEL, RED_DOG_VEL = 60, 5, 2, 3
    if MODE == "ROUGH": FPS, VEL, DOG_VEL, RED_DOG_VEL = 5,60, 25, 30
    main()

'''
issues: 
1. there can only be one color of key and box because yes
2. this game isnt going to be developed into multiple levels for the time being. i plan on making platformers instead :P
'''