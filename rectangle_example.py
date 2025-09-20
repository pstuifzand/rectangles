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
    pygame.display.set_caption("Rectangle Examples")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        rechthoek(screen)
        rechthoek(screen, x=200, y=150, color=(255, 0, 0))
        rechthoek(screen, x=300, y=200, width=120, height=60, color=(0, 255, 0), rotation=45)
        rechthoek(screen, x=450, y=100, color=(0, 0, 255), rotation=30)
        rechthoek(screen, x=600, y=300, width=100, height=20, color=(255, 255, 0), rotation=90)
        rechthoek(screen, x=150, y=400, width=60, height=100, color=(255, 0, 255), rotation=15)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()