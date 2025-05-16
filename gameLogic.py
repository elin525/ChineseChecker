from gameBoard import GameState
from gameBoard import gameBoard


class gameLogic:
    @staticmethod
    def is_valid_move(current_pos: tuple, new_pos: tuple, board: gameBoard) -> bool:
        """
        Checks if a basic (non-jump) move is valid for a given player or AI.
        """
        allPossibleMoves = gameLogic.getPossibleMove(board, current_pos)
        if (current_pos, new_pos) in allPossibleMoves:
            return True

        return False

    @staticmethod
    def is_valid_jump(path, board: gameBoard) -> bool:
        """
        Checks if a jump move from current_pos to new_pos is valid.
        """
        if len(path) < 2:
            return False  # must contain at least a start and one jump

        start = path[0]
        valid_paths = gameLogic.getAllPossibleJumps(board, start)
        return path in valid_paths

    @staticmethod
    def getPossibleMove(board: gameBoard, current_pos: tuple) -> set[tuple]:
        """
        Returns all possible 1-step moves from the current position.
        """

        # make sure the current position is in the board
        if current_pos not in board.nodes:
            return set()

        possible_moves = set()

        for neighbor in board.nodes[current_pos].neighbors:
            if board.nodes[neighbor].state == GameState.EMPTY:
                possible_moves.add((current_pos, neighbor))

        return possible_moves

    @staticmethod
    def getAllPossibleJumps(board: gameBoard, current_pos: tuple) -> set[tuple[tuple[int, int], ...]]:
        """
        Returns all possible jump path from the current position.
        each jump is a tuple of (from_pos, to_pos).
        """

        # make sure the current position is in the board
        if current_pos not in board.nodes:
            return set()

        allPossibleJumps: set[tuple[tuple[int, int], ...]] = set()

        jumpOver = set()

        for neighbor in board.nodes[current_pos].neighbors:
            if board.nodes[neighbor].state != GameState.EMPTY:
                jumpOver.add(neighbor)

        for piece in jumpOver:
            dx = piece[0]-current_pos[0]
            dz = piece[1]-current_pos[1]

            path = [current_pos]
            pos = current_pos

            while True:
                mid = (pos[0] + dx, pos[1] + dz)
                jump = (pos[0] + 2 * dx, pos[1] + 2 * dz)

                if (
                    mid in board.nodes and
                    jump in board.nodes and
                    board.nodes[mid].state != GameState.EMPTY and
                    board.nodes[jump].state == GameState.EMPTY
                ):
                    path.append(jump)
                    allPossibleJumps.add(tuple(path))
                    pos = jump
                else:
                    break

        return allPossibleJumps

    @staticmethod
    def getAllPossibleMoves(board: gameBoard, state: GameState) -> set[tuple[tuple[int, int], ...]]:
        """
        Returns all valid moves (normal + jumps) for the given player.
        Each move is a (from_pos, to_pos) tuple.
        """
        possible_moves: set[tuple[tuple[int, int], ...]] = set()
        positions = board.ai_nodes if state == GameState.AI else board.player_nodes

        for position in positions:
            possible_moves.update(gameLogic.getPossibleMove(board, position))
            possible_moves.update(
                gameLogic.getAllPossibleJumps(board, position))

        return possible_moves

    @staticmethod
    def checkWinCondition(board: gameBoard) -> GameState:
        """
        Checks the win condition.
        Returns:
            GameState.PLAYER if player wins,
            GameState.AI if AI wins,
            GameState.EMPTY (or None) if no one has won yet.
        """

        ai_nodes = {
            (1, -5), (2, -5), (3, -5), (4, -5),
            (2, -6), (3, -6), (4, -6),
            (3, -7), (4, -7),
            (4, -8)
        }

        player_nodes = {
            (-4, 5), (-3, 5), (-2, 5), (-1, 5),
            (-4, 6), (-3, 6), (-2, 6),
            (-4, 7), (-3, 7),
            (-4, 8)
        }

        if board.ai_nodes <= player_nodes:
            return GameState.AI
        if board.player_nodes <= ai_nodes:
            return GameState.PLAYER

        return GameState.EMPTY
