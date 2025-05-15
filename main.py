import pygame
import sys
from gameBoard import GameBoard

pygame.init()

LAUNCH_SCREEN_SIZE = (800, 600)
BG_COLOR = (10, 10, 10)
WHITE = (255, 255, 255)

# Fonts
FONT_BUTTON = pygame.font.SysFont('comic sans ms', 28, bold=True)
FONT_TITLE = pygame.font.SysFont('comic sans ms', 60, bold=True)

# Button colors
START_COLOR = (60, 120, 200)
START_HOVER = (85, 145, 225)
EXIT_COLOR = (160, 40, 40)
EXIT_HOVER = (185, 65, 65)

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
    pygame.init()
    
    launch = LaunchScreen()
    launch.run()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chinese Checkers - Game")
    
    board = GameBoard()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        board.draw(screen)
    
    pygame.quit()

if __name__ == "__main__":
    main()