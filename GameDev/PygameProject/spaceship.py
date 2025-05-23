import pygame
from settings import VEL, HEIGHT

class Spaceship:
    def __init__(self, x, y, image, controls, boundary_left, boundary_right):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.image = image
        self.controls = controls
        self.health = 10
        self.boundary_left = boundary_left
        self.boundary_right = boundary_right

    def handle_movement(self, keys):
        if keys[self.controls["left"]] and self.rect.x - VEL > self.boundary_left:
            self.rect.x -= VEL
        if keys[self.controls["right"]] and self.rect.x + VEL + self.rect.width < self.boundary_right:
            self.rect.x += VEL
        if keys[self.controls["up"]] and self.rect.y - VEL > 0:
            self.rect.y -= VEL
        if keys[self.controls["down"]] and self.rect.y + VEL + self.rect.height < HEIGHT - 15:
            self.rect.y += VEL
