import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)
BLUE = (0, 50, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Rolling Circle with Moving Background")

# Background properties
scroll_speed = 5

# Sprite properties
sprite_radius = 25
sprite_rect = pygame.Rect(SCREEN_WIDTH // 2 - sprite_radius, SCREEN_HEIGHT - sprite_radius * 2, sprite_radius * 2, sprite_radius * 2)
sprite_angle = 0
sprite_jump = 0
gravity = 1
jump_strength = -15
is_jumping = False
boost_strength = -20

# Item properties
item_size = 20
item_list = []
item_spawn_time = 1500
last_spawn_time = pygame.time.get_ticks()
item_speed = 5

# Ramp properties
ramp_width = 60
ramp_height = 15
ramp_list = []
ramp_spawn_time = 500
last_ramp_spawn_time = pygame.time.get_ticks()
ramp_speed = 5

# Enemy properties
enemy_radius = 20
enemy_list = []
enemy_spawn_time = 2000
last_enemy_spawn_time = pygame.time.get_ticks()
enemy_speed = 5

# Score
score = 0

# Font for score display
font = pygame.font.Font(None, 36)

# Clock for frame rate
clock = pygame.time.Clock()

def draw_background():
    screen.fill(GREEN)

def rotate_center(surface, angle):
    """Rotate a surface while keeping its center and size."""
    rotated_surface = pygame.transform.rotate(surface, angle)
    return rotated_surface

def spawn_item():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - item_size)
    return pygame.Rect(x, y, item_size, item_size)

def spawn_ramp():
    x = SCREEN_WIDTH
    y = SCREEN_HEIGHT - random.randint(ramp_height * 3, ramp_height * 20)
    return pygame.Rect(x, y, ramp_width, ramp_height)

def spawn_enemy():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - enemy_radius * 2)
    return pygame.Rect(x, y, enemy_radius * 2, enemy_radius * 2)

def reset_game():
    global score, item_list, ramp_list, enemy_list, sprite_rect, is_jumping, sprite_jump
    score = 0
    item_list = []
    ramp_list = []
    enemy_list = []
    sprite_rect.topleft = (SCREEN_WIDTH // 2 - sprite_radius, SCREEN_HEIGHT - sprite_radius * 2)
    is_jumping = False
    sprite_jump = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_jumping == False:  # Jump normally
                    sprite_jump = jump_strength
                    is_jumping = True
                else:  # Boost if on ramp
                    for ramp in ramp_list:
                        if sprite_rect.colliderect(ramp):
                            sprite_jump = boost_strength
                            break

    # Clear screen and draw background
    draw_background()

    # Rotate the sprite
    sprite_angle = (sprite_angle - 5) % 360
    rotated_circle_surface = pygame.Surface((sprite_radius * 2, sprite_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(rotated_circle_surface, BLUE, (sprite_radius, sprite_radius), sprite_radius)
    rotated_circle_surface = rotate_center(rotated_circle_surface, sprite_angle)
    screen.blit(rotated_circle_surface, sprite_rect.topleft)

    # Handle sprite jump
    if is_jumping:
        sprite_jump += gravity
        sprite_rect.y += sprite_jump
        if sprite_rect.bottom >= SCREEN_HEIGHT:
            sprite_rect.bottom = SCREEN_HEIGHT
            sprite_jump = 0
            is_jumping = False

    # Spawn items
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > item_spawn_time:
        item_list.append(spawn_item())
        last_spawn_time = current_time

    # Spawn ramps
    if current_time - last_ramp_spawn_time > ramp_spawn_time:
        ramp_list.append(spawn_ramp())
        last_ramp_spawn_time = current_time

    # Spawn enemies
    if current_time - last_enemy_spawn_time > enemy_spawn_time:
        enemy_list.append(spawn_enemy())
        last_enemy_spawn_time = current_time

    # Move items
    for item in item_list[:]:
        item.x -= item_speed
        if item.right < 0:
            item_list.remove(item)
        pygame.draw.rect(screen, GOLD, item)

    # Move ramps
    for ramp in ramp_list[:]:
        ramp.x -= ramp_speed
        if ramp.right < 0:
            ramp_list.remove(ramp)
        pygame.draw.rect(screen, BROWN, ramp)

    # Move enemies
    for enemy in enemy_list[:]:
        enemy.x -= enemy_speed
        if enemy.right < 0:
            enemy_list.remove(enemy)
        pygame.draw.circle(screen, RED, (enemy.x + enemy_radius, enemy.y + enemy_radius), enemy_radius)

    # Check for collisions with items
    for item in item_list[:]:
        if sprite_rect.colliderect(item):
            item_list.remove(item)
            score += 1

    # Check for collisions with enemies
    for enemy in enemy_list:
        if sprite_rect.colliderect(enemy):
            reset_game()

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)
