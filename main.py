import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Checkers")

board_img = pygame.image.load("chinese_checkers.png")
board_rect = board_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

title_font = pygame.font.SysFont('arial', 52, bold=True)
prompt_font = pygame.font.SysFont('arial', 32)

title_text = title_font.render("Chinese Checkers", True, (255, 255, 255))
prompt_text = prompt_font.render("Start", True, (200, 200, 200))

def launch_screen():
    while True:
        screen.fill((0, 0, 0))

        screen.blit(board_img, board_rect)

        screen.blit(title_text, (
            WIDTH // 2 - title_text.get_width() // 2,
            board_rect.top - 80
        ))

        screen.blit(prompt_text, (
            WIDTH // 2 - prompt_text.get_width() // 2,
            board_rect.bottom + 30
        ))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return 


if __name__ == "__main__":
    launch_screen()
    
