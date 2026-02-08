import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Snake settings
SNAKE_SIZE = 15
initial_speed = 10


def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(WIN, GREEN, (x, y, SNAKE_SIZE, SNAKE_SIZE))


def message(text, color, y_offset=0, size=28):
    font_style = pygame.font.SysFont("comicsansms", size)
    msg = font_style.render(text, True, color)
    WIN.blit(msg, (WIDTH/2 - msg.get_width()/2, HEIGHT/2 - msg.get_height()/2 + y_offset))


def game_loop():
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    speed = initial_speed
    score = 0

    while not game_over:

        while game_close:
            WIN.fill(BLACK)
            message("GAME OVER", RED, -40, 40)
            message(f"Score: {score}", WHITE, 10, 30)
            message("Press R to Restart or Q to Quit", WHITE, 60, 20)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -SNAKE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = SNAKE_SIZE

        # Move snake
        x += dx
        y += dy

        # Boundary collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        WIN.fill(BLACK)
        pygame.draw.rect(WIN, RED, (food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            snake_list.pop(0)

        # Self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)

        # Display score
        font = pygame.font.SysFont("comicsansms", 22)
        score_text = font.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

        pygame.display.update()

        # Snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            snake_length += 1
            score += 1
            speed += 1  # Increase speed every time snake eats

        clock.tick(speed)

    pygame.quit()
    sys.exit()


game_loop()
