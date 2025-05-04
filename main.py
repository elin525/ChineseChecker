import pygame
import sys

pygame.init()

# set up the launch screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Checkers")

# load the board image
board_img = pygame.image.load("chinese_checkers.png")
board_rect = board_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

# set up fonts
title_font = pygame.font.SysFont('comic sans ms', 60, bold=True)
button_font = pygame.font.SysFont('comic sans ms', 28, bold=True)

# title text
title_text = title_font.render("Chinese Checkers", True, (240, 240, 230))

# set up colors
BG_COLOR = (10, 10, 10)
START_COLOR = (60, 120, 200)
START_HOVER = (85, 145, 225)
EXIT_COLOR = (160, 40, 40)
EXIT_HOVER = (185, 65, 65)

# draw button
def draw_button(text, rect, base_color, hover_color, mouse_pos):
    is_hover = rect.collidepoint(mouse_pos)
    color = hover_color if is_hover else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return is_hover

def launch_screen():
    clock = pygame.time.Clock()

    # button rectangles
    start_button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 140, 160, 45)
    exit_button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 80, 160, 45)

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # render the board and title
        screen.blit(board_img, board_rect)
        screen.blit(title_text, (
            WIDTH // 2 - title_text.get_width() // 2,
            30
        ))

        # render buttons
        hover_start = draw_button("Start", start_button_rect, START_COLOR, START_HOVER, mouse_pos)
        hover_exit = draw_button("Exit", exit_button_rect, EXIT_COLOR, EXIT_HOVER, mouse_pos)

        # set mouse cursor
        if hover_start or hover_exit:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    launch_screen()
