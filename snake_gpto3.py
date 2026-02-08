import pygame
import random
import sys

# ---------- CONFIG -----------------------------------------------------------
WIDTH, HEIGHT = 640, 480          # window size
BLOCK_SIZE = 20                   # size of each snake segment & food square
START_SPEED = 10                  # initial game speed (frames per second)
SPEED_INCREMENT = 1               # how much FPS increases after each meal
FONT_NAME = pygame.font.get_default_font()
# -----------------------------------------------------------------------------


def draw_text(surface, text, size, color, x, y, center=False):
    """Render text on the given surface."""
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(render, rect)


def random_food_position(snake_body):
    """Return a food position that is not on the snake."""
    while True:
        pos = (
            random.randrange(0, WIDTH, BLOCK_SIZE),
            random.randrange(0, HEIGHT, BLOCK_SIZE),
        )
        if pos not in snake_body:
            return pos


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — Pygame Edition")
    clock = pygame.time.Clock()

    # Colors (RGB)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (200,   0,   0)
    GREEN = (  0, 180,   0)

    # Initial game state
    snake_body = [(WIDTH // 2, HEIGHT // 2)]
    direction = (BLOCK_SIZE, 0)  # moving right
    food_pos = random_food_position(snake_body)
    speed = START_SPEED
    score = 0
    game_over = False

    while True:  # main loop (handles restart)
        while not game_over:
            # -------------- EVENT HANDLING -----------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction[1] == 0:
                        direction = (0, -BLOCK_SIZE)
                    elif event.key == pygame.K_DOWN and direction[1] == 0:
                        direction = (0, BLOCK_SIZE)
                    elif event.key == pygame.K_LEFT and direction[0] == 0:
                        direction = (-BLOCK_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction[0] == 0:
                        direction = (BLOCK_SIZE, 0)

            # -------------- MOVE SNAKE ---------------------------------------
            new_head = (snake_body[0][0] + direction[0],
                        snake_body[0][1] + direction[1])
            snake_body.insert(0, new_head)

            # Check collisions with walls
            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_over = True

            # Check collisions with itself
            if new_head in snake_body[1:]:
                game_over = True

            # Check if food eaten
            if new_head == food_pos:
                score += 1
                speed += SPEED_INCREMENT
                food_pos = random_food_position(snake_body)
            else:
                snake_body.pop()  # remove tail segment if no food eaten

            # -------------- RENDERING ----------------------------------------
            screen.fill(BLACK)

            # Draw food
            pygame.draw.rect(screen, RED,
                             (*food_pos, BLOCK_SIZE, BLOCK_SIZE))

            # Draw snake
            for segment in snake_body:
                pygame.draw.rect(screen, GREEN,
                                 (*segment, BLOCK_SIZE, BLOCK_SIZE))

            # Draw score
            draw_text(screen, f"Score: {score}", 24, WHITE, 8, 8)

            pygame.display.flip()
            clock.tick(speed)

        # ---------------- GAME-OVER SCREEN -----------------------------------
        draw_text(screen, "GAME OVER", 64, RED, WIDTH // 2, HEIGHT // 3, center=True)
        draw_text(screen, f"Final Score: {score}", 32, WHITE,
                  WIDTH // 2, HEIGHT // 2, center=True)
        draw_text(screen, "Press R to Restart or Q to Quit", 24, WHITE,
                  WIDTH // 2, HEIGHT // 2 + 60, center=True)
        pygame.display.flip()

        # Wait for restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        # reset game state
                        snake_body[:] = [(WIDTH // 2, HEIGHT // 2)]
                        direction = (BLOCK_SIZE, 0)
                        food_pos = random_food_position(snake_body)
                        speed = START_SPEED
                        score = 0
                        game_over = False
                        waiting = False

            clock.tick(10)  # limit game-over loop speed


if __name__ == "__main__":
    game_loop()
