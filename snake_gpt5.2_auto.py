#!/usr/bin/env python3
"""
Snake (pygame) - single-file complete game.

Features:
- Score display
- Game Over screen with restart option
- Snake speeds up every time it eats food
"""

import sys
import random
import pygame


# ----------------------------
# Config
# ----------------------------
CELL_SIZE = 20
GRID_W, GRID_H = 30, 24  # 30*20=600, 24*20=480
WIDTH, HEIGHT = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
FPS_BASE = 10            # starting speed (frames/sec)
FPS_PER_FOOD = 1         # speed increase per food eaten
MAX_FPS = 45             # cap speed so it doesn't become unplayable

BG_COLOR = (18, 18, 18)
SNAKE_COLOR = (40, 200, 120)
SNAKE_HEAD_COLOR = (70, 255, 160)
FOOD_COLOR = (240, 70, 70)
TEXT_COLOR = (235, 235, 235)
MUTED_TEXT = (170, 170, 170)
PANEL_COLOR = (28, 28, 28)
BORDER_COLOR = (55, 55, 55)


# ----------------------------
# Helpers
# ----------------------------
def draw_cell(surface: pygame.Surface, pos, color, inset=2):
    """Draws a grid cell with a slight inset for nicer visuals."""
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE + inset, y * CELL_SIZE + inset,
                       CELL_SIZE - inset * 2, CELL_SIZE - inset * 2)
    pygame.draw.rect(surface, color, rect, border_radius=6)


def spawn_food(occupied: set[tuple[int, int]]) -> tuple[int, int]:
    """Spawn food on a free cell."""
    free = [(x, y) for x in range(GRID_W) for y in range(GRID_H) if (x, y) not in occupied]
    if not free:
        # Board full: player wins (handled elsewhere)
        return (-1, -1)
    return random.choice(free)


def render_text_center(surface: pygame.Surface, font: pygame.font.Font, text: str, y: int, color=TEXT_COLOR):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    surface.blit(img, rect)


# ----------------------------
# Game
# ----------------------------
def new_game_state():
    # Start snake in center, moving right
    start_x, start_y = GRID_W // 2, GRID_H // 2
    snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
    direction = (1, 0)  # dx, dy
    pending_dir = direction
    occupied = set(snake)
    food = spawn_food(occupied)
    score = 0
    fps = FPS_BASE
    return {
        "snake": snake,
        "direction": direction,
        "pending_dir": pending_dir,
        "occupied": occupied,
        "food": food,
        "score": score,
        "fps": fps,
        "alive": True,
        "won": False,
    }


def main():
    pygame.init()
    pygame.display.set_caption("Snake (pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font_small = pygame.font.SysFont("consolas", 20)
    font_medium = pygame.font.SysFont("consolas", 32, bold=True)
    font_large = pygame.font.SysFont("consolas", 52, bold=True)

    state = new_game_state()

    # To prevent repeated turns on long key-hold, we accept one direction change per tick.
    can_turn_this_tick = True

    while True:
        # ----------------------------
        # Events
        # ----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if not state["alive"]:
                    if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                        state = new_game_state()
                        can_turn_this_tick = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    continue

                # Direction changes (no immediate reversal)
                if can_turn_this_tick:
                    dx, dy = state["direction"]
                    if event.key in (pygame.K_UP, pygame.K_w) and (dx, dy) != (0, 1):
                        state["pending_dir"] = (0, -1)
                        can_turn_this_tick = False
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and (dx, dy) != (0, -1):
                        state["pending_dir"] = (0, 1)
                        can_turn_this_tick = False
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and (dx, dy) != (1, 0):
                        state["pending_dir"] = (-1, 0)
                        can_turn_this_tick = False
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and (dx, dy) != (-1, 0):
                        state["pending_dir"] = (1, 0)
                        can_turn_this_tick = False

        # ----------------------------
        # Update
        # ----------------------------
        if state["alive"]:
            state["direction"] = state["pending_dir"]

            dx, dy = state["direction"]
            head_x, head_y = state["snake"][-1]
            new_head = (head_x + dx, head_y + dy)

            # Wall collision
            if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
                state["alive"] = False
            else:
                ate_food = (new_head == state["food"])

                # Self collision:
                # If not eating, tail will move away, so it's okay to step into the current tail.
                tail = state["snake"][0]
                occupied = state["occupied"]

                if ate_food:
                    # new_head must not be in occupied at all
                    if new_head in occupied:
                        state["alive"] = False
                else:
                    # allow moving into tail because it will be removed
                    if new_head in occupied and new_head != tail:
                        state["alive"] = False

                if state["alive"]:
                    # Move snake
                    state["snake"].append(new_head)
                    occupied.add(new_head)

                    if ate_food:
                        state["score"] += 1
                        # Speed up each time it eats food
                        state["fps"] = min(MAX_FPS, FPS_BASE + state["score"] * FPS_PER_FOOD)

                        # Spawn new food
                        state["food"] = spawn_food(occupied)
                        if state["food"] == (-1, -1):
                            state["alive"] = False
                            state["won"] = True
                    else:
                        # Remove tail
                        removed = state["snake"].pop(0)
                        occupied.remove(removed)

            can_turn_this_tick = True  # allow a turn next tick

        # ----------------------------
        # Draw
        # ----------------------------
        screen.fill(BG_COLOR)

        # Subtle grid (optional, but nice)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (24, 24, 24), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (24, 24, 24), (0, y), (WIDTH, y))

        # Food
        if state["food"] != (-1, -1):
            draw_cell(screen, state["food"], FOOD_COLOR, inset=3)

        # Snake
        for seg in state["snake"][:-1]:
            draw_cell(screen, seg, SNAKE_COLOR, inset=3)
        draw_cell(screen, state["snake"][-1], SNAKE_HEAD_COLOR, inset=2)

        # Score panel
        panel_rect = pygame.Rect(10, 10, 220, 42)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=10)
        pygame.draw.rect(screen, BORDER_COLOR, panel_rect, width=2, border_radius=10)
        score_txt = font_small.render(f"Score: {state['score']}   Speed: {state['fps']}", True, TEXT_COLOR)
        screen.blit(score_txt, (20, 20))

        # Game Over overlay
        if not state["alive"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            if state.get("won", False):
                render_text_center(screen, font_large, "YOU WIN!", HEIGHT // 2 - 70)
                render_text_center(screen, font_medium, f"Final Score: {state['score']}", HEIGHT // 2 - 10)
            else:
                render_text_center(screen, font_large, "GAME OVER", HEIGHT // 2 - 70)
                render_text_center(screen, font_medium, f"Final Score: {state['score']}", HEIGHT // 2 - 10)

            render_text_center(screen, font_small, "Press R / Enter / Space to Restart", HEIGHT // 2 + 40, color=TEXT_COLOR)
            render_text_center(screen, font_small, "Press Esc to Quit", HEIGHT // 2 + 70, color=MUTED_TEXT)

        pygame.display.flip()

        # Control speed
        clock.tick(state["fps"] if state["alive"] else 30)


if __name__ == "__main__":
    main()
