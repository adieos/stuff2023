import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spaceship batle pew pew") # title
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
VEL = 3 # velocity
BULLET_VEL = 5
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets_spaceshipBattle', 'Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets_spaceshipBattle', 'Gun.mp3'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_spaceshipBattle', 'spaceship_yellow.png')) # using join() bc other os may not use \
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_spaceshipBattle', 'spaceship_red.png'))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.image.load(os.path.join('assets_spaceshipBattle', 'space.png'))
SPACEBG = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_HP, yellow_HP):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) # WOW !!!???
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y)) # from top left corner (both window and image)
    WIN.blit(RED_SHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render(f"HP: {str(red_HP)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"HP: {str(yellow_HP)}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() # MUST !!

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT YELLOW
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT YELLOW
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # DOWN YELLOW
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP YELLOW
        yellow.y -= VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL  - 15> BORDER.x: # LEFT RED
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 12 < WIDTH: # RIGHT RED
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # DOWN RED
        red.y += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP RED
        red.y -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # ONLY IF BOTH ARE RECT
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): # ONLY IF BOTH ARE RECT
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    
    red_HP = 10
    yellow_HP = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() # coded this way to ensure game can restart after someone won
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 15, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_HP -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_HP -= 1
                BULLET_HIT_SOUND.play()
                    
        winner_text = ""
        if red_HP <= 0:
            winner_text = "Yellow won!"

        if yellow_HP <= 0:
            winner_text = "Red won!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() # ScancodeWrapper class
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_HP, yellow_HP)
        

    main()

if __name__ == "__main__":
    main()