from gameBoard import gameBoard
from gameBoard import GameState
from gameLogic import gameLogic
from gameBoard import node
import copy

class aiAgent:

    @staticmethod
    def _hex_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        x1, z1 = a
        x2, z2 = b

        dx = abs(x1 - x2)
        dy = abs((-x1 - z1) - (-x2 - z2)) 
        dz = abs(z1 - z2)

        return max(dx, dy, dz)

    @staticmethod
    def _evaluate(board: gameBoard) -> int:
        """
        Evaluates the board state.
        Higher score means AI is closer to winning.
        """
        # AI tries to reach player_start_zone
        player_goal = {
            (-4, 5), (-3, 5), (-2, 5), (-1, 5),
            (-4, 6), (-3, 6), (-2, 6),
            (-4, 7), (-3, 7),
            (-4, 8)
        }

        # Player tries to reach ai_start_zone
        ai_goal = {
            (1, -5), (2, -5), (3, -5), (4, -5),
            (2, -6), (3, -6), (4, -6),
            (3, -7), (4, -7),
            (4, -8)
        }

        ai_score = 0
        for piece in board.ai_nodes:
            min_dist = min(aiAgent._hex_distance(piece, goal) for goal in ai_goal)
            ai_score += min_dist

        player_score = 0
        for piece in board.player_nodes:
            min_dist = min(aiAgent._hex_distance(piece, goal) for goal in player_goal)
            player_score += min_dist

        # Lower distance for AI is good → subtract AI’s distance
        return player_score - ai_score

    @staticmethod
    def _minimax_pruning(board: gameBoard, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or gameLogic.checkWinCondition(board) != GameState.EMPTY:
            return aiAgent._evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in gameLogic.getAllPossibleMoves(board, GameState.AI):
                new_board = copy.deepcopy(board)
                start, end = move
                new_board.moveNode(start, end)

                eval = aiAgent._minimax_pruning(
                    new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return max_eval

        else:
            min_eval = float('inf')
            for move in gameLogic.getAllPossibleMoves(board, GameState.PLAYER):
                new_board = copy.deepcopy(board)
                start, end = move
                new_board.moveNode(start, end)

                eval = aiAgent._minimax_pruning(
                    new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break 
            return min_eval

    @staticmethod
    def getBestMove(board: gameBoard, depth: int) -> tuple[tuple[int, int], ...]:
        """
        Returns the best move for the AI: (start, end)
        """
        best_move = None
        best_value = float('-inf')

        for move in gameLogic.getAllPossibleMoves(board, GameState.AI):
            new_board = copy.deepcopy(board)
            start, end = move
            new_board.moveNode(start, end)

            move_value = aiAgent._minimax_pruning(
                new_board, depth - 1, float('-inf'), float('inf'), False)

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move  

from gameBoard import gameBoard, GameState
from gameLogic import gameLogic
from aiAgent import aiAgent

if __name__ == "__main__":
    # Create a new board
    board = gameBoard()

    ai_piece = (-4, 5)
    moves = gameLogic.getPossibleMove(board, ai_piece)
    print(f"Possible moves for AI piece {ai_piece}:", moves)

    # 4. If there is a move, move the AI piece to the first possible move
    if moves:
        move_to = (-4,4)
        print(f"Moving AI piece from {ai_piece} to {move_to}")
        board.moveNode(ai_piece, move_to)
        
    print(board.nodes[move_to].state)  # Should be AI
    print(board.nodes[ai_piece].state)  # Should be EMPTY
    
    move_to = (4,-4)
    human_piece = (4,-5)
    board.moveNode(move_to, ai_piece)  # Move back to original position
    print(board.nodes[move_to].state)  # Should be EMPTY
    print(board.nodes[human_piece].state)  # Should be human
    board.moveNode((-3,5),(-2,4))
    board.moveNode((3,-6),(1,-4))
    print(aiAgent.getBestMove(board, 2))  # Get the best move for AI