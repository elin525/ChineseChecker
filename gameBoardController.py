from gameBoard import gameBoard, node, GameState
from gameLogic import gameLogic

def generate_two_player_board_coords():
    coords = []
    # Center hex
    for x in range(-4, 5):
        for z in range(-4, 5):
            y = -x - z
            if abs(y) <= 4:
                coords.append((x, z))
    # Player arms
    for x, z in [(1, -5), (2, -5), (3, -5), (4, -5),
                 (2, -6), (3, -6), (4, -6),
                 (3, -7), (4, -7), (4, -8)]:
        coords.append((x, z))
    for x, z in [(-4, 5), (-3, 5), (-2, 5), (-1, 5),
                 (-4, 6), (-3, 6), (-2, 6),
                 (-4, 7), (-3, 7), (-4, 8)]:
        coords.append((x, z))
    return list(set(coords))

class GameBoardController:
    def __init__(self):
        self.coords = generate_two_player_board_coords()
        self.selected_piece = None
        self.current_player = 1  # 1 for player, 2 for AI
        self.pieces = {}
        for pos in [(1, -5), (2, -5), (3, -5), (4, -5),
                    (2, -6), (3, -6), (4, -6),
                    (3, -7), (4, -7), (4, -8)]:
            self.pieces[pos] = 1
        for pos in [(-4, 5), (-3, 5), (-2, 5), (-1, 5),
                    (-4, 6), (-3, 6), (-2, 6),
                    (-4, 7), (-3, 7), (-4, 8)]:
            self.pieces[pos] = 2
        self.last_valid_moves = set()

    def get_pieces(self):
        return self.pieces

    def get_selected_piece(self):
        return self.selected_piece

    def get_valid_moves(self):
        if not self.selected_piece or self.pieces[self.selected_piece] != self.current_player:
            return set()
        board = self.to_game_board()
        moves = set()
        # Add all adjacent moves' destinations
        for move in gameLogic.getPossibleMove(board, self.selected_piece):
            moves.add(move[1])  # move is (from, to)
        # Add jump moves' destinations
        for move in gameLogic.getAllPossibleJumps(board, self.selected_piece):
            moves.add(move[1])  # move is (from, to)
        return moves


    def select_piece(self, coord):
        if coord in self.pieces and self.pieces[coord] == self.current_player:
            self.selected_piece = coord
            return True
        return False

    def try_move(self, coord):
        # Try to move using game logic, don't just update self.pieces!
        if not self.selected_piece:
            self.select_piece(coord)
            return False
        valid = self.get_valid_moves()
        if coord in valid:
            board = self.to_game_board()
            # Call your board move function (will update nodes/player_nodes/ai_nodes)
            board.moveNode(self.selected_piece, coord)
            # Now sync self.pieces with board state
            self.pieces = {}
            for pos, n in board.nodes.items():
                if n.state == GameState.PLAYER:
                    self.pieces[pos] = 1
                elif n.state == GameState.AI:
                    self.pieces[pos] = 2
            self.selected_piece = None
            self.last_valid_moves = set()
            return True
        if coord in self.pieces and self.pieces[coord] == self.current_player:
            self.selected_piece = coord
        return False

    def to_game_board(self):
        board = gameBoard()
        board.nodes.clear()
        board.player_nodes = set()
        board.ai_nodes = set()
        for coord in self.coords:
            board.nodes[coord] = node(coord[0], coord[1], GameState.EMPTY)
        for coord, player in self.pieces.items():
            if coord in board.nodes:
                if player == 1:
                    board.nodes[coord].state = GameState.PLAYER
                    board.player_nodes.add(coord)
                else:
                    board.nodes[coord].state = GameState.AI
                    board.ai_nodes.add(coord)
        return board
