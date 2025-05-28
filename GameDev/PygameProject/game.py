import pygame
from settings import *
from bullet import handle_bullets
pygame.font.init()

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)


def draw_window(win, bg, border, yellow, red, yellow_bullets, red_bullets, yellow_name, red_name):
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, BLACK, border)

    yellow_text = HEALTH_FONT.render(f"{yellow_name}: {yellow.health}", 1, WHITE)
    red_text = HEALTH_FONT.render(f"{red_name}: {red.health}", 1, WHITE)


    win.blit(yellow_text, (10, 10))
    win.blit(red_text, (WIDTH - red_text.get_width() - 10, 10))

    win.blit(yellow.image, (yellow.rect.x, yellow.rect.y))
    win.blit(red.image, (red.rect.x, red.rect.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(win, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(win, RED, bullet)

    pygame.display.update()


def end_screen(win, winner_name, loser_name):
    font = pygame.font.SysFont('comicsans', 60)
    small_font = pygame.font.SysFont('comicsans', 30)
    countdown = 10

    running = True
    while running:
        win.fill((0, 0, 0))

        # Game over message
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 50))

        # winner
        winner_display = small_font.render(f"Winner: {winner_name}", True, (255, 255, 255))
        win.blit(winner_display, (WIDTH // 2 - winner_display.get_width() // 2, 150))

        # loser
        loser_display = small_font.render(f"Loser: {loser_name}", True, (200, 200, 200))
        win.blit(loser_display, (WIDTH // 2 - loser_display.get_width() // 2, 200))

        # reset button 
        restart_text = small_font.render("Press R to Restart", True, (0, 255, 0))
        win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 300))

        # timer 
        timer_text = small_font.render(f"Exiting in {countdown}...", True, (255, 100, 100))
        win.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # just go back to restart

        pygame.time.delay(1000)
        countdown -= 1
        if countdown == 0:
            pygame.quit()
            exit()