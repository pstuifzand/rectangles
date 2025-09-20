import pygame
import math
import random

def rechthoek(surface, x=100, y=100, width=80, height=40, color=(255, 255, 255), rotation=0, alpha=255):
    """Draw a rectangle with position, color, rotation, and transparency.

    Args:
        surface: pygame surface to draw on
        x, y: center position of rectangle
        width, height: rectangle dimensions
        color: RGB color tuple
        rotation: rotation angle in degrees
        alpha: transparency (0-255)
    """
    temp_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)

    if rotation == 0:
        rect = pygame.Rect(5, 5, width, height)
        pygame.draw.rect(temp_surface, (*color, alpha), rect)
    else:
        points = []
        half_w, half_h = width // 2, height // 2
        corners = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]

        rad = math.radians(rotation)
        cos_r, sin_r = math.cos(rad), math.sin(rad)

        for cx, cy in corners:
            rotated_x = cx * cos_r - cy * sin_r + (width + 10) // 2
            rotated_y = cx * sin_r + cy * cos_r + (height + 10) // 2
            points.append((rotated_x, rotated_y))

        pygame.draw.polygon(temp_surface, (*color, alpha), points)

    surface.blit(temp_surface, (x - (width + 10) // 2, y - (height + 10) // 2))

class Particle:
    def __init__(self, x, y, vx, vy, width, height, color, ttl, gravity=0, particle_type="normal"):
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
        self.gravity = gravity
        self.particle_type = particle_type
        self.rain_timer = random.randint(0, 60)  # Random delay before dropping rain

    def update(self, ground_y=None, ground_rects=None):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.rotation += self.rotation_speed
        self.ttl -= 1

        # Cloud particles occasionally drop rain
        new_rain_particles = []
        if self.particle_type == "cloud":
            self.rain_timer -= 1
            if self.rain_timer <= 0 and random.random() < 0.1:  # 10% chance when timer reaches 0
                # Create a rain particle below the cloud
                rain_x = self.x + random.uniform(-self.width//2, self.width//2)
                rain_y = self.y + self.height//2
                rain_particle = Particle(
                    rain_x, rain_y,
                    random.uniform(-0.5, 0.5), random.uniform(0.5, 3),
                    random.randint(3, 6), random.randint(8, 12),
                    (100, 150, 255), random.randint(200, 400),
                    random.uniform(0.05, 0.15), "rain"
                )
                new_rain_particles.append(rain_particle)
                self.rain_timer = random.randint(30, 90)  # Reset timer

        # Check for ground collision for rain particles
        if ground_y and self.gravity > 0 and self.y >= ground_y:
            self.y = ground_y
            self.vy = -abs(self.vy) * 0.3  # Bounce up with reduced velocity
            self.vx *= 0.8  # Reduce horizontal velocity
            self.ttl = min(self.ttl, 30)  # Force death soon after bouncing

            # Make ground blocks wetter when rain hits
            if ground_rects:
                for rect in ground_rects:
                    rect_left = rect['x'] - rect['width'] // 2
                    rect_right = rect['x'] + rect['width'] // 2
                    if rect_left <= self.x <= rect_right:
                        rect['wetness'] = min(rect['wetness'] + 10, 100)
                        break

        return new_rain_particles

    def get_alpha(self):
        return max(0, int(255 * (self.ttl / self.max_ttl)))

    def is_dead(self):
        return self.ttl <= 0

    def draw(self, surface):
        alpha = self.get_alpha()
        rechthoek(surface, self.x, self.y, self.width, self.height, self.color, self.rotation, alpha)

class Emitter:
    def __init__(self, x, y, max_particles, emit_rate, particle_type, ttl):
        self.x = x
        self.y = y
        self.max_particles = max_particles
        self.emit_rate = emit_rate
        self.particle_type = particle_type
        self.emit_timer = 0
        self.active_particles = 0
        self.ttl = ttl
        self.max_ttl = ttl

    def can_emit(self):
        return self.active_particles < self.max_particles and self.ttl > 0

    def particle_died(self):
        self.active_particles -= 1

    def particle_created(self):
        self.active_particles += 1

    def update(self):
        self.ttl -= 1

    def is_dead(self):
        return self.ttl <= 0

    def get_alpha(self):
        return max(0, self.ttl / self.max_ttl)

    def emit_particle(self):
        self.emit_timer += 1
        if self.emit_timer < self.emit_rate:
            return None

        self.emit_timer = 0

        if not self.can_emit():
            return None

        alpha = self.get_alpha()

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
            gravity = 0

        elif self.particle_type == "rain":
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-3, -0.5)
            color = (100, 150, 255)
            ttl = random.randint(200, 400)
            size = random.randint(3, 8)
            gravity = random.uniform(0.05, 0.15)

        elif self.particle_type == "cloud":
            vx = random.uniform(-0.3, 0.3)
            vy = random.uniform(-0.2, 0.2)
            color = (220, 220, 230)
            ttl = random.randint(300, 600)
            size = random.randint(15, 30)
            gravity = 0

        self.particle_created()
        if self.particle_type == "rain":
            return Particle(self.x, self.y, vx, vy, size, size, color, ttl, gravity, "rain")
        elif self.particle_type == "cloud":
            return Particle(self.x, self.y, vx, vy, size, size, color, ttl, gravity, "cloud")
        else:
            return Particle(self.x, self.y, vx, vy, size, size, color, ttl)

    def draw_emitter(self, surface):
        alpha = self.get_alpha()
        color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
        rechthoek(surface, self.x, self.y, 20, 20, color, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mouse-Controlled Emitter System")
    clock = pygame.time.Clock()

    emitters = []
    particles = []
    emitter_types = ["fountain", "explosion", "smoke", "rain", "cloud"]
    current_emitter_type = 0
    ground_y = 550  # Ground line 50 pixels from bottom

    # Generate fixed ground rectangles with random widths and heights
    ground_rects = []
    x = 0
    while x < 800:
        width = random.randint(4, 16)
        height = random.randint(3, 12)
        ground_rects.append({'x': x + width // 2, 'width': width, 'height': height, 'wetness': 0})
        x += width

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if emitter_types[current_emitter_type] == "cloud":
                        # Create multiple cloud particles around mouse position
                        for _ in range(random.randint(8, 15)):
                            offset_x = random.uniform(-50, 50)
                            offset_y = random.uniform(-30, 30)
                            cloud_particle = Particle(
                                mouse_x + offset_x, mouse_y + offset_y,
                                random.uniform(-0.3, 0.3), random.uniform(-0.2, 0.2),
                                random.randint(15, 30), random.randint(15, 30),
                                (220, 220, 230), random.randint(300, 600),
                                0, "cloud"
                            )
                            particles.append(cloud_particle)
                    else:
                        new_emitter = Emitter(
                            mouse_x, mouse_y,
                            random.randint(20, 40),
                            random.randint(3, 6),
                            emitter_types[current_emitter_type],
                            random.randint(300, 600)
                        )
                        emitters.append(new_emitter)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_emitter_type = (current_emitter_type + 1) % len(emitter_types)

        screen.fill((20, 20, 40))

        for emitter in emitters:
            emitter.update()
            new_particle = emitter.emit_particle()
            if new_particle:
                particles.append(new_particle)

        emitters = [e for e in emitters if not e.is_dead()]

        dead_particles = [p for p in particles if p.is_dead()]
        for emitter in emitters:
            for dead_particle in dead_particles:
                emitter.particle_died()

        particles = [p for p in particles if not p.is_dead()]

        # Draw gravelly ground with small rectangles (fixed widths and heights)
        for rect in ground_rects:
            # Calculate color based on wetness - more blue when wet
            base_gray = 80
            blue_amount = int(rect['wetness'] * 1.5)  # Scale wetness to blue
            color = (max(0, base_gray - blue_amount // 2), max(0, base_gray - blue_amount // 2), min(255, base_gray + blue_amount))
            rechthoek(screen, rect['x'], ground_y - rect['height'] // 2, rect['width'], rect['height'], color)

            # Slowly dry the ground over time
            rect['wetness'] = max(0, rect['wetness'] - 0.2)

        for particle in particles:
            new_rain = particle.update(ground_y, ground_rects)
            if new_rain:
                particles.extend(new_rain)
            particle.draw(screen)


        font = pygame.font.Font(None, 24)
        total_particles = len(particles)
        text = font.render(f"Particles: {total_particles}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        text = font.render(f"Emitters: {len(emitters)}", True, (255, 255, 255))
        screen.blit(text, (10, 35))

        text = font.render(f"Current type: {emitter_types[current_emitter_type]}", True, (255, 255, 255))
        screen.blit(text, (10, 60))

        text = font.render("Click to place emitter, SPACE to change type", True, (255, 255, 255))
        screen.blit(text, (10, 85))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()