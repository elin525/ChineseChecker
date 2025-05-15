import pygame
from enum import Enum

# Constants
GAME_SCREEN_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

class GameState(Enum):
    EMPTY = 0
    PLAYER = 1
    AI = 2

class Node:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.neighbors = set()
        self.state = state

class GameBoard:
    def __init__(self):
        self.unit_length = 22
        self.circle_radius = 12
        self.center_x = GAME_SCREEN_SIZE[0] // 2
        self.center_y = GAME_SCREEN_SIZE[1] // 2
        self.nodes = {}
        self.player_nodes = set()
        self.ai_nodes = set()
        self.reset_game_board()

    def reset_game_board(self):
        """Reset the game board to its initial state."""
        self.nodes = {}
        self.player_nodes = set()
        self.ai_nodes = set()
        
        # Central hexagon
        for p in range(-3, 4):
            for q in range(-3, 4):
                if -3 <= p + q <= 3:
                    self.nodes[(p, q)] = Node(p, q, GameState.EMPTY)
        
        # Player 1 (Red) pieces
        for coord in [(-4, -1), (-4, -2), (-4, -3), (-4, -4),
                      (-3, -2), (-3, -3), (-3, -4),
                      (-2, -3), (-2, -4),
                      (-1, -4)]:
            self.nodes[coord] = Node(coord[0], coord[1], GameState.PLAYER)
            self.player_nodes.add(coord)
        
        # Player 2 (Blue) pieces
        for coord in [(1, 4), (2, 4), (3, 4), (4, 4),
                      (2, 3), (3, 3), (4, 3),
                      (3, 2), (4, 2),
                      (4, 1)]:
            self.nodes[coord] = Node(coord[0], coord[1], GameState.AI)
            self.ai_nodes.add(coord)

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

    def draw_piece(self, screen, x, y, player):
        """Draw a game piece at the specified position."""
        color = PLAYER_COLORS[player]
        pygame.draw.circle(screen, color, (x, y), self.circle_radius - 1)
        pygame.draw.circle(screen, WHITE, (x - 3, y - 3), int(self.circle_radius * 0.3))  # Highlight
        pygame.draw.circle(screen, BLACK, (x + 2, y + 2), 2)  # Shadow
        pygame.draw.circle(screen, BLACK, (x, y), self.circle_radius, 1)  # Border

    def draw(self, screen):
        """Draw the entire game board."""
        screen.fill(WHITE)
        
        for p, q in self.generate_board_coordinates():
            x, y = self.hex_to_pixel(p, q)
            region = self.get_region(p, q)
            bg_color = REGION_COLORS[region]

            # Draw region background
            pygame.draw.circle(screen, bg_color, (x, y), self.circle_radius)
            pygame.draw.circle(screen, BLACK, (x, y), self.circle_radius, 1)

            # Draw piece if present
            if (p, q) in PIECES:
                self.draw_piece(screen, x, y, PIECES[(p, q)])
        
        pygame.display.flip()

    def move_node(self, current_pos, new_pos):
        """Move a piece from current position to new position."""
        if current_pos in self.nodes and new_pos in self.nodes:
            current_node = self.nodes[current_pos]
            new_node = self.nodes[new_pos]
            
            if current_node.state != GameState.EMPTY and new_node.state == GameState.EMPTY:
                if current_node.state == GameState.PLAYER:
                    new_node.state = GameState.PLAYER
                    current_node.state = GameState.EMPTY
                    self.player_nodes.remove(current_pos)
                    self.player_nodes.add(new_pos)
                elif current_node.state == GameState.AI:
                    new_node.state = GameState.AI
                    current_node.state = GameState.EMPTY
                    self.ai_nodes.remove(current_pos)
                    self.ai_nodes.add(new_pos)
                    
    