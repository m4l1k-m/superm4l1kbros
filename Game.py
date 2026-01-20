import pygame
import sys
import random

pygame.init()

# ================== SETUP ==================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Malik's Mario Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)

# ================== COLORS ==================
SKY_TOP = (90, 170, 255)
SKY_BOTTOM = (170, 220, 255)
GRASS = (60, 200, 80)
DIRT = (120, 85, 50)

# ================== PLAYER ==================
player = pygame.Rect(100, 400, 40, 55)
vel_x = 0
vel_y = 0
SPEED = 5
GRAVITY = 0.7
JUMP = -15
on_ground = False

camera_x = 0
LEVEL_END = 4200

# ================== PLATFORMS ==================
platforms = []
for x in range(0, LEVEL_END, 200):
    platforms.append(pygame.Rect(x, 540, 200, 60))

platforms += [
    pygame.Rect(500, 430, 120, 20),
    pygame.Rect(800, 360, 120, 20),
    pygame.Rect(1200, 420, 120, 20),
    pygame.Rect(1600, 330, 120, 20),
    pygame.Rect(2000, 280, 120, 20),
    pygame.Rect(2400, 420, 120, 20),
    pygame.Rect(2800, 360, 120, 20),
    pygame.Rect(3200, 300, 120, 20),
]

# ================== ENEMIES ==================
enemies = [
    {"rect": pygame.Rect(700, 500, 40, 40), "speed": 2},
    {"rect": pygame.Rect(1500, 500, 40, 40), "speed": -2},
    {"rect": pygame.Rect(2600, 500, 40, 40), "speed": 2},
]

# ================== LUCKY BLOCKS ==================
lucky_blocks = [
    {"rect": pygame.Rect(550, 390, 40, 40), "used": False},
    {"rect": pygame.Rect(1250, 310, 40, 40), "used": False},
    {"rect": pygame.Rect(2150, 260, 40, 40), "used": False},
]

# ================== FLAG ==================
flag = pygame.Rect(3900, 480, 30, 60)

state = "menu"

# ================== FUNCTIONS ==================
def reset_game():
    global state, vel_x, vel_y
    player.x, player.y = 100, 400
    vel_x = vel_y = 0

    enemies.clear()
    enemies.extend([
        {"rect": pygame.Rect(700, 500, 40, 40), "speed": 2},
        {"rect": pygame.Rect(1500, 500, 40, 40), "speed": -2},
        {"rect": pygame.Rect(2600, 500, 40, 40), "speed": 2},
    ])

    for b in lucky_blocks:
        b["used"] = False

    state = "game"

def draw_sky():
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_platform(p):
    pygame.draw.rect(screen, DIRT, (p.x - camera_x, p.y, p.width, p.height))
    pygame.draw.rect(screen, GRASS, (p.x - camera_x, p.y, p.width, 12))

def draw_player():
    r = pygame.Rect(player.x - camera_x, player.y, player.width, player.height)
    pygame.draw.rect(screen, (60, 120, 255), r, border_radius=8)
    pygame.draw.circle(screen, (255, 255, 255), (r.x + 12, r.y + 18), 4)
    pygame.draw.circle(screen, (255, 255, 255), (r.x + 28, r.y + 18), 4)

def draw_enemy(e):
    r = pygame.Rect(e["rect"].x - camera_x, e["rect"].y, 40, 40)
    pygame.draw.rect(screen, (220, 60, 60), r, border_radius=6)
    pygame.draw.circle(screen, (0, 0, 0), (r.x + 12, r.y + 15), 4)
    pygame.draw.circle(screen, (0, 0, 0), (r.x + 28, r.y + 15), 4)

def draw_lucky(b):
    r = pygame.Rect(b["rect"].x - camera_x, b["rect"].y, 40, 40)
    color = (220, 200, 60) if not b["used"] else (160, 160, 160)
    pygame.draw.rect(screen, color, r)
    pygame.draw.rect(screen, (0, 0, 0), r, 2)

def center_text(text, y):
    t = font.render(text, True, (255, 255, 255))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

# ================== MAIN LOOP ==================
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if state == "menu":
        screen.fill((30, 30, 30))
        center_text("Super Malik Bros.", 220)
        center_text("Press SPACE to Start", 300)
        if keys[pygame.K_SPACE]:
            reset_game()
        pygame.display.flip()
        continue

    if state == "win":
        screen.fill((20, 20, 20))
        center_text("YOU WIN!", 220)
        center_text("Press R for New Game", 300)
        if keys[pygame.K_r]:
            reset_game()
        pygame.display.flip()
        continue

    if state == "lose":
        screen.fill((20, 20, 20))
        center_text("GAME OVER", 220)
        center_text("Press R to Retry", 300)
        if keys[pygame.K_r]:
            reset_game()
        pygame.display.flip()
        continue

    # ========== GAME LOGIC ==========
    vel_x = 0
    if keys[pygame.K_a]:
        vel_x = -SPEED
    if keys[pygame.K_d]:
        vel_x = SPEED
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = JUMP

    player.x += vel_x
    vel_y += GRAVITY
    player.y += vel_y

    on_ground = False
    for p in platforms:
        if player.colliderect(p):
            if vel_y > 0:
                player.bottom = p.top
                vel_y = 0
                on_ground = True
            elif vel_y < 0:
                player.top = p.bottom
                vel_y = 0

    # Lucky blocks
    for b in lucky_blocks:
        if player.colliderect(b["rect"]) and vel_y < 0 and not b["used"]:
            player.top = b["rect"].bottom
            vel_y = 0
            b["used"] = True

            roll = random.randint(1, 3)
            if roll == 1:
                vel_y = -22
            elif roll == 2:
                enemies.append({
                    "rect": pygame.Rect(b["rect"].x, b["rect"].y - 40, 40, 40),
                    "speed": random.choice([-2, 2])
                })

    # Enemies
    for e in enemies[:]:
        e["rect"].x += e["speed"]
        if random.random() < 0.01:
            e["speed"] *= -1

        if player.colliderect(e["rect"]):
            if vel_y > 0:
                enemies.remove(e)
                vel_y = -10
            else:
                state = "lose"

    if player.y > HEIGHT + 200:
        state = "lose"

    if player.colliderect(flag):
        state = "win"

    camera_x = max(0, player.centerx - WIDTH // 2)

    # ========== DRAW ==========
    draw_sky()

    for p in platforms:
        draw_platform(p)

    for b in lucky_blocks:
        draw_lucky(b)

    for e in enemies:
        draw_enemy(e)

    pygame.draw.rect(screen, (255, 255, 0),
                     (flag.x - camera_x, flag.y, flag.width, flag.height))

    draw_player()
    pygame.display.flip()
