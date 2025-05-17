import pygame

GAME_SCREEN_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_COLORS = {
    1: (220, 50, 50),   # Red
    2: (50, 90, 220),   # Blue
}

REGION_COLORS = {
    'red': (250, 200, 200),
    'blue': (200, 200, 250),
    'green': (200, 255, 200),
    'yellow': (255, 255, 180),
    'purple': (230, 200, 255),
    'orange': (255, 220, 180),
    'center': WHITE,
}

class GameBoardGUI:
    def __init__(self, screen):
        self.screen = screen
        self.unit_length = 22
        self.circle_radius = 12
        self.center_x = GAME_SCREEN_SIZE[0] // 2
        self.center_y = GAME_SCREEN_SIZE[1] // 2
        self.font = pygame.font.Font(None, 16)
        self.board_coords = self.generate_board_coordinates()

    def hex_to_pixel(self, p, q):
        x = self.unit_length * (3**0.5) * (p + q / 2)
        y = self.unit_length * 1.5 * q
        return int(self.center_x + x), int(self.center_y - y)

    def pixel_to_hex(self, x, y):
        rel_x = x - self.center_x
        rel_y = self.center_y - y
        q = (rel_x * (3**0.5)/3 - rel_y / 3) / self.unit_length
        r = rel_y * 2/3 / self.unit_length
        cube_x = q
        cube_z = r
        cube_y = -cube_x - cube_z
        rx = round(cube_x)
        ry = round(cube_y)
        rz = round(cube_z)
        x_diff = abs(rx - cube_x)
        y_diff = abs(ry - cube_y)
        z_diff = abs(rz - cube_z)
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
        hex_coord = (rx, rz)
        if hex_coord in self.board_coords:
            return hex_coord
        return None

    def generate_board_coordinates(self):
        coords = []
        for p in range(-3, 4):
            for q in range(-3, 4):
                if -3 <= p + q <= 3:
                    coords.append((p, q))
        regions = [
            (range(-4, 1), range(4, 9), lambda p, q: p + q <= 4),
            (range(0, 5), range(-8, -3), lambda p, q: p + q >= -4),
            (range(-8, -3), range(0, 5), lambda p, q: p + q >= -4),
            (range(4, 9), range(-4, 1), lambda p, q: p + q <= 4),
            (range(0, 5), range(0, 5), lambda p, q: p + q >= 4),
            (range(-4, 1), range(-4, 1), lambda p, q: p + q <= -4),
        ]
        for p_range, q_range, condition in regions:
            for p in p_range:
                for q in q_range:
                    if condition(p, q):
                        coords.append((p, q))
        return coords

    def get_region(self, p, q):
        regions = {
            'red': [(-4, -1), (-4, -2), (-4, -3), (-4, -4),
                    (-3, -2), (-3, -3), (-3, -4),
                    (-2, -3), (-2, -4),
                    (-1, -4)],
            'blue': [(1, 4), (2, 4), (3, 4), (4, 4),
                     (2, 3), (3, 3), (4, 3),
                     (3, 2), (4, 2),
                     (4, 1)],
            'green': [(-1, 5), (-2, 5), (-2, 6),
                      (-3, 5), (-3, 6), (-3, 7),
                      (-4, 5), (-4, 6), (-4, 7), (-4, 8)],
            'yellow': [(1, -5), (2, -5), (2, -6),
                        (3, -5), (3, -6), (3, -7),
                        (4, -5), (4, -6), (4, -7), (4, -8)],
            'purple': [(-8, 4), (-7, 4), (-6, 4), (-5, 4),
                        (-7, 3), (-6, 3), (-5, 3),
                        (-6, 2), (-5, 2),
                        (-5, 1)],
            'orange': [(5, -1), (5, -2), (6, -2),
                       (5, -3), (6, -3), (7, -3),
                       (5, -4), (6, -4), (7, -4), (8, -4)],
        }
        for region, coords in regions.items():
            if (p, q) in coords:
                return region
        return 'center'

    def draw_piece(self, x, y, player):
        color = PLAYER_COLORS[player]
        pygame.draw.circle(self.screen, color, (x, y), self.circle_radius - 1)
        pygame.draw.circle(self.screen, WHITE, (x - 3, y - 3), int(self.circle_radius * 0.3))
        pygame.draw.circle(self.screen, BLACK, (x + 2, y + 2), 2)
        pygame.draw.circle(self.screen, BLACK, (x, y), self.circle_radius, 1)

    def draw_highlight(self, x, y):
        highlight_color = (255, 255, 0)
        pygame.draw.circle(self.screen, highlight_color, (x, y), self.circle_radius + 2, 2)

    def draw_valid_moves(self, move_coords):
        for (p, q) in move_coords:
            x, y = self.hex_to_pixel(p, q)
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), self.circle_radius - 4, 2)

    def draw(self, pieces, selected=None, valid_moves=None, bg_color=(250, 250, 250)):
        self.screen.fill(bg_color)
        for p, q in self.board_coords:
            x, y = self.hex_to_pixel(p, q)
            # Always use region color as background
            region = self.get_region(p, q)
            region_color = REGION_COLORS[region]
            pygame.draw.circle(self.screen, region_color, (x, y), self.circle_radius)
            pygame.draw.circle(self.screen, BLACK, (x, y), self.circle_radius, 1)
            # Draw highlight if this is selected
            if selected == (p, q):
                self.draw_highlight(x, y)
            # Draw piece if present
            if (p, q) in pieces:
                self.draw_piece(x, y, pieces[(p, q)])
            # Draw valid move markers
            if valid_moves and (p, q) in valid_moves:
                self.draw_valid_moves([(p, q)])
            # Draw coordinate label
            label = self.font.render(f"{p},{q}", True, BLACK)
            self.screen.blit(label, label.get_rect(center=(x, y)))
        pygame.display.flip()
