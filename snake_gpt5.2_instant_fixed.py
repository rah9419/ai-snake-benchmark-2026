import pygame
import random
import sys

# -------------------- INITIAL SETUP --------------------
pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 48)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# -------------------- GAME STATE --------------------
def reset_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = spawn_food(snake)
    score = 0
    speed = 10
    return snake, direction, food, score, speed

def spawn_food(snake):
    attempts = 0
    while attempts < 1000:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)
        attempts += 1
    return (0, 0)  # Fallback if board is nearly full

snake, direction, food, score, speed = reset_game()
game_over = False

# -------------------- DRAW FUNCTIONS --------------------
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (*block, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_game_over():
    global score
    screen.fill(BLACK)
    title = BIG_FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    restart_text = FONT.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 170))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 210))
    pygame.display.flip()

# -------------------- MAIN LOOP --------------------
running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
            else:
                if event.key == pygame.K_r:
                    snake, direction, food, score, speed = reset_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

    if game_over:
        draw_game_over()
        continue

    # Move snake
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)

    # Collision with wall
    if (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT or
        new_head in snake
    ):
        game_over = True
        continue

    snake.insert(0, new_head)

    # Eating food
    if new_head == food:
        score += 1
        speed = min(speed + 0.5, 15)  # SPEED INCREASE (capped at 15)
        food = spawn_food(snake)
    else:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    draw_score(score)
    pygame.display.flip()

pygame.quit()
sys.exit()
