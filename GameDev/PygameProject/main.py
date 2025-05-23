import pygame
import os
from spaceship import Spaceship
from game import draw_window, draw_winner
from bullet import handle_bullets
from settings import *

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modular Game")

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

# Load images
YELLOW_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_IMG = pygame.transform.rotate(pygame.transform.scale(YELLOW_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_IMG = pygame.transform.rotate(pygame.transform.scale(RED_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def main():
    yellow_controls = {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_q}
    red_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "shoot": pygame.K_p}

    yellow = Spaceship(100, 300, YELLOW_IMG, yellow_controls, 0, BORDER.x)
    red = Spaceship(700, 300, RED_IMG, red_controls, BORDER.x + BORDER.width, WIDTH)

    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == yellow.controls["shoot"] and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.rect.x + yellow.rect.width, yellow.rect.y + yellow.rect.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == red.controls["shoot"] and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.rect.x, red.rect.y + red.rect.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red.health -= 1
            if event.type == YELLOW_HIT:
                yellow.health -= 1

        winner_text = ""
        if red.health <= 0:
            winner_text = "Yellow Wins!"
        if yellow.health <= 0:
            winner_text = "Red Wins!"

        if winner_text:
            draw_winner(WIN, winner_text)
            break

        keys = pygame.key.get_pressed()
        yellow.handle_movement(keys)
        red.handle_movement(keys)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(WIN, SPACE, BORDER, yellow, red, yellow_bullets, red_bullets)
        

    pygame.quit()

if __name__ == "__main__":
    main()
