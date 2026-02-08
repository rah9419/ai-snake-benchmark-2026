import pygame
import random
import sys


# Initialize pygame
pygame.init()

# ---------- Game Settings ----------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20

INITIAL_SPEED = 10        # Initial frames per second
SPEED_INCREMENT = 1       # How much to speed up after each food

# Colors (R, G, B)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (200, 0,   0)
GREEN  = (0,   200, 0)
DARK_GREEN = (0, 155, 0)
BLUE   = (0,   0, 255)
YELLOW = (255, 255, 0)
GRAY   = (40,  40,  40)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Fonts
score_font = pygame.font.SysFont("consolas", 24)
game_over_font = pygame.font.SysFont("consolas", 48)
info_font = pygame.font.SysFont("consolas", 24)


def draw_grid():
    """Draw a subtle grid to make movement clearer."""
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(snake_list):
    """Draw the snake blocks from the snake_list positions."""
    for segment in snake_list:
        x, y = segment
        pygame.draw.rect(screen, DARK_GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(screen, GREEN, [x + 2, y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4])


def show_score(score, speed):
    """Display current score and speed at the top-left."""
    score_surface = score_font.render(f"Score: {score}", True, YELLOW)
    speed_surface = score_font.render(f"Speed: {speed} FPS", True, YELLOW)
    screen.blit(score_surface, (10, 10))
    screen.blit(speed_surface, (10, 10 + score_surface.get_height() + 4))


def random_food_position():
    """Return a random food position aligned to the grid."""
    x = random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    y = random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    return x, y


def game_over_screen(score):
    """Show the Game Over screen and handle restart / quit."""
    screen.fill(BLACK)

    title_text = game_over_font.render("GAME OVER", True, RED)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
    screen.blit(title_text, title_rect)

    score_text = info_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(score_text, score_rect)

    info_text = info_font.render("Press R to Restart or Q to Quit", True, WHITE)
    info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
    screen.blit(info_text, info_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False  # Return to start a new game


def game_loop():
    # Initial snake position and movement
    x = WINDOW_WIDTH // 2
    y = WINDOW_HEIGHT // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    # Initial food position
    food_x, food_y = random_food_position()

    # Score and speed
    score = 0
    snake_speed = INITIAL_SPEED

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = BLOCK_SIZE

        # If the snake hasn't started moving yet, don't update position
        if dx != 0 or dy != 0:
            x += dx
            y += dy

        # --- Collision with walls (Game Over) ---
        if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            game_over_screen(score)
            return  # End this game_loop, outer loop will restart a new game

        # --- Update snake body ---
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # --- Collision with self (Game Over) ---
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over_screen(score)
                return

        # --- Food collision ---
        if x == food_x and y == food_y:
            snake_length += 1
            score += 1
            snake_speed += SPEED_INCREMENT  # Speed up after each food
            food_x, food_y = random_food_position()

        # --- Drawing ---
        screen.fill(BLACK)
        draw_grid()

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw snake
        draw_snake(snake_list)

        # Draw score and speed
        show_score(score, snake_speed)

        pygame.display.flip()

        # Control the game speed
        clock.tick(snake_speed)


def main():
    while True:
        game_loop()  # After game over, control comes back here and restarts


if __name__ == "__main__":
    main()
