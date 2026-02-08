#!/usr/bin/env python3
"""
Snake (Pygame) - single file
Requirements:
- Score display
- Game Over screen with restart option
- Snake speeds up each time it eats food
"""

import sys
import random
import pygame

# -----------------------------
# Config
# -----------------------------
WINDOW_W, WINDOW_H = 720, 480
CELL = 24  # grid cell size (pixels) - keep WINDOW_* divisible by CELL for clean grid
FPS_BASE = 10  # starting speed (frames per second)
FPS_STEP = 1   # speed increment per food eaten
FPS_MAX = 35   # cap speed to keep it playable

# Colors
BLACK = (12, 12, 14)
WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
DARK = (28, 28, 34)
RED = (220, 50, 60)
GREEN = (40, 210, 120)
YELLOW = (240, 210, 60)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# -----------------------------
# Helpers
# -----------------------------
def clamp(n, lo, hi):
    return lo if n < lo else hi if n > hi else n

def grid_size():
    return WINDOW_W // CELL, WINDOW_H // CELL

def random_food_position(occupied_set):
    gw, gh = grid_size()
    all_cells = gw * gh
    if len(occupied_set) >= all_cells:
        return None  # no space
    while True:
        pos = (random.randrange(gw), random.randrange(gh))
        if pos not in occupied_set:
            return pos

def draw_text(surface, text, font, color, center):
    img = font.render(text, True, color)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)

def draw_cell(surface, pos, color, inset=2, radius=6):
    x, y = pos
    r = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    r.inflate_ip(-inset, -inset)
    pygame.draw.rect(surface, color, r, border_radius=radius)

def draw_grid(surface):
    # subtle grid
    gw, gh = grid_size()
    for x in range(gw + 1):
        px = x * CELL
        pygame.draw.line(surface, (18, 18, 22), (px, 0), (px, WINDOW_H))
    for y in range(gh + 1):
        py = y * CELL
        pygame.draw.line(surface, (18, 18, 22), (0, py), (WINDOW_W, py))

# -----------------------------
# Game State
# -----------------------------
class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        gw, gh = grid_size()
        start = (gw // 2, gh // 2)
        self.snake = [start, (start[0] - 1, start[1]), (start[0] - 2, start[1])]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.food = random_food_position(set(self.snake))
        self.alive = True
        self.victory = False
        self.speed_fps = FPS_BASE

        # Movement pacing independent from FPS so it feels consistent
        self.move_interval_ms = int(1000 / self.speed_fps)
        self._accum_ms = 0

    def set_direction(self, d):
        # Prevent 180-degree reversal
        dx, dy = d
        cx, cy = self.direction
        if (dx, dy) == (-cx, -cy):
            return
        self.next_direction = d

    def _update_speed(self):
        self.speed_fps = clamp(FPS_BASE + self.score * FPS_STEP, FPS_BASE, FPS_MAX)
        self.move_interval_ms = int(1000 / self.speed_fps)

    def step(self, dt_ms):
        if not self.alive:
            return

        self._accum_ms += dt_ms
        while self._accum_ms >= self.move_interval_ms and self.alive:
            self._accum_ms -= self.move_interval_ms
            self._move_once()

    def _move_once(self):
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        gw, gh = grid_size()

        # Wall collision
        if new_head[0] < 0 or new_head[0] >= gw or new_head[1] < 0 or new_head[1] >= gh:
            self.alive = False
            return

        # Self collision (note: moving into the tail is allowed if tail will move away)
        tail = self.snake[-1]
        body_set = set(self.snake[:-1])  # exclude tail for collision check unless growing
        if new_head in body_set:
            self.alive = False
            return

        ate = (self.food is not None and new_head == self.food)

        # Insert new head
        self.snake.insert(0, new_head)

        if ate:
            self.score += 1
            self._update_speed()

            occupied = set(self.snake)
            self.food = random_food_position(occupied)

            if self.food is None:
                # Grid full => win
                self.victory = True
                self.alive = False
                return
        else:
            # Normal move: pop tail
            self.snake.pop()

# -----------------------------
# Main
# -----------------------------
def main():
    pygame.init()
    pygame.display.set_caption("Snake (Pygame)")
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    # Fonts
    font_small = pygame.font.SysFont("consolas", 18)
    font_med = pygame.font.SysFont("consolas", 28, bold=True)
    font_big = pygame.font.SysFont("consolas", 44, bold=True)

    game = SnakeGame()

    def draw_play():
        screen.fill(BLACK)
        draw_grid(screen)

        # Food
        if game.food is not None:
            draw_cell(screen, game.food, YELLOW, inset=4, radius=8)

        # Snake
        for i, seg in enumerate(game.snake):
            if i == 0:
                draw_cell(screen, seg, GREEN, inset=2, radius=10)
            else:
                draw_cell(screen, seg, (30, 180, 110), inset=3, radius=8)

        # HUD
        score_text = f"Score: {game.score}"
        speed_text = f"Speed: {game.speed_fps} fps"
        hud = font_small.render(score_text, True, WHITE)
        hud2 = font_small.render(speed_text, True, GRAY)
        screen.blit(hud, (10, 8))
        screen.blit(hud2, (10, 28))

    def draw_game_over():
        # Dim overlay
        overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = "YOU WIN!" if game.victory else "GAME OVER"
        draw_text(screen, title, font_big, RED if not game.victory else GREEN, (WINDOW_W // 2, WINDOW_H // 2 - 60))

        draw_text(
            screen,
            f"Final Score: {game.score}",
            font_med,
            WHITE,
            (WINDOW_W // 2, WINDOW_H // 2 - 10),
        )

        draw_text(
            screen,
            "Press R to Restart  |  Press ESC to Quit",
            font_small,
            GRAY,
            (WINDOW_W // 2, WINDOW_H // 2 + 40),
        )

    running = True
    while running:
        dt_ms = clock.tick(60)  # render at up to 60 FPS; movement paced by move_interval_ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game.alive:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        game.set_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game.set_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        game.set_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game.set_direction(RIGHT)
                else:
                    if event.key == pygame.K_r:
                        game.reset()

        # Update
        game.step(dt_ms)

        # Draw
        draw_play()
        if not game.alive:
            draw_game_over()

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    # Basic sanity check: ensure grid aligns
    if WINDOW_W % CELL != 0 or WINDOW_H % CELL != 0:
        print("Error: WINDOW_W and WINDOW_H must be divisible by CELL for a clean grid.")
        sys.exit(1)
    main()
