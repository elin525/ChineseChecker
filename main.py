import pygame
import sys
from gameboardGUI import GameBoardGUI
from gameBoardController import GameBoardController
from aiAgent import aiAgent

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chinese Checkers (Minimal Demo)")
gui = GameBoardGUI(screen)
controller = GameBoardController()
clock = pygame.time.Clock()

current_turn = 1  # 1 = player, 2 = AI

running = True
while running:
    screen.fill((245, 245, 245))
    valid_moves = controller.get_valid_moves()
    gui.draw(controller.get_pieces(), controller.get_selected_piece(), valid_moves)
    pygame.display.flip()

    # Handle player turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and current_turn == 1:
            coord = gui.pixel_to_hex(*event.pos)
            if coord:
                # Print state before move
                sel = controller.selected_piece if controller.selected_piece else coord
                print(f"[Player] Before move: start {sel} state = {controller.get_pieces().get(sel)}, end {coord} state = {controller.get_pieces().get(coord)}")
                moved = controller.try_move(coord)
                # Print state after move
                print(f"[Player] After move: start {sel} state = {controller.get_pieces().get(sel)}, end {coord} state = {controller.get_pieces().get(coord)}")
                if moved:
                    print("Player moved.")
                    current_turn = 2  # Switch to AI

    # Handle AI turn (outside event loop, so it happens automatically after player)
    if current_turn == 2:
        print("AI is thinking...")
        board_for_ai = controller.to_game_board()
        ai_move = aiAgent.getBestMove(board_for_ai, depth=2)
        print(f"AI best move: {ai_move}")

        if ai_move:
            start, end = ai_move
            # Print state before AI move
            print(f"[AI] Before move: start {start} state = {controller.get_pieces().get(start)}, end {end} state = {controller.get_pieces().get(end)}")
            controller.selected_piece = start
            ai_moved = controller.try_move(end)
            controller.selected_piece = None
            # Print state after AI move
            print(f"[AI] After move: start {start} state = {controller.get_pieces().get(start)}, end {end} state = {controller.get_pieces().get(end)}")
            if ai_moved:
                print(f"AI moved from {start} to {end}.")
            else:
                print(f"AI failed to move from {start} to {end}.")
        else:
            print("AI has no valid moves!")
        current_turn = 1  # Switch back to player

    clock.tick(60)

pygame.quit()
sys.exit()
