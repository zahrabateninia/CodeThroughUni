import pygame
from settings import BULLET_VEL, WIDTH

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets[:]:  # Copy of the list to avoid iteration issues
        bullet.x += BULLET_VEL
        if red.rect.colliderect(bullet):
            red.health -= 1           # Direct damage, no event needed
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets[:]:
        bullet.x -= BULLET_VEL
        if yellow.rect.colliderect(bullet):
            yellow.health -= 1        # Direct damage, no event needed
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
