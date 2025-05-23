import pygame
from settings import BULLET_VEL, RED_HIT, YELLOW_HIT, WIDTH

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets[:]:
        bullet.x += BULLET_VEL
        if red.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets[:]:
        bullet.x -= BULLET_VEL
        if yellow.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
