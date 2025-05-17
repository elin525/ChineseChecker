from gameBoard import gameBoard, GameState


class gameLogic:

    @staticmethod
    def getPossibleMove(board: gameBoard, pos: tuple):
        """return all possible move and jump"""

        if pos not in board.nodes:
            return set()

        result = set()
        current_node = board.nodes[pos]
        for node in current_node.neighbors:
            if board.nodes[node].state == GameState.EMPTY:
                result.add((node))
            else:
                jump_node = (node[0] + (node[0] - pos[0]),
                             node[1] + (node[1] - pos[1]))
                if jump_node in board.nodes and board.nodes[jump_node].state == GameState.EMPTY:
                    if jump_node != pos:
                        result.add((jump_node))
        return result

    @staticmethod
    def getAllPossibleMoves(board: gameBoard, who: GameState):
        """Get all moves for PLAYER or AI as (start, end)."""
        if who not in (GameState.PLAYER, GameState.AI):
            raise ValueError("Invalid player type. Must be PLAYER or AI.")

        result = set()
        if who == GameState.PLAYER:
            for pos in board.player_nodes:
                possible_moves = gameLogic.getPossibleMove(board, pos)
                for move in possible_moves:
                    result.add((pos, move))
        else:
            for pos in board.ai_nodes:
                possible_moves = gameLogic.getPossibleMove(board, pos)
                for move in possible_moves:
                    result.add((pos, move))

        return result

    @staticmethod
    def is_valid_move(start, end, board: gameBoard):
        """Check if move is valid."""
        if start not in board.nodes or end not in board.nodes:
            return False
        allPossibleMoves = gameLogic.getPossibleMove(board, start)
        for move in allPossibleMoves:
            if move == end:
                return True
        return False

    @staticmethod
    def checkWinCondition(board: gameBoard):
        # check if any one wins
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
        if board.player_nodes <= player_goal:
            return GameState.PLAYER
        if board.ai_nodes <= ai_goal:
            return GameState.AI
        return GameState.EMPTY
