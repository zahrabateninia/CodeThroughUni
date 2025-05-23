import pygame
from settings import *
from bullet import handle_bullets
pygame.font.init()

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)


def draw_window(win, bg, border, yellow, red, yellow_bullets, red_bullets):
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, BLACK, border)

    yellow_text = HEALTH_FONT.render("Health: " + str(yellow.health), 1, WHITE)
    red_text = HEALTH_FONT.render("Health: " + str(red.health), 1, WHITE)

    win.blit(yellow_text, (10, 10))
    win.blit(red_text, (WIDTH - red_text.get_width() - 10, 10))

    win.blit(yellow.image, (yellow.rect.x, yellow.rect.y))
    win.blit(red.image, (red.rect.x, red.rect.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(win, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(win, RED, bullet)

    pygame.display.update()


def draw_winner(win, text):
    font = pygame.font.SysFont('comicsans', 100)
    draw_text = font.render(text, 1, WHITE)
    win.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
