#!/usr/bin/env python3
"""
Frogger - Python Edition
Requiere: pip install pygame
Controles: Flechas o WASD | ESC salir | R reiniciar
"""

try:
    import pygame
except ImportError:
    print("=" * 50)
    print("ERROR: pygame no está instalado.")
    print("Ejecuta:   pip install pygame")
    print("=" * 50)
    input("Pulsa Enter para cerrar...")
    raise SystemExit

import sys
import random

SCREEN_W = 480
SCREEN_H = 560
CELL     = 40
ROWS     = SCREEN_H // CELL
COLS     = SCREEN_W // CELL
FPS      = 60

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (34,  139,  34)
DARK_GREEN = (0,   100,   0)
ROAD_GRAY  = (80,   80,  80)
WATER_BLUE = (30,  144, 255)
LOG_BROWN  = (139,  90,  43)
FROG_GREEN = (50,  205,  50)
YELLOW     = (255, 215,   0)
GRAY       = (120, 120, 120)
GOLD       = (255, 215,   0)
RED        = (220,  50,  50)

ROW_RIVER_START = 1
ROW_RIVER_END   = 5
ROW_ROAD_START  = 7
ROW_ROAD_END    = 11
ROW_START       = 12
ROW_GOAL        = 0

BASE_SPEED    = 0.6
INITIAL_LIVES = 50
GOAL_BONUS    = 100
TIME_LIMIT    = 45 * FPS


class Log(pygame.sprite.Sprite):
    def __init__(self, row, x, width, speed):
        super().__init__()
        self.image = pygame.Surface((width, CELL - 4))
        self.image.fill(LOG_BROWN)
        pygame.draw.rect(self.image, (100, 60, 20), (0, 0, width, CELL - 4), 3)
        for vy in range(8, CELL - 10, 8):
            pygame.draw.line(self.image, (160, 100, 50), (4, vy), (width - 4, vy), 1)
        self.rect  = self.image.get_rect(x=x, y=row * CELL + 2)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_W:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_W


class Car(pygame.sprite.Sprite):
    def __init__(self, row, x, width, speed, color):
        super().__init__()
        self.image = pygame.Surface((width, CELL - 6))
        self.image.fill(color)
        wc = (180, 230, 255)
        pygame.draw.rect(self.image, wc, (5, 4, min(14, width // 3), CELL - 16))
        if width > 60:
            pygame.draw.rect(self.image, wc, (width - 22, 4, 14, CELL - 16))
        self.rect  = self.image.get_rect(x=x, y=row * CELL + 3)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_W:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_W


class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL - 4, CELL - 4), pygame.SRCALPHA)
        self._draw()
        self.rect   = self.image.get_rect()
        self.on_log = None
        self.reset()

    def _draw(self):
        img = self.image
        img.fill((0, 0, 0, 0))
        pygame.draw.ellipse(img, FROG_GREEN, (4, 6, CELL - 12, CELL - 16))
        for ex in (8, CELL - 16):
            pygame.draw.circle(img, WHITE, (ex, 7), 4)
            pygame.draw.circle(img, BLACK, (ex, 7), 2)
        pygame.draw.line(img, FROG_GREEN, (4, CELL - 14), (0, CELL - 6), 3)
        pygame.draw.line(img, FROG_GREEN, (CELL - 12, CELL - 14), (CELL - 4, CELL - 6), 3)
        pygame.draw.arc(img, (0, 150, 0), (10, 14, CELL - 24, 8), 3.14, 0, 2)

    def reset(self):
        self.col    = COLS // 2
        self.row    = ROW_START
        self.on_log = None
        self.rect.x = self.col * CELL + 2
        self.rect.y = self.row * CELL + 2

    def move(self, dcol, drow):
        nc, nr = self.col + dcol, self.row + drow
        if 0 <= nc < COLS and 0 <= nr <= ROW_START:
            self.col, self.row = nc, nr
            self.rect.x = self.col * CELL + 2
            self.rect.y = self.row * CELL + 2
            self.on_log = None

    def update(self):
        if self.on_log:
            self.rect.x += self.on_log.speed
            self.col = self.rect.x // CELL


class Game:
    def __init__(self):
        pygame.init()
        self.screen     = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Frogger - Python Edition")
        self.clock      = pygame.time.Clock()
        self.font_big   = pygame.font.SysFont("Arial", 34, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)
        self.goal_flash_timer = 0
        self.reset_game()

    def reset_game(self):
        self.score            = 0
        self.lives            = INITIAL_LIVES
        self.level            = 1
        self.timer            = TIME_LIMIT
        self.goal_flash_timer = 0
        self._build_level()

    def _build_level(self):
        spd       = BASE_SPEED + (self.level - 1) * 0.08
        self.logs = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.frog = Frog()

        for row, v, w, n in [
            (1, +spd * 1.0, 140, 2),
            (2, -spd * 1.2,  90, 3),
            (3, +spd * 0.8, 180, 2),
            (4, -spd * 1.1, 110, 2),
            (5, +spd * 1.3, 100, 2),
        ]:
            sp = SCREEN_W // n
            for i in range(n):
                self.logs.add(Log(row, i * sp + random.randint(10, max(11, sp // 4)), w, v))

        for row, v, w, n, c in [
            (7,  -spd * 1.0, 55, 2, (220,  50,  50)),
            (8,  +spd * 1.2, 45, 2, (255, 215,   0)),
            (9,  -spd * 0.9, 70, 2, (220, 220, 220)),
            (10, +spd * 1.3, 50, 2, (100, 149, 237)),
            (11, -spd * 1.1, 60, 2, (255, 165,   0)),
        ]:
            sp = SCREEN_W // n
            for i in range(n):
                self.cars.add(Car(row, i * sp + random.randint(10, max(11, sp // 4)), w, v, c))

    def _draw_bg(self):
        self.screen.fill(BLACK)
        for row in range(ROWS):
            y = row * CELL
            if row == ROW_GOAL:
                color = (40, 220, 90) if self.goal_flash_timer > 0 else (0, 180, 60)
                pygame.draw.rect(self.screen, color, (0, y, SCREEN_W, CELL))
                for lx in range(-CELL, SCREEN_W, 20):
                    pygame.draw.line(self.screen, GOLD, (lx, y), (lx + CELL, y + CELL), 3)
                txt = self.font_med.render("*** META ***", True, BLACK)
                self.screen.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2,
                                       y + CELL // 2 - txt.get_height() // 2))
            elif ROW_RIVER_START <= row <= ROW_RIVER_END:
                pygame.draw.rect(self.screen, WATER_BLUE, (0, y, SCREEN_W, CELL))
                for wx in range(0, SCREEN_W, 22):
                    pygame.draw.arc(self.screen, (20, 100, 200),
                                    (wx, y + CELL // 2, 18, 7), 0, 3.14, 2)
            elif row in (6, ROW_START):
                pygame.draw.rect(self.screen, GREEN, (0, y, SCREEN_W, CELL))
                for gx in range(0, SCREEN_W, 10):
                    pygame.draw.line(self.screen, DARK_GREEN,
                                     (gx, y + 2), (gx + 5, y + CELL - 4), 1)
            elif ROW_ROAD_START <= row <= ROW_ROAD_END:
                pygame.draw.rect(self.screen, ROAD_GRAY, (0, y, SCREEN_W, CELL))
                if row < ROW_ROAD_END:
                    for lx in range(0, SCREEN_W, 30):
                        pygame.draw.rect(self.screen, YELLOW, (lx, y + CELL - 3, 16, 3))

    def _draw_hud(self):
        pygame.draw.rect(self.screen, (20, 20, 20), (0, SCREEN_H - CELL, SCREEN_W, CELL))
        secs    = max(0, self.timer // FPS)
        t_color = (255, 80, 80) if secs < 10 else WHITE
        self.screen.blit(self.font_med.render(f"Pts:{self.score}",   True, WHITE),      (4,   SCREEN_H - 32))
        self.screen.blit(self.font_med.render(f"Vidas:{self.lives}", True, FROG_GREEN), (130, SCREEN_H - 32))
        self.screen.blit(self.font_med.render(f"Niv:{self.level}",   True, GOLD),       (295, SCREEN_H - 32))
        self.screen.blit(self.font_med.render(f"{secs:02d}s",        True, t_color),    (415, SCREEN_H - 32))
        if self.goal_flash_timer > 0:
            bonus = self.font_small.render(f"+{GOAL_BONUS} META!", True, GOLD)
            self.screen.blit(bonus, (SCREEN_W // 2 - bonus.get_width() // 2, SCREEN_H - 58))

    def _check_status(self):
        frog = self.frog
        if frog.row == ROW_GOAL:
            return "goal"
        if ROW_RIVER_START <= frog.row <= ROW_RIVER_END:
            on_log = next((lg for lg in self.logs if lg.rect.colliderect(frog.rect)), None)
            if on_log:
                frog.on_log = on_log
            else:
                return "dead"
        if ROW_ROAD_START <= frog.row <= ROW_ROAD_END:
            if any(c.rect.colliderect(frog.rect) for c in self.cars):
                return "dead"
        if frog.rect.right < 0 or frog.rect.left > SCREEN_W:
            return "dead"
        return "ok"

    def _on_die(self):
        self.lives -= 1
        if self.lives <= 0:
            self._show_game_over()
        else:
            self.frog.reset()
            self.timer            = TIME_LIMIT
            self.goal_flash_timer = 0

    def _on_goal(self):
        bonus       = GOAL_BONUS + (self.timer // FPS)
        self.score += bonus
        self.goal_flash_timer = FPS
        self.frog.reset()
        self.timer = TIME_LIMIT
        if self.score % 500 < bonus:
            self.level += 1
            self._build_level()

    def _overlay(self):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        self.screen.blit(ov, (0, 0))

    def _blit_center(self, font, text, color, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, y))

    def _show_game_over(self):
        self._overlay()
        self._blit_center(self.font_big,   "GAME OVER",             RED,   170)
        self._blit_center(self.font_med,   f"Puntos: {self.score}", WHITE, 240)
        self._blit_center(self.font_small, "R = reiniciar",         GRAY,  295)
        self._blit_center(self.font_small, "ESC = salir",           GRAY,  322)
        pygame.display.flip()
        self._wait_key({pygame.K_r:      self.reset_game,
                        pygame.K_ESCAPE: lambda: (pygame.quit(), sys.exit())})

    def _wait_key(self, key_map):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key in key_map:
                    key_map[event.key]()
                    return

    def run(self):
        MOVE_DELAY = 150
        last_move  = 0
        while True:
            self.clock.tick(FPS)
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            keys = pygame.key.get_pressed()
            if now - last_move > MOVE_DELAY:
                moved = False
                if   keys[pygame.K_UP]    or keys[pygame.K_w]: self.frog.move(0, -1); moved = True
                elif keys[pygame.K_DOWN]  or keys[pygame.K_s]: self.frog.move(0, +1); moved = True
                elif keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.frog.move(-1, 0); moved = True
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.frog.move(+1, 0); moved = True
                if moved:
                    last_move = now
            self.logs.update()
            self.cars.update()
            self.frog.update()
            if self.goal_flash_timer > 0:
                self.goal_flash_timer -= 1
            self.timer -= 1
            if self.timer <= 0:
                self._on_die()
            status = self._check_status()
            if status == "dead":
                self._on_die()
            elif status == "goal":
                self._on_goal()
            self._draw_bg()
            self.logs.draw(self.screen)
            self.cars.draw(self.screen)
            self.screen.blit(self.frog.image, self.frog.rect)
            self._draw_hud()
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()