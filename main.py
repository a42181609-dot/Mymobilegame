import asyncio
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Mobile Screen Size (Portrait Mode)
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Modern Mobile Battle Game")

# Colors
GREEN = (40, 180, 99)
WHITE = (255, 255, 255)
RED = (231, 76, 60)
DARK_GRAY = (50, 50, 50)
YELLOW = (241, 196, 15)
BLUE = (41, 128, 185)

# Player Setup
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 160
player_speed = 7
earnings = 0
player_health = 100  # Added Player Health
game_over = False    # Game state check

# Game Objects
bullets = []
enemies = []
enemy_spawn_timer = 0

# Touch Buttons Layout (For Mobile Screen)
btn_left = pygame.Rect(20, SCREEN_HEIGHT - 80, 80, 60)
btn_right = pygame.Rect(120, SCREEN_HEIGHT - 80, 80, 60)
btn_fire = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 80, 80, 60)

async def main():
    global player_x, player_y, enemy_spawn_timer, earnings, player_health, game_over
    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)  # Draw Ground

        # Event handling
        move_left = False
        move_right = False
        shoot = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Check Touch/Mouse Click
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN) and not game_over:
                pos = pygame.mouse.get_pos()
                if btn_left.collidepoint(pos):
                    move_left = True
                if btn_right.collidepoint(pos):
                    move_right = True
                if btn_fire.collidepoint(pos):
                    shoot = True

        if not game_over:
            # PC Keyboard Backups
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or move_left:
                if player_x > 20: player_x -= player_speed
            if keys[pygame.K_RIGHT] or move_right:
                if player_x < SCREEN_WIDTH - 20: player_x += player_speed
            if keys[pygame.K_SPACE] or shoot:
                bullets.append([player_x, player_y - 20])

            # Spawn Enemies
            enemy_spawn_timer += 1
            if enemy_spawn_timer > 40:
                enemies.append([random.randint(20, SCREEN_WIDTH - 20), 0])
                enemy_spawn_timer = 0

            # Move and Draw Bullets
            for b in bullets[:]:
                b[1] -= 10  # Speed of bullet
                pygame.draw.circle(screen, YELLOW, (b[0], b[1]), 5)
                if b[1] < 0:
                    bullets.remove(b)

            # Move and Draw Enemies
            for e in enemies[:]:
                e[1] += 3  # Speed of enemy
                pygame.draw.rect(screen, DARK_GRAY, (e[0] - 15, e[1] - 15, 30, 30))
                
                # Check Collision with Bullets
                for b in bullets[:]:
                    if abs(b[0] - e[0]) < 20 and abs(b[1] - e[1]) < 20:
                        if e in enemies: enemies.remove(e)
                        if b in bullets: bullets.remove(b)
                        earnings += 10  # Earn $10 on each kill
                
                # Check Collision with Player (Enemy Attacks Player)
                if abs(player_x - e[0]) < 25 and abs(player_y - e[1]) < 25:
                    player_health -= 20  # Lose 20 HP on hit
                    if e in enemies: enemies.remove(e)
                    if player_health <= 0:
                        player_health = 0
                        game_over = True
                
                # Remove if enemy goes offscreen
                if e[1] > SCREEN_HEIGHT - 100:
                    if e in enemies: enemies.remove(e)

        # Draw Player
        if not game_over:
            pygame.draw.circle(screen, RED, (player_x, player_y), 20)

        # Draw Control Panel Base
        pygame.draw.rect(screen, (30, 30, 30), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw Touch Buttons
        pygame.draw.rect(screen, BLUE, btn_left, border_radius=10)
        pygame.draw.rect(screen, BLUE, btn_right, border_radius=10)
        pygame.draw.rect(screen, RED, btn_fire, border_radius=10)

        # Button Labels
        font_btn = pygame.font.SysFont(None, 24)
        screen.blit(font_btn.render("< L", True, WHITE), (btn_left.x + 25, btn_left.y + 20))
        screen.blit(font_btn.render("R >", True, WHITE), (btn_right.x + 25, btn_right.y + 20))
        screen.blit(font_btn.render("FIRE", True, WHITE), (btn_fire.x + 20, btn_fire.y + 20))

        # Top Bar Stats Info
        font_ui = pygame.font.SysFont(None, 26)
        text_earnings = font_ui.render(f"EARNINGS: ${earnings}", True, WHITE)
        text_health = font_ui.render(f"HP: {player_health}", True, RED if player_health <= 40 else WHITE)
        screen.blit(text_earnings, (10, 10))
        screen.blit(text_health, (SCREEN_WIDTH - 80, 10))

        # Display Game Over Screen
        if game_over:
            font_go = pygame.font.SysFont(None, 48)
            text_go = font_go.render("GAME OVER!", True, RED)
            screen.blit(text_go, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())