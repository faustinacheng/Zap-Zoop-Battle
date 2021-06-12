import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500    # Dimensions of window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zap Zoop Battle") # Sets window title

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4

YELLOW_HIT = pygame.USEREVENT + 1   # creating custom user event
RED_HIT = pygame.USEREVENT + 2
HP_PER_HIT = 5

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, 500)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

WINNER_FONT = pygame.font.SysFont("impact", 130)
SCORE_FONT = pygame.font.SysFont("helvetica", 20)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

class Scores:
    red_score = 0
    yellow_score = 0

def draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))      # When you want to draw surfaces onto screen (ie. text/images) order of drawing matters, can draw on top of other surfaces
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    red_scoreboard = SCORE_FONT.render(f"ROUNDS WON: {Scores.red_score}", 1, WHITE)
    WIN.blit(red_scoreboard, (10, 10))
    yellow_scoreboard = SCORE_FONT.render(f"ROUNDS WON: {Scores.yellow_score}", 1, WHITE)
    WIN.blit(yellow_scoreboard, (WIDTH - yellow_scoreboard.get_width() - 10, 10))   

    red_hp_white = pygame.Rect(red.x, red.y - 15, red.width, 7)
    pygame.draw.rect(WIN, WHITE, red_hp_white)
    red_hp_red = pygame.Rect(red.x, red.y - 15, red_hp, 7)
    pygame.draw.rect(WIN, RED, red_hp_red)
    yellow_hp_white = pygame.Rect(yellow.x, yellow.y - 15, yellow.width, 7)
    pygame.draw.rect(WIN, WHITE, yellow_hp_white)
    yellow_hp_red = pygame.Rect(yellow.x, yellow.y - 15, yellow_hp, 7)
    pygame.draw.rect(WIN, RED, yellow_hp_red)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)   

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - 15 - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height: # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - 15 - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x >= WIDTH:
            yellow_bullets.remove(bullet) 
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + bullet.width <= 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, YELLOW)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    red = pygame.Rect(WIDTH - 100 - SPACESHIP_HEIGHT, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH) # x position, y position, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    red_hp = red.width
    yellow_hp = yellow.width

    red_bullets = []
    yellow_bullets = []

    winner_text = ""

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_COMMA and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
            if event.type == RED_HIT:
                red_hp -= HP_PER_HIT
                BULLET_HIT_SOUND.play()
                if red_hp <= 0:
                    Scores.red_score += 1
                    winner_text = "YELLOW WINS!"

            if event.type == YELLOW_HIT:
                yellow_hp -= HP_PER_HIT
                BULLET_HIT_SOUND.play()
                if yellow_hp <= 0:
                    Scores.yellow_score += 1
                    winner_text = "RED WINS!"

        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() # tells us what keys are pressed down
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
    
        draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)    
    
    pygame.event.clear()
    main()

if __name__ == "__main__":
    main()
