class GameBoardController:
    def __init__(self):
        self.pieces = {}  # {(p, q): player_id}
        self.coords = []  # valid hex coordinates
        self.region_lookup = {}  # {(p, q): region_name}
        self.selected_piece = None

    def generate_board_coordinates(self):
        # Populate self.coords with valid board hexes
        pass

    def generate_region_lookup(self):
        # Map board hexes to visual regions
        pass

    def get_pieces(self):
        return self.pieces

    def get_board_state(self):
        return self.coords, self.region_lookup, self.pieces

    def select_piece(self, coord):
        # Mark a piece as selected if it's valid
        pass

    def get_selected_piece(self):
        return self.selected_piece

    def move_selected_piece(self, target_coord):
        # Move the selected piece if the move is valid
        pass

    def reset_selection(self):
        # Deselect the currently selected piece
        pass

    def is_valid_move(self, start, end):
        # Optional: Validate move based on game logic
        pass
