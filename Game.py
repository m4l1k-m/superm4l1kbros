import pygame
import sys
import random

pygame.init()

# ================= SETUP =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super M4l1k Bros.")
clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arialblack", 52)
FONT = pygame.font.SysFont("arialblack", 22)

# ================= COLORS =================
SKY_TOP = (80, 160, 255)
SKY_BOTTOM = (210, 235, 255)
GRASS = (70, 200, 90)
DIRT = (110, 75, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ================= PLAYER =================
player = pygame.Rect(100, 420, 38, 52)
vel_x = 0
vel_y = 0
SPEED = 5
GRAVITY = 0.8
JUMP = -15

on_ground = False
facing = 1
fire_power = False
fire_cooldown = 0

# ================= CAMERA =================
camera_x = 0
LEVEL_END = 4200

# ================= PLATFORMS =================
platforms = []

# Solid ground base
for x in range(0, LEVEL_END, 140):
    platforms.append(pygame.Rect(x, 540, 140, 60))

# HARD precision platforms (skill-based, tested)
platforms += [
    pygame.Rect(300, 460, 100, 16),
    pygame.Rect(480, 390, 90, 16),
    pygame.Rect(650, 330, 80, 16),
    pygame.Rect(820, 380, 80, 16),
    pygame.Rect(1000, 300, 80, 16),
    pygame.Rect(1180, 420, 90, 16),
    pygame.Rect(1360, 350, 70, 16),
    pygame.Rect(1540, 290, 70, 16),
    pygame.Rect(1720, 420, 80, 16),
    pygame.Rect(1900, 360, 90, 16),
    pygame.Rect(2150, 300, 80, 16),
    pygame.Rect(2350, 420, 90, 16),
    pygame.Rect(2550, 350, 80, 16),
    pygame.Rect(2800, 290, 70, 16),
    pygame.Rect(3000, 420, 100, 16),
    pygame.Rect(3250, 360, 80, 16),
    pygame.Rect(3500, 300, 80, 16),
]

# ================= PLAYER POWERUPS =================
shield = False
shield_cooldown = 0
speed_boost = False
speed_boost_time = 0
double_jump = False
double_jump_used = False

# ================= ENEMIES =================
enemies = [
    {"rect": pygame.Rect(700, 500, 38, 38), "dir": 1},
    {"rect": pygame.Rect(1500, 500, 38, 38), "dir": -1},
    {"rect": pygame.Rect(2300, 500, 38, 38), "dir": 1},
    {"rect": pygame.Rect(3100, 500, 38, 38), "dir": -1},
]

# ================= SPIKES =================
spikes = [
    {"rect": pygame.Rect(400, 520, 30, 20)},
    {"rect": pygame.Rect(900, 520, 30, 20)},
    {"rect": pygame.Rect(1400, 520, 30, 20)},
    {"rect": pygame.Rect(1850, 520, 30, 20)},
    {"rect": pygame.Rect(2600, 520, 30, 20)},
    {"rect": pygame.Rect(3200, 520, 30, 20)},
]

# ================= MOVING PLATFORMS =================
moving_platforms = [
    {"rect": pygame.Rect(1200, 450, 80, 16), "start_y": 450, "end_y": 350, "speed": 2, "pos": 0},
    {"rect": pygame.Rect(2000, 420, 80, 16), "start_y": 420, "end_y": 280, "speed": 2.5, "pos": 0},
    {"rect": pygame.Rect(2700, 380, 80, 16), "start_y": 380, "end_y": 250, "speed": 1.5, "pos": 0},
]

# ================= LUCKY BLOCKS =================
lucky_blocks = [
    {"rect": pygame.Rect(480, 340, 40, 40), "used": False},
    {"rect": pygame.Rect(700, 410, 40, 40), "used": False},
    {"rect": pygame.Rect(1000, 240, 40, 40), "used": False},
    {"rect": pygame.Rect(1350, 290, 40, 40), "used": False},
    {"rect": pygame.Rect(1650, 380, 40, 40), "used": False},
    {"rect": pygame.Rect(1900, 300, 40, 40), "used": False},
    {"rect": pygame.Rect(2250, 350, 40, 40), "used": False},
    {"rect": pygame.Rect(2550, 280, 40, 40), "used": False},
    {"rect": pygame.Rect(2800, 240, 40, 40), "used": False},
    {"rect": pygame.Rect(3100, 350, 40, 40), "used": False},
    {"rect": pygame.Rect(3400, 260, 40, 40), "used": False},
]

# ================= FIREBALLS =================
fireballs = []

# ================= FLAGPOLE =================
flag_pole = pygame.Rect(3950, 260, 8, 280)
flag_rect = pygame.Rect(3958, 260, 32, 22)

state = "menu"

# ================= FUNCTIONS =================
def reset_game():
    global vel_x, vel_y, fire_power, state, shield, speed_boost, double_jump, shield_cooldown, speed_boost_time, double_jump_used
    player.x, player.y = 100, 420
    vel_x = vel_y = 0
    fire_power = False
    shield = False
    speed_boost = False
    double_jump = False
    shield_cooldown = 0
    speed_boost_time = 0
    double_jump_used = False
    fireballs.clear()
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
    # 3D effect with shading
    pygame.draw.rect(screen, (80, 50, 20), (p.x - camera_x, p.y + 4, p.width, p.height - 4))
    pygame.draw.rect(screen, DIRT, (p.x - camera_x, p.y, p.width, p.height - 4))
    pygame.draw.rect(screen, GRASS, (p.x - camera_x, p.y, p.width, 8))
    # Border for definition
    pygame.draw.rect(screen, (50, 140, 50), (p.x - camera_x, p.y, p.width, 12), 1)

def draw_player():
    r = pygame.Rect(player.x - camera_x, player.y, player.width, player.height)
    color = (255, 140, 60) if fire_power else (60, 140, 255)
    # Body
    pygame.draw.rect(screen, color, r, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0) if fire_power else (40, 100, 200), r, 2, border_radius=8)
    # Eyes
    eye_y = r.y + 12
    eye_x = r.centerx + (6 * facing)
    pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 4)
    pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 2)
    # Hat/Fire power indicator
    if fire_power:
        pygame.draw.polygon(screen, (255, 200, 0), [(r.x + 5, r.y + 2), (r.x + 20, r.y - 5), (r.x + 33, r.y + 2)])
    else:
        pygame.draw.rect(screen, (100, 100, 100), (r.x + 5, r.y - 4, 28, 6))
    # Shield indicator
    if shield:
        pygame.draw.circle(screen, (0, 200, 255), r.center, 35, 2)
    # Speed boost indicator
    if speed_boost:
        for i in range(3):
            pygame.draw.line(screen, (255, 255, 0), (r.x - 5 - i*3, r.centery), (r.x - i*3, r.centery), 1)

def draw_enemy(e):
    r = pygame.Rect(e["rect"].x - camera_x, e["rect"].y, 38, 38)
    # Body with gradient effect
    pygame.draw.rect(screen, (220, 40, 40), r, border_radius=6)
    pygame.draw.rect(screen, (255, 100, 100), r, 2, border_radius=6)
    # Eyes
    eye_y = r.y + 10
    eye_left = r.x + 8
    eye_right = r.x + 22
    pygame.draw.circle(screen, WHITE, (eye_left, eye_y), 4)
    pygame.draw.circle(screen, WHITE, (eye_right, eye_y), 4)
    pygame.draw.circle(screen, BLACK, (eye_left, eye_y), 2)
    pygame.draw.circle(screen, BLACK, (eye_right, eye_y), 2)
    # Mouth
    pygame.draw.line(screen, (255, 150, 150), (r.x + 10, r.y + 24), (r.x + 28, r.y + 24), 2)

def draw_lucky(b):
    r = pygame.Rect(b["rect"].x - camera_x, b["rect"].y, 40, 40)
    base = (230, 200, 60) if not b["used"] else (160, 160, 160)
    pygame.draw.rect(screen, base, r, border_radius=4)
    pygame.draw.rect(screen, BLACK, r, 3, border_radius=4)
    if not b["used"]:
        # Question mark
        q = FONT.render("?", True, BLACK)
        screen.blit(q, (r.centerx - q.get_width()//2,
                         r.centery - q.get_height()//2))
        # Glow effect
        pygame.draw.rect(screen, (255, 255, 150), r, 1, border_radius=4)
    else:
        # Used block effect
        pygame.draw.line(screen, (100, 100, 100), r.topleft, r.bottomright, 2)
        pygame.draw.line(screen, (100, 100, 100), r.topright, r.bottomleft, 2)

def draw_spikes(spike):
    r = pygame.Rect(spike["rect"].x - camera_x, spike["rect"].y, spike["rect"].width, spike["rect"].height)
    # Draw spike triangle
    points = [
        (r.x + r.width // 2, r.y - 5),  # Top point
        (r.x, r.y + r.height),           # Bottom left
        (r.x + r.width, r.y + r.height)  # Bottom right
    ]
    pygame.draw.polygon(screen, (150, 0, 0), points)
    pygame.draw.polygon(screen, (255, 80, 80), points, 1)

def draw_moving_platform(p):
    rect = pygame.Rect(p["rect"].x - camera_x, p["rect"].y, p["rect"].width, p["rect"].height)
    # Animated platform with color pulse
    pulse = int(100 + 55 * abs(pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 100).x))
    pygame.draw.rect(screen, (100, pulse, 100), rect, border_radius=4)
    pygame.draw.rect(screen, (50, 200, 50), rect, 2, border_radius=4)

# ================= MAIN LOOP =================
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # ===== MENU =====
    if state == "menu":
        draw_sky()
        title = FONT_BIG.render("Super M4l1k Bros.", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        hint = FONT.render("Press SPACE to Start", True, BLACK)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 280))
        if keys[pygame.K_SPACE]:
            reset_game()
        pygame.display.flip()
        continue

    # ===== INPUT =====
    vel_x = 0
    current_speed = SPEED * 1.5 if speed_boost else SPEED
    if keys[pygame.K_a]:
        vel_x = -current_speed
        facing = -1
    if keys[pygame.K_d]:
        vel_x = current_speed
        facing = 1
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = JUMP
    # Double jump ability
    if keys[pygame.K_SPACE] and not on_ground and double_jump and not double_jump_used:
        vel_y = JUMP - 2
        double_jump_used = True

    if keys[pygame.K_f] and fire_power and fire_cooldown == 0:
        fireballs.append({"rect": pygame.Rect(player.centerx, player.centery, 10, 10), "dir": facing})
        fire_cooldown = 20

    fire_cooldown = max(0, fire_cooldown - 1)

    # ===== MOVEMENT =====
    player.x += vel_x
    for p in platforms:
        if player.colliderect(p):
            if vel_x > 0:
                player.right = p.left
            elif vel_x < 0:
                player.left = p.right
    for p in moving_platforms:
        if player.colliderect(p["rect"]):
            if vel_x > 0:
                player.right = p["rect"].left
            elif vel_x < 0:
                player.left = p["rect"].right

    vel_y += GRAVITY
    player.y += vel_y
    on_ground = False

    for p in platforms:
        if player.colliderect(p):
            if vel_y > 0:
                player.bottom = p.top
                vel_y = 0
                on_ground = True
                double_jump_used = False
            elif vel_y < 0:
                player.top = p.bottom
                vel_y = 0
    
    # Moving platforms collision
    for p in moving_platforms:
        if player.colliderect(p["rect"]):
            if vel_y > 0:
                player.bottom = p["rect"].top
                vel_y = 0
                on_ground = True
                double_jump_used = False
            elif vel_y < 0:
                player.top = p["rect"].bottom
                vel_y = 0

    # ===== LUCKY BLOCKS =====
    for b in lucky_blocks:
        if player.colliderect(b["rect"]) and vel_y < 0 and not b["used"]:
            player.top = b["rect"].bottom
            vel_y = 0
            b["used"] = True
            reward = random.choice(["fire", "bounce", "enemy", "shield", "speed", "double_jump"])
            if reward == "fire":
                fire_power = True
            elif reward == "bounce":
                vel_y = -18
            elif reward == "enemy":
                enemies.append({"rect": pygame.Rect(b["rect"].x, 500, 38, 38), "dir": 1})
            elif reward == "shield":
                shield = True
                shield_cooldown = 300  # 5 seconds at 60 FPS
            elif reward == "speed":
                speed_boost = True
                speed_boost_time = 180  # 3 seconds at 60 FPS
            elif reward == "double_jump":
                double_jump = True
                double_jump_used = False

    # ===== ENEMIES =====
    for e in enemies[:]:
        e["rect"].x += e["dir"] * 2
        # Keep enemies on ground
        e["rect"].y = 500
        # Make them patrol back and forth
        if e["rect"].x < 0 or e["rect"].x > LEVEL_END:
            e["dir"] *= -1
        if player.colliderect(e["rect"]):
            if vel_y > 0 and player.centery < e["rect"].centery:
                enemies.remove(e)
                vel_y = -10
            elif not shield:
                state = "menu"
            elif shield:
                enemies.remove(e)
                shield = False

    # ===== SPIKES =====
    for spike in spikes:
        if player.colliderect(spike["rect"]):
            if not shield:
                state = "menu"
            else:
                shield = False

    # ===== MOVING PLATFORMS UPDATE =====
    for p in moving_platforms:
        p["pos"] += p["speed"]
        if p["pos"] > 100:
            p["pos"] = 0
        progress = p["pos"] / 100
        p["rect"].y = p["start_y"] + (p["end_y"] - p["start_y"]) * (abs(pygame.math.Vector2(1, 0).rotate(progress * 360).x))

    # ===== POWERUP TIMERS =====
    if speed_boost_time > 0:
        speed_boost_time -= 1
        if speed_boost_time == 0:
            speed_boost = False
    
    if shield_cooldown > 0:
        shield_cooldown -= 1
        if shield_cooldown == 0:
            shield = False

    # ===== FIREBALLS =====
    for f in fireballs[:]:
        f["rect"].x += f["dir"] * 8
        if abs(f["rect"].x - player.x) > WIDTH:
            fireballs.remove(f)
        for e in enemies[:]:
            if f["rect"].colliderect(e["rect"]):
                enemies.remove(e)
                fireballs.remove(f)

    # ===== FLAG =====
    if player.colliderect(flag_pole):
        state = "menu"

    if player.y > HEIGHT + 200:
        state = "menu"

    camera_x = max(0, player.centerx - WIDTH // 2)

    # ===== DRAW =====
    draw_sky()
    for p in platforms:
        draw_platform(p)
    for p in moving_platforms:
        draw_moving_platform(p)
    for spike in spikes:
        draw_spikes(spike)
    for b in lucky_blocks:
        draw_lucky(b)
    for e in enemies:
        draw_enemy(e)
    for f in fireballs:
        pygame.draw.circle(screen, (255, 140, 60),
                           (f["rect"].x - camera_x, f["rect"].y), 6)
        pygame.draw.circle(screen, (255, 200, 100),
                           (f["rect"].x - camera_x, f["rect"].y), 4)

    # Flagpole with flag animation
    pygame.draw.rect(screen, (139, 69, 19),
                     (flag_pole.x - camera_x, flag_pole.y, flag_pole.width, flag_pole.height))
    # Animated flag
    flag_wave = 3 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 10).x
    flag_points = [
        (flag_rect.x - camera_x, flag_rect.y),
        (flag_rect.x + flag_rect.width + flag_wave - camera_x, flag_rect.y + 5),
        (flag_rect.x - camera_x, flag_rect.y + flag_rect.height)
    ]
    pygame.draw.polygon(screen, (255, 50, 50), flag_points)

    draw_player()
    pygame.display.flip()
