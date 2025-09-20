import pygame
import math
import random

def rechthoek(surface, x=100, y=100, width=80, height=40, color=(255, 255, 255), rotation=0):
    """Draw a rectangle with position, color, and rotation.

    Args:
        surface: pygame surface to draw on
        x, y: center position of rectangle
        width, height: rectangle dimensions
        color: RGB color tuple
        rotation: rotation angle in degrees
    """
    if rotation == 0:
        rect = pygame.Rect(x - width//2, y - height//2, width, height)
        pygame.draw.rect(surface, color, rect)
    else:
        points = []
        half_w, half_h = width // 2, height // 2
        corners = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]

        rad = math.radians(rotation)
        cos_r, sin_r = math.cos(rad), math.sin(rad)

        for cx, cy in corners:
            rotated_x = cx * cos_r - cy * sin_r + x
            rotated_y = cx * sin_r + cy * cos_r + y
            points.append((rotated_x, rotated_y))

        pygame.draw.polygon(surface, color, points)

class Particle:
    def __init__(self, screen_width, screen_height):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.width = random.randint(8, 20)
        self.height = random.randint(8, 20)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed

        if self.x < 0 or self.x > self.screen_width:
            self.vx *= -1
        if self.y < 0 or self.y > self.screen_height:
            self.vy *= -1

        self.x = max(0, min(self.screen_width, self.x))
        self.y = max(0, min(self.screen_height, self.y))

    def draw(self, surface):
        rechthoek(surface, self.x, self.y, self.width, self.height, self.color, self.rotation)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Particle System with 100 Rectangles")
    clock = pygame.time.Clock()

    particles = [Particle(800, 600) for _ in range(100)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 30))

        for particle in particles:
            particle.update()
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()