import pygame
import os
from spaceship import Spaceship
from game import draw_window, end_screen #تغییر کرد
from bullet import handle_bullets
from settings import *

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Combat")
pygame.mixer.init()
YELLOW_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
RED_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3')) 

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

# Load images
YELLOW_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_IMG = pygame.transform.rotate(pygame.transform.scale(YELLOW_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_IMG = pygame.transform.rotate(pygame.transform.scale(RED_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#جدید اضافه شد
def login_screen():
    FONT = pygame.font.SysFont('comicsans', 40)
    input_active = True
    player1_name = ""
    player2_name = ""
    current_player = 1
    clock = pygame.time.Clock()

    while True:
        WIN.fill((0, 0, 0))

        if current_player == 1:
            prompt = "Enter Player 1 Name:"
        else:
            prompt = "Enter Player 2 Name:"

        prompt_render = FONT.render(prompt, True, (255, 255, 255))
        input_render = FONT.render((player1_name if current_player == 1 else player2_name), True, (0, 255, 0))

        WIN.blit(prompt_render, (WIDTH//2 - prompt_render.get_width()//2, HEIGHT//2 - 50))
        WIN.blit(input_render, (WIDTH//2 - input_render.get_width()//2, HEIGHT//2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_player == 1 and player1_name.strip():
                        current_player = 2
                    elif current_player == 2 and player2_name.strip():
                        return player1_name, player2_name
                elif event.key == pygame.K_BACKSPACE:
                    if current_player == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                else:
                    if current_player == 1:
                        player1_name += event.unicode
                    else:
                        player2_name += event.unicode

        clock.tick(60)


def show_instructions(yellow_name, red_name):
    FONT = pygame.font.SysFont('comicsans', 24)
    BIG_FONT = pygame.font.SysFont('comicsans', 40)

    waiting = True
    while waiting:
        WIN.fill((0, 0, 30))  # blackish background

        # main title
        title = BIG_FONT.render("Welcome to the Game!", True, (255, 255, 0))
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        start_y = 100

        # yellow player section
        yellow_title = FONT.render(f"{yellow_name} (Yellow)", True, (255, 255, 0))
        yellow_controls = [
            "Move: W, A, S, D",
            "Shoot: Q",
            "You have 10 Lives"
        ]

        WIN.blit(yellow_title, (WIDTH // 2 - yellow_title.get_width() // 2, start_y))
        for i, line in enumerate(yellow_controls):
            text = FONT.render(line, True, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, start_y + 30 + i * 30))

        # red player section
        offset = start_y + 30 + len(yellow_controls) * 30 + 30  
        red_title = FONT.render(f"{red_name} (Red)", True, (255, 0, 0))
        red_controls = [
            "Move: K_UP, K_DOWN, K_LEFT, K_RIGHT",
            "Shoot: P",
            "You have 10 Lives"
        ]


        WIN.blit(red_title, (WIDTH // 2 - red_title.get_width() // 2, offset))
        for i, line in enumerate(red_controls):
            text = FONT.render(line, True, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, offset + 30 + i * 30))

        # ending message
        start_msg = FONT.render("Press SPACE to start playing.", True, (0, 255, 0))
        WIN.blit(start_msg, (WIDTH // 2 - start_msg.get_width() // 2, HEIGHT - 80))

        restart_msg = FONT.render("Press R to restart the game after it ends.", True, (255, 255, 255))
        WIN.blit(restart_msg, (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT - 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


 

def main(yellow_name, red_name):
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
                    YELLOW_SHOOT_SOUND.play()#اضافه شد

                if event.key == red.controls["shoot"] and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.rect.x, red.rect.y + red.rect.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    RED_SHOOT_SOUND.play()
                    

            if event.type == RED_HIT:
                red.health -= 1
            if event.type == YELLOW_HIT:
                yellow.health -= 1

        winner_text = ""
        if red.health <= 0:
            return yellow_name  

        if yellow.health <= 0:
            return red_name  



        if winner_text:
            end_screen(WIN, winner_text, loser_name)
            main(yellow_name, red_name)


        keys = pygame.key.get_pressed()
        yellow.handle_movement(keys)
        red.handle_movement(keys)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(WIN, SPACE, BORDER, yellow, red, yellow_bullets, red_bullets, yellow_name, red_name)
        

    pygame.quit()

if __name__ == "__main__":
    yellow_name, red_name = login_screen()
    while True:
        winner = main(yellow_name, red_name)
        loser = red_name if winner == yellow_name else yellow_name
        end_screen(WIN, winner, loser)