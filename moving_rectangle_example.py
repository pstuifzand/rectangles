import pygame
import math

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Moving Rectangle Examples")
    clock = pygame.time.Clock()

    time = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Moving horizontally
        x1 = 100 + math.sin(time * 0.02) * 200
        rechthoek(screen, x=x1, y=100, color=(255, 0, 0))

        # Moving in circle
        x2 = 400 + math.cos(time * 0.03) * 150
        y2 = 300 + math.sin(time * 0.03) * 150
        rechthoek(screen, x=x2, y=y2, color=(0, 255, 0), rotation=time * 2)

        # Moving vertically with rotation
        y3 = 100 + math.sin(time * 0.025) * 180
        rechthoek(screen, x=600, y=y3, width=60, height=100, color=(0, 0, 255), rotation=time * 1.5)

        # Moving diagonally
        x4 = 50 + (time * 0.5) % 700
        y4 = 400 + math.sin(time * 0.04) * 100
        rechthoek(screen, x=x4, y=y4, width=40, height=80, color=(255, 255, 0), rotation=time * 3)

        # Rotating in place
        rechthoek(screen, x=400, y=500, width=100, height=30, color=(255, 0, 255), rotation=time * 4)

        pygame.display.flip()
        clock.tick(60)
        time += 1

    pygame.quit()

if __name__ == "__main__":
    main()