import pygame
import random
import sys
import os
from pygame import mixer
import math
import numpy as np  # Añadir esta línea al inicio


# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 20
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED = 8
BALL_COUNT = 8
BALL_SPAWN_DELAY = 1000  # Delay between ball spawns in milliseconds
PARTICLE_COUNT = 20  # Number of particles in explosion
PARTICLE_LIFETIME = 500  # How long particles last in milliseconds

# Colors
WHITE = (255, 255, 255)
BLUE1 = (0, 102, 204)
PURPLE2 = (153, 0, 204)
BAR_COLOR = (0, 255, 200)
BALL_COLOR = (255, 80, 80)



# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Lluvia de Pelotas - ¡Con Explosiones!")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.lifetime = PARTICLE_LIFETIME
        self.birth_time = pygame.time.get_ticks()

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity effect
        self.lifetime = PARTICLE_LIFETIME - (pygame.time.get_ticks() - self.birth_time)
        return self.lifetime > 0

    def draw(self):
        alpha = int(255 * (self.lifetime / PARTICLE_LIFETIME))
        color = (*self.color, alpha)
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size//2, self.size//2), self.size//2)
        screen.blit(surf, (int(self.x), int(self.y)))

# Create a simple beep sound
def create_beep_sound():
    sample_rate = 44100
    duration = 0.2  # segundos (más largo)
    frequency = 440  # Hz (nota A4)
    
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    samples = np.array(wave * 32767, dtype=np.int16)

    stereo_sound = np.column_stack((samples, samples))  # sonido estéreo
    return pygame.sndarray.make_sound(stereo_sound)

try:
    collision_sound = create_beep_sound()
    collision_sound.set_volume(1.0)  # 100% volumen
except Exception as e:
    print("No se pudo crear el efecto de sonido:", e)
    collision_sound = None


# Create and load sound effect
try:
    collision_sound = create_beep_sound()
    collision_sound.set_volume(1.0)  # Set volume to 100%
except:
    print("No se pudo crear el efecto de sonido")
    collision_sound = None

def draw_vertical_gradient(surface, top_color, bottom_color):
    """Draw a vertical gradient from top_color to bottom_color on the surface."""
    for y in range(WINDOW_HEIGHT):
        ratio = y / WINDOW_HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 50
        self.speed = PADDLE_SPEED

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BAR_COLOR, (self.x, self.y, self.width, self.height), border_radius=8)

class Ball:
    def __init__(self):
        self.size = BALL_SIZE
        self.active = False
        self.reset()

    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(BALL_SPEED, BALL_SPEED + 5)
        self.active = True

    def move(self):
        if self.active:
            self.y += self.speed
            if self.y > WINDOW_HEIGHT:
                self.active = False
                return True
        return False

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, BALL_COLOR, (self.x + self.size//2, self.y + self.size//2), self.size//2)

    def check_collision(self, paddle):
        if not self.active:
            return False
        ball_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
        return ball_rect.colliderect(paddle_rect)

def main():
    paddle = Paddle()
    balls = [Ball() for _ in range(BALL_COUNT)]
    particles = []
    score = 0
    font = pygame.font.Font(None, 36)
    last_spawn_time = pygame.time.get_ticks()
    current_ball_index = 0

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Spawn balls sequentially
        if current_time - last_spawn_time > BALL_SPAWN_DELAY:
            if current_ball_index < len(balls):
                balls[current_ball_index].reset()
                current_ball_index += 1
                last_spawn_time = current_time
            elif all(not ball.active for ball in balls):
                current_ball_index = 0
                last_spawn_time = current_time

        # Move balls and check collisions
        for ball in balls:
            if ball.move():
                score -= 1  # Penalty for missing a ball
            if ball.check_collision(paddle):
                score += 1
                ball.active = False
                # Create explosion particles
                for _ in range(PARTICLE_COUNT):
                    particles.append(Particle(
                        ball.x + ball.size//2,
                        ball.y + ball.size//2
                    ))
                # Play sound effect
                if collision_sound:
                    collision_sound.play()

        # Update and draw particles
        particles = [p for p in particles if p.update()]
        for particle in particles:
            particle.draw()

        # Draw everything
        draw_vertical_gradient(screen, BLUE1, PURPLE2)
        paddle.draw()
        for ball in balls:
            ball.draw()
        
        # Draw score
        score_text = font.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 