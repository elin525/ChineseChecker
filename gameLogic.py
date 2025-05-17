from gameBoard import gameBoard, GameState

class gameLogic:

    @staticmethod
    def getPossibleMove(board: gameBoard, pos: tuple) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        """Return all simple (adjacent) moves for the piece at pos as (start, end)."""
        if pos not in board.nodes or board.nodes[pos].state == GameState.EMPTY:
            return set()
        moves = set()
        for neighbor in board.nodes[pos].neighbors:
            if neighbor in board.nodes and board.nodes[neighbor].state == GameState.EMPTY:
                moves.add((pos, neighbor))
        return moves

    @staticmethod
    def getAllPossibleJumps(board: gameBoard, pos: tuple) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        """Return all valid jump moves from pos as (start, end) tuples."""
        all_jumps = set()
        gameLogic._find_jumps(board, pos, pos, set(), all_jumps)
        return all_jumps

    @staticmethod
    def _find_jumps(board, start, current, visited, result):
        """Recursive helper for jump logic."""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        for dx, dy in directions:
            mid = (current[0] + dx, current[1] + dy)
            dest = (current[0] + 2*dx, current[1] + 2*dy)
            if (
                mid in board.nodes and
                dest in board.nodes and
                board.nodes[mid].state != GameState.EMPTY and
                board.nodes[dest].state == GameState.EMPTY and
                dest not in visited
            ):
                result.add((start, dest))
                gameLogic._find_jumps(board, start, dest, visited | {dest}, result)

    @staticmethod
    def getAllPossibleMoves(board: gameBoard, who: GameState) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        """Get all moves for PLAYER or AI as (start, end)."""
        result = set()
        node_set = board.player_nodes if who == GameState.PLAYER else board.ai_nodes
        for pos in node_set:
            result |= gameLogic.getPossibleMove(board, pos)
            result |= gameLogic.getAllPossibleJumps(board, pos)
        return result

    @staticmethod
    def is_valid_move(start, end, board: gameBoard) -> bool:
        """Check if a simple adjacent move is valid."""
        return (start, end) in gameLogic.getPossibleMove(board, start)

    @staticmethod
    def is_valid_jump(start, end, board: gameBoard) -> bool:
        """Check if a jump move is valid."""
        return (start, end) in gameLogic.getAllPossibleJumps(board, start)

    @staticmethod
    def checkWinCondition(board: gameBoard):
        # Checks if player or AI occupies all of opponent's home positions
        player_goal = {
            (-4, 5), (-3, 5), (-2, 5), (-1, 5),
            (-4, 6), (-3, 6), (-2, 6),
            (-4, 7), (-3, 7), (-4, 8)
        }
        ai_goal = {
            (1, -5), (2, -5), (3, -5), (4, -5),
            (2, -6), (3, -6), (4, -6),
            (3, -7), (4, -7), (4, -8)
        }
        # If all goal spots are occupied by correct player, that player wins
        if all(board.nodes[pos].state == GameState.PLAYER for pos in player_goal):
            return GameState.PLAYER
        if all(board.nodes[pos].state == GameState.AI for pos in ai_goal):
            return GameState.AI
        return GameState.EMPTY  # Game not over
