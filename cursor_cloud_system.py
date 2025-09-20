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

    def update(self, ground_y=None, ground_rects=None):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.rotation += self.rotation_speed
        self.ttl -= 1

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

    def get_alpha(self):
        return max(0, int(255 * (self.ttl / self.max_ttl)))

    def is_dead(self):
        return self.ttl <= 0

    def draw(self, surface):
        alpha = self.get_alpha()
        rechthoek(surface, self.x, self.y, self.width, self.height, self.color, self.rotation, alpha)

class CloudParticle:
    def __init__(self, offset_x, offset_y, cloud_particles_count=20):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.local_vx = random.uniform(-0.05, 0.05)
        self.local_vy = random.uniform(-0.05, 0.05)

        # Scale cloud particle size based on total cloud size
        base_size = 12 + (cloud_particles_count - 5) * 0.8  # Grows with cloud size
        size_variation = random.randint(-3, 8)
        self.width = max(8, int(base_size + size_variation))
        self.height = max(8, int(base_size + size_variation))

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)
        self.color = (220, 220, 230)

    def update(self, mouse_x, mouse_y, cloud_size):
        # Very gentle local movement
        self.offset_x += self.local_vx * 0.3
        self.offset_y += self.local_vy * 0.3
        self.rotation += self.rotation_speed

        # Scale bounding area based on cloud size
        max_x = 25 + (cloud_size - 5) * 1.5  # Grows from 25 to 77.5 pixels
        max_y = 15 + (cloud_size - 5) * 0.9  # Grows from 15 to 46.5 pixels

        # Keep offsets within scaled bounds
        self.offset_x = max(-max_x, min(max_x, self.offset_x))
        self.offset_y = max(-max_y, min(max_y, self.offset_y))

        # Actual position follows mouse with offset - no screen bounds
        self.x = mouse_x + self.offset_x
        self.y = mouse_y + self.offset_y

    def create_rain_or_fog(self):
        # Create a rain or fog particle below this cloud particle
        particle_x = self.x + random.uniform(-self.width//2, self.width//2)
        particle_y = self.y + self.height//2

        # Check if cloud is in bottom half of screen (300px is middle of 600px screen)
        if self.y > 300:
            # Create fog particle in bottom half
            return Particle(
                particle_x, particle_y,
                random.uniform(-0.3, 0.3), random.uniform(-0.2, 0.5),
                random.randint(8, 20), random.randint(8, 20),
                (200, 200, 210), random.randint(180, 300),
                0, "fog"
            )
        else:
            # Create rain particle in top half
            distance_to_ground = max(100, 550 - particle_y)
            ttl = int(distance_to_ground / 2) + random.randint(50, 100)

            return Particle(
                particle_x, particle_y,
                random.uniform(-0.5, 0.5), random.uniform(0.5, 3),
                random.randint(3, 6), random.randint(8, 12),
                (100, 150, 255), ttl,
                random.uniform(0.05, 0.15), "rain"
            )

    def draw(self, surface):
        rechthoek(surface, self.x, self.y, self.width, self.height, self.color, self.rotation)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cursor Cloud System")
    clock = pygame.time.Clock()

    # Create cloud particles that follow the mouse
    initial_count = 20
    cloud_particles = []
    for _ in range(initial_count):
        offset_x = random.uniform(-50, 50)
        offset_y = random.uniform(-30, 30)
        cloud_particles.append(CloudParticle(offset_x, offset_y, initial_count))

    rain_particles = []
    ground_y = 550

    # Generate fixed ground rectangles with random widths and heights
    ground_rects = []
    x = 0
    while x < 800:
        width = random.randint(4, 16)
        height = random.randint(3, 12)
        ground_rects.append({'x': x + width // 2, 'width': width, 'height': height, 'wetness': 0})
        x += width

    # Create random fire emitters on the ground
    fire_emitters = []
    for _ in range(random.randint(3, 6)):  # 3-6 fires
        fire_x = random.randint(50, 750)  # Keep away from edges
        fire_emitter = {
            'x': fire_x,
            'y': ground_y - 10,  # Slightly above ground
            'max_particles': random.randint(15, 25),
            'emit_rate': random.randint(2, 4),
            'active_particles': 0,
            'emit_timer': 0,
            'active': True,
            'age': 0,  # How long the fire has existed
            'growth_timer': 0,  # Timer for growing the fire
            'spawn_timer': 0  # Timer for spawning new fires
        }
        fire_emitters.append(fire_emitter)

    # Global fire spawn cooldown
    fire_spawn_cooldown = 0
    round_number = 1
    round_cooldown = 0  # Cooldown between rounds

    mouse_pressed = False
    rain_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Grow cloud - add more particles and resize existing ones
                    if len(cloud_particles) < 40:
                        current_count = len(cloud_particles)
                        offset_x = random.uniform(-50, 50)
                        offset_y = random.uniform(-30, 30)
                        cloud_particles.append(CloudParticle(offset_x, offset_y, current_count + 1))

                        # Resize existing particles to match new cloud size
                        for particle in cloud_particles[:-1]:  # All except the new one
                            base_size = 12 + (current_count + 1 - 5) * 0.8
                            size_variation = random.randint(-3, 8)
                            particle.width = max(8, int(base_size + size_variation))
                            particle.height = max(8, int(base_size + size_variation))

                elif event.key == pygame.K_MINUS:
                    # Shrink cloud - remove particles and resize existing ones
                    if len(cloud_particles) > 5:
                        cloud_particles.pop()
                        current_count = len(cloud_particles)

                        # Resize remaining particles to match new smaller cloud size
                        for particle in cloud_particles:
                            base_size = 12 + (current_count - 5) * 0.8
                            size_variation = random.randint(-3, 8)
                            particle.width = max(8, int(base_size + size_variation))
                            particle.height = max(8, int(base_size + size_variation))

        screen.fill((40, 60, 80))  # Darker sky color

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate cloud size based on number of cloud particles visible
        cloud_size = len(cloud_particles)

        # Update cloud particles to follow mouse
        for cloud in cloud_particles:
            cloud.update(mouse_x, mouse_y, cloud_size)
        # Rain intensity based on cloud size (more particles = more rain)
        rain_chance = min(0.8, cloud_size * 0.03)  # Cap at 80% chance

        # Create rain when mouse is pressed
        if mouse_pressed:
            rain_timer += 1
            rain_frequency = max(1, 5 - cloud_size // 4)  # Bigger clouds rain more frequently
            if rain_timer >= rain_frequency:
                for cloud in cloud_particles:
                    if random.random() < rain_chance:
                        rain_particles.append(cloud.create_rain_or_fog())
                rain_timer = 0

        # Update fire spawn cooldown and round cooldown
        fire_spawn_cooldown = max(0, fire_spawn_cooldown - 1)
        round_cooldown = max(0, round_cooldown - 1)

        # Update fire emitters
        for fire in fire_emitters:
            if not fire['active']:
                continue

            # Age the fire
            fire['age'] += 1
            fire['growth_timer'] += 1
            fire['spawn_timer'] += 1

            # Grow fire every 300 frames (5 seconds at 60fps)
            if fire['growth_timer'] >= 300:
                fire['max_particles'] = min(50, fire['max_particles'] + 5)  # Cap at 50
                fire['emit_rate'] = max(1, fire['emit_rate'] - 1)  # Faster emission, min 1
                fire['growth_timer'] = 0

            # Spawn new fire every 300 frames if no global cooldown
            if fire['spawn_timer'] >= 300 and fire_spawn_cooldown <= 0:
                # Try to spawn a new fire nearby
                attempts = 0
                while attempts < 10:  # Try 10 times to find a good spot
                    new_x = fire['x'] + random.randint(-100, 100)
                    if 50 <= new_x <= 750:  # Keep within bounds
                        # Check if too close to existing fires
                        too_close = False
                        for existing_fire in fire_emitters:
                            if existing_fire['active'] and abs(existing_fire['x'] - new_x) < 80:
                                too_close = True
                                break

                        if not too_close:
                            new_fire = {
                                'x': new_x,
                                'y': ground_y - 10,
                                'max_particles': random.randint(10, 15),  # Start smaller
                                'emit_rate': random.randint(3, 5),
                                'active_particles': 0,
                                'emit_timer': 0,
                                'active': True,
                                'age': 0,
                                'growth_timer': 0,
                                'spawn_timer': 0
                            }
                            fire_emitters.append(new_fire)
                            fire_spawn_cooldown = 300  # 5 second global cooldown
                            break
                    attempts += 1
                fire['spawn_timer'] = 0

            # Emit fire particles
            fire['emit_timer'] += 1
            if fire['emit_timer'] >= fire['emit_rate'] and fire['active_particles'] < fire['max_particles']:
                # Create fire particle
                fire_particle = Particle(
                    fire['x'] + random.uniform(-5, 5),
                    fire['y'],
                    random.uniform(-0.5, 0.5),
                    random.uniform(-3, -1),
                    random.randint(4, 10),
                    random.randint(6, 15),
                    (255, random.randint(100, 200), random.randint(0, 50)),
                    random.randint(60, 120),
                    0, "fire"
                )
                rain_particles.append(fire_particle)
                fire['active_particles'] += 1
                fire['emit_timer'] = 0

        # Check for rain hitting fires (extinguishing them)
        for particle in rain_particles:
            if particle.particle_type == "rain":
                for fire in fire_emitters:
                    if fire['active'] and abs(particle.x - fire['x']) < 20 and abs(particle.y - fire['y']) < 30:
                        fire['active'] = False  # Extinguish fire

        # Draw underground base layer
        rechthoek(screen, 400, 575, 800, 50, (60, 40, 20))

        # Draw gravelly ground with small rectangles
        for rect in ground_rects:
            # Calculate color based on wetness - more blue when wet
            base_gray = 80
            blue_amount = int(rect['wetness'] * 1.5)
            color = (max(0, base_gray - blue_amount // 2), max(0, base_gray - blue_amount // 2), min(255, base_gray + blue_amount))
            rechthoek(screen, rect['x'], ground_y - rect['height'] // 2, rect['width'], rect['height'], color)

            # Slowly dry the ground over time
            rect['wetness'] = max(0, rect['wetness'] - 0.2)

        # Update and draw rain particles
        dead_particles = [p for p in rain_particles if p.is_dead()]

        # Count fire particles per emitter and update counts
        fire_particle_counts = {}
        for fire in fire_emitters:
            fire_particle_counts[id(fire)] = 0

        for particle in rain_particles:
            if particle.particle_type == "fire" and not particle.is_dead():
                # Find closest fire emitter (rough matching)
                closest_fire = None
                min_distance = float('inf')
                for fire in fire_emitters:
                    if fire['active']:
                        distance = abs(particle.x - fire['x'])
                        if distance < min_distance and distance < 15:  # Within reasonable range
                            min_distance = distance
                            closest_fire = fire
                if closest_fire:
                    fire_particle_counts[id(closest_fire)] += 1

        # Update fire particle counts
        for fire in fire_emitters:
            fire['active_particles'] = fire_particle_counts.get(id(fire), 0)

        rain_particles = [p for p in rain_particles if not p.is_dead()]
        for particle in rain_particles:
            particle.update(ground_y, ground_rects)
            particle.draw(screen)

        # Draw cloud particles
        for cloud in cloud_particles:
            cloud.draw(screen)

        # Draw UI
        font = pygame.font.Font(None, 24)
        text = font.render(f"Particles: {len(rain_particles)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        text = font.render(f"Cloud size: {cloud_size} | Rain intensity: {int(rain_chance * 100)}%", True, (255, 255, 255))
        screen.blit(text, (10, 35))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 300:
            text = font.render("Hold mouse button to create fog!", True, (255, 255, 255))
        else:
            text = font.render("Hold mouse button to make it rain!", True, (255, 255, 255))
        screen.blit(text, (10, 60))

        text = font.render("Press +/- to grow/shrink cloud", True, (255, 255, 255))
        screen.blit(text, (10, 85))

        active_fires = sum(1 for fire in fire_emitters if fire['active'])

        # Check if all fires are extinguished - start new round
        if active_fires == 0 and len(fire_emitters) > 0 and round_cooldown == 0:
            # Start round cooldown
            round_cooldown = 180  # 3 seconds at 60fps

        # Create new round after cooldown
        if active_fires == 0 and len(fire_emitters) > 0 and round_cooldown == 1:
            # Clear all old fire emitters
            fire_emitters.clear()
            round_number += 1

            # Create new round of fires (more fires each round)
            num_fires = min(10, 3 + round_number)
            for _ in range(num_fires):
                fire_x = random.randint(50, 750)
                fire_emitter = {
                    'x': fire_x,
                    'y': ground_y - 10,
                    'max_particles': random.randint(15, 25),
                    'emit_rate': random.randint(2, 4),
                    'active_particles': 0,
                    'emit_timer': 0,
                    'active': True,
                    'age': 0,
                    'growth_timer': 0,
                    'spawn_timer': 0
                }
                fire_emitters.append(fire_emitter)

            fire_spawn_cooldown = 0  # Reset cooldown for new round

        text = font.render(f"Active fires: {active_fires}/{len(fire_emitters)}", True, (255, 255, 255))
        screen.blit(text, (10, 110))

        text = font.render(f"Round: {round_number}", True, (255, 255, 255))
        screen.blit(text, (10, 135))

        if active_fires == 0 and len(fire_emitters) > 0:
            if round_cooldown > 1:
                seconds_left = (round_cooldown - 1) // 60 + 1
                text = font.render(f"All fires extinguished! Next round in {seconds_left}s", True, (255, 255, 0))
                screen.blit(text, (10, 160))
            else:
                text = font.render("Starting new round!", True, (255, 255, 0))
                screen.blit(text, (10, 160))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()