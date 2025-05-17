import pygame
from gameBoard import gameBoard, GameState
from gameLogic import gameLogic
from aiAgent import aiAgent
from gameboardGUI import GameBoardGUI

class GameBoardController:
    def __init__(self, board, gui):
        self.board = board
        self.gui = gui
        self.turn = 'player'  # 'player' or 'ai'
        self.selected = None  # Currently selected piece (pos)
        self.valid_moves = set()  # Valid moves for selected piece

    def get_pieces_dict(self):
        """
        Return {(x, z): 1 or 2} for drawing. 1=player, 2=ai
        """
        pieces = {}
        for pos in self.board.player_nodes:
            pieces[pos] = 1
        for pos in self.board.ai_nodes:
            pieces[pos] = 2
        return pieces

    def display_message(self, message):
        self.gui.draw(
            pieces=self.get_pieces_dict(),
            selected=self.selected,
            valid_moves=self.valid_moves,
            bg_color=(250, 250, 250)
        )
        font = pygame.font.SysFont(None, 48)
        text = font.render(message, True, (40, 0, 0))
        rect = text.get_rect(center=(self.gui.center_x, self.gui.center_y))
        self.gui.screen.blit(text, rect)
        pygame.display.flip()

    def check_and_handle_win(self):
        winner = gameLogic.checkWinCondition(self.board)
        if winner == GameState.PLAYER:
            self.display_message("You win! 🎉")
            pygame.time.wait(1200)
            self.board.resetGameBoard()
            self.selected = None
            self.valid_moves = set()
            self.turn = 'player'
        elif winner == GameState.AI:
            self.display_message("AI wins!")
            pygame.time.wait(1200)
            self.board.resetGameBoard()
            self.selected = None
            self.valid_moves = set()
            self.turn = 'player'

    def handle_click(self, mouse_pos):
        # Convert pixel to board position
        pos = self.gui.pixel_to_hex(*mouse_pos)
        if pos is None:
            
            return

        if self.turn == 'player':
            # If no piece is selected, try to select a player piece
            if self.selected is None:
                if pos in self.board.player_nodes:
                    self.selected = pos
                    self.valid_moves = gameLogic.getPossibleMove(self.board, pos)
            else:
                # If already selected, and click on valid move, perform move
                if pos in self.valid_moves:
                    self.board.moveNode(self.selected, pos)
                    self.selected = None
                    self.valid_moves = set()
                    self.check_and_handle_win()
                    self.turn = 'ai'
                # Clicked on another own piece: switch selection
                elif pos in self.board.player_nodes:
                    self.selected = pos
                    self.valid_moves = gameLogic.getPossibleMove(self.board, pos)
                # Otherwise: deselect
                else:
                    self.selected = None
                    self.valid_moves = set()

    def ai_turn(self):
        best_move = aiAgent.getBestMove(self.board, depth=2)
        if best_move:
            self.board.moveNode(*best_move)
        self.check_and_handle_win()
        self.turn = 'player'
        self.selected = None
        self.valid_moves = set()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            if self.turn == 'ai':
                pygame.time.wait(500)
                self.ai_turn()
            self.gui.draw(
                pieces=self.get_pieces_dict(),
                selected=self.selected,
                valid_moves=self.valid_moves,
                bg_color=(250, 250, 250)
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.turn == 'player':
                    self.handle_click(event.pos)
            clock.tick(60)

