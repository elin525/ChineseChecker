import pygame
import sys

# Constants
LAUNCH_SCREEN_SIZE = (800, 600)  # Launch screen size
GAME_SCREEN_SIZE = (800, 600)    # Game screen size
BG_COLOR = (10, 10, 10)          # Dark background for launch screen
GAME_BG_COLOR = (250, 250, 250)  # Game background color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player colors
PLAYER_COLORS = {
    1: (220, 50, 50),   # Red
    2: (50, 90, 220),   # Blue
}

# Region colors (six corners + center)
REGION_COLORS = {
    'red': (250, 200, 200),
    'blue': (200, 200, 250),
    'green': (200, 255, 200),
    'yellow': (255, 255, 180),
    'purple': (230, 200, 255),
    'orange': (255, 220, 180),
    'center': WHITE,
}

# Game pieces
PIECES = {
    (-4, -1): 1, (-4, -2): 1, (-4, -3): 1, (-4, -4): 1,
    (-3, -2): 1, (-3, -3): 1, (-3, -4): 1,
    (-2, -3): 1, (-2, -4): 1,
    (-1, -4): 1,
    
    (1, 4): 2, (2, 4): 2, (3, 4): 2, (4, 4): 2,
    (2, 3): 2, (3, 3): 2, (4, 3): 2,
    (3, 2): 2, (4, 2): 2,
    (4, 1): 2,
}

pygame.init()

# Fonts
FONT_SMALL = pygame.font.Font(None, 16)
FONT_BUTTON = pygame.font.SysFont('comic sans ms', 28, bold=True)
FONT_TITLE = pygame.font.SysFont('comic sans ms', 60, bold=True)

# Button colors
START_COLOR = (60, 120, 200)
START_HOVER = (85, 145, 225)
EXIT_COLOR = (160, 40, 40)
EXIT_HOVER = (185, 65, 65)


class GameBoard:
    def __init__(self):
        self.unit_length = 22
        self.circle_radius = 12
        self.center_x = GAME_SCREEN_SIZE[0] // 2
        self.center_y = GAME_SCREEN_SIZE[1] // 2

    def hex_to_pixel(self, p, q):
        """Convert hex coordinates to pixel coordinates."""
        x = self.unit_length * (3**0.5) * (p + q / 2)
        y = self.unit_length * 1.5 * q
        return int(self.center_x + x), int(self.center_y - y)

    def generate_board_coordinates(self):
        """Generate all valid board coordinates."""
        coords = []
        
        # Central hexagon
        for p in range(-3, 4):
            for q in range(-3, 4):
                if -3 <= p + q <= 3:
                    coords.append((p, q))
        
        # Extended regions
        regions = [
            (range(-4, 1), range(4, 9), lambda p, q: p + q <= 4),    # Top-right
            (range(0, 5), range(-8, -3), lambda p, q: p + q >= -4),   # Bottom-left
            (range(-8, -3), range(0, 5), lambda p, q: p + q >= -4),   # Top-left
            (range(4, 9), range(-4, 1), lambda p, q: p + q <= 4),     # Bottom-right
            (range(0, 5), range(0, 5), lambda p, q: p + q >= 4),      # Far bottom-right
            (range(-4, 1), range(-4, 1), lambda p, q: p + q <= -4),   # Far top-left
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
        """Draw a game piece at the specified position."""
        color = PLAYER_COLORS[player]
        pygame.draw.circle(screen, color, (x, y), self.circle_radius - 1)
        pygame.draw.circle(screen, WHITE, (x - 3, y - 3), int(self.circle_radius * 0.3))  # Highlight
        pygame.draw.circle(screen, BLACK, (x + 2, y + 2), 2)  # Shadow
        pygame.draw.circle(screen, BLACK, (x, y), self.circle_radius, 1)  # Border

    def draw(self):
        """Draw the entire game board."""
        screen.fill(GAME_BG_COLOR)
        
        for p, q in self.generate_board_coordinates():
            x, y = self.hex_to_pixel(p, q)
            region = self.get_region(p, q)
            bg_color = REGION_COLORS[region]

            # Draw region background
            pygame.draw.circle(screen, bg_color, (x, y), self.circle_radius)
            pygame.draw.circle(screen, BLACK, (x, y), self.circle_radius, 1)

            # Draw piece if present
            if (p, q) in PIECES:
                self.draw_piece(x, y, PIECES[(p, q)])

            # Coordinate label
            #label = FONT_SMALL.render(f"{p},{q}", True, (90, 90, 90))
            #screen.blit(label, label.get_rect(center=(x, y)))
        
        pygame.display.flip()


class LaunchScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode(LAUNCH_SCREEN_SIZE)
        pygame.display.set_caption("Chinese Checkers")
        self.clock = pygame.time.Clock()
        
        self.board_img = pygame.image.load("chinese_checkers.png")
        self.board_rect = self.board_img.get_rect(center=(LAUNCH_SCREEN_SIZE[0] // 2, 
                                                          LAUNCH_SCREEN_SIZE[1] // 2 - 30))
        self.title_text = FONT_TITLE.render("Chinese Checkers", True, (240, 240, 230))
        
        
        # Button rectangles
        self.start_button = pygame.Rect(
            LAUNCH_SCREEN_SIZE[0] // 2 - 80,
            LAUNCH_SCREEN_SIZE[1] - 140,
            160, 45
        )
        self.exit_button = pygame.Rect(
            LAUNCH_SCREEN_SIZE[0] // 2 - 80,
            LAUNCH_SCREEN_SIZE[1] - 80,
            160, 45
        )

    def draw_button(self, text, rect, base_color, hover_color):
        """Draw a button with hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        color = hover_color if is_hover else base_color
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        text_surf = FONT_BUTTON.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return is_hover

    def run(self):
        """Run the launch screen loop."""
        while True:
            self.screen.fill(BG_COLOR)
            
            self.screen.blit(self.board_img, self.board_rect)
            self.screen.blit(
                    self.title_text,
                    (LAUNCH_SCREEN_SIZE[0] // 2 - self.title_text.get_width() // 2, 30)
                )

            # Draw buttons
            hover_start = self.draw_button(
                "Start", self.start_button, START_COLOR, START_HOVER
            )
            hover_exit = self.draw_button(
                "Exit", self.exit_button, EXIT_COLOR, EXIT_HOVER
            )

            # Change cursor on hover
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND if hover_start or hover_exit 
                else pygame.SYSTEM_CURSOR_ARROW
            )
            
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


def main():
    launch = LaunchScreen()
    launch.run()
    
    global screen
    screen = pygame.display.set_mode(GAME_SCREEN_SIZE)
    pygame.display.set_caption("Chinese Checkers - Game")
    
    board = GameBoard()
    board.draw()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()


if __name__ == "__main__":
    main()