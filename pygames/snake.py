import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen settings
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("🌿 Snake Game - Jungle Theme 🌿")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (34, 139, 34)  # Jungle Green
yellow = (255, 255, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
orange = (255, 140, 0)

# Snake settings
snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load jungle background
bg_image = pygame.image.load("jungle_bg.png")
bg_image = pygame.transform.scale(bg_image, (width, height))

# High Score system
high_score = 0

def show_score(score):
    score_text = score_font.render(f"Score: {score}", True, yellow)
    win.blit(score_text, [10, 10])

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(win, green, [block[0], block[1], snake_block, snake_block])

def message(msg, color, x, y, size=25):
    text = pygame.font.SysFont("bahnschrift", size).render(msg, True, color)
    win.blit(text, [x, y])

def game_intro():
    flashing = True
    intro = True
    while intro:
        win.fill(black)
        win.blit(bg_image, (0, 0))
        message("🐍 WELCOME TO SNAKE GAME 🐍", yellow, width / 6, height / 5, 35)
        
        if flashing:
            message("Press SPACE to Start", red, width / 3, height / 2, 30)
        
        pygame.display.update()
        time.sleep(0.5)  # Creates flashing effect
        flashing = not flashing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

def game_loop():
    global high_score
    game_over = False
    game_close = False

    x, y = width / 2, height / 2
    x_change, y_change = 0, 0
    snake_list = []
    length = 1

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            win.fill(black)
            message("Game Over! Press C-Play Again or Q-Quit", red, width / 6, height / 3, 30)
            show_score(length - 1)
            pygame.display.update()

            if length - 1 > high_score:
                high_score = length - 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        win.fill(black)
        win.blit(bg_image, (0, 0))
        pygame.draw.rect(win, orange, [food_x, food_y, snake_block, snake_block])

        snake_list.append([x, y])
        if len(snake_list) > length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == [x, y]:
                game_close = True

        draw_snake(snake_list)
        show_score(length - 1)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_intro()
game_loop()
