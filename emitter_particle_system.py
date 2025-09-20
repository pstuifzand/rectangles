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
    def __init__(self, x, y, vx, vy, width, height, color, ttl):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-3, 3)
        self.color = color
        self.ttl = ttl
        self.max_ttl = ttl

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        self.ttl -= 1

        alpha = max(0, self.ttl / self.max_ttl)
        self.color = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )

    def is_dead(self):
        return self.ttl <= 0

    def draw(self, surface):
        rechthoek(surface, self.x, self.y, self.width, self.height, self.color, self.rotation)

class Emitter:
    def __init__(self, x, y, max_particles, emit_rate, particle_type):
        self.x = x
        self.y = y
        self.max_particles = max_particles
        self.emit_rate = emit_rate
        self.particle_type = particle_type
        self.emit_timer = 0
        self.active_particles = 0

    def can_emit(self):
        return self.active_particles < self.max_particles

    def particle_died(self):
        self.active_particles -= 1

    def particle_created(self):
        self.active_particles += 1

    def emit_particle(self):
        self.emit_timer += 1
        if self.emit_timer < self.emit_rate:
            return None

        self.emit_timer = 0

        if not self.can_emit():
            return None

        if self.particle_type == "fountain":
            vx = random.uniform(-1, 1)
            vy = random.uniform(-3, -1)
            color = (random.randint(100, 255), random.randint(100, 255), 255)
            ttl = random.randint(120, 180)
            size = random.randint(6, 12)

        elif self.particle_type == "explosion":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = (255, random.randint(100, 255), random.randint(0, 100))
            ttl = random.randint(60, 120)
            size = random.randint(8, 16)

        elif self.particle_type == "smoke":
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-1.5, -0.5)
            color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
            ttl = random.randint(180, 300)
            size = random.randint(10, 20)

        self.particle_created()
        return Particle(self.x, self.y, vx, vy, size, size, color, ttl)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Particle System with 3 Emitters")
    clock = pygame.time.Clock()

    emitters = [
        Emitter(200, 550, 50, 3, "fountain"),
        Emitter(400, 300, 30, 5, "explosion"),
        Emitter(600, 100, 40, 4, "smoke")
    ]

    particles = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 40))

        for emitter in emitters:
            new_particle = emitter.emit_particle()
            if new_particle:
                particles.append(new_particle)

        dead_particles = [p for p in particles if p.is_dead()]
        for emitter in emitters:
            for dead_particle in dead_particles:
                emitter.particle_died()

        particles = [p for p in particles if not p.is_dead()]

        for particle in particles:
            particle.update()
            particle.draw(screen)

        font = pygame.font.Font(None, 24)
        total_particles = len(particles)
        text = font.render(f"Particles: {total_particles}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        for i, emitter in enumerate(emitters):
            active = emitter.active_particles
            text = font.render(f"Emitter {i+1}: {active}/{emitter.max_particles} active", True, (255, 255, 255))
            screen.blit(text, (10, 40 + i * 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()