import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("دایره ساده")

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

x = random.randint(50, 550)
y = random.randint(50, 350)
radius = 30
color = random_color()

running = True
while running:
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # چک می‌کنیم آیا کلیک داخل مربع اطراف دایره بوده یا نه
            if x - radius <= mx <= x + radius and y - radius <= my <= y + radius:
                color = random_color()
                radius = random.randint(10, 60)
                x = random.randint(radius, 600 - radius)
                y = random.randint(radius, 400 - radius)

pygame.quit()