from enum import Enum


class GameState(Enum):
    """
    Enum to represent the state of a board cell.
    """
    EMPTY = 0
    PLAYER = 1
    AI = 2


class node:
    """
    Represents a single node on the game board.
    """

    def __init__(self, x, z, state):
        self.x = x
        self.z = z
        self.neighbors = set() # Set of coordinates of neighboring nodes
        self.state = state # GameState enum: EMPTY, PLAYER, or AI

def generate_two_player_board_coords():
    coords = []
    # Main center hexagon (radius 4)
    for x in range(-4, 5):
        for z in range(-4, 5):
            y = -x - z
            if abs(y) <= 4:
                coords.append((x, z))
    # Player 1 "arm" (bottom right)
    for x, z in [
        (1, -5), (2, -5), (3, -5), (4, -5),
        (2, -6), (3, -6), (4, -6),
        (3, -7), (4, -7),
        (4, -8)
    ]:
        coords.append((x, z))
    # Player 2/AI "arm" (top left)
    for x, z in [
        (-4, 5), (-3, 5), (-2, 5), (-1, 5),
        (-4, 6), (-3, 6), (-2, 6),
        (-4, 7), (-3, 7),
        (-4, 8)
    ]:
        coords.append((x, z))
    return list(set(coords))

class gameBoard:
    """
    Represents the entire Chinese Checkers game board.
    Stores all node positions and their states.
    """

    def __init__(self):
        self.nodes = {} # {(x, z): node}
        self.player_nodes = set() # Set of (x, z) for player-occupied nodes
        self.ai_nodes = set() # Set of (x, z) for AI-occupied nodes
        self.resetGameBoard() # Initialize the board
      

    def resetGameBoard(self):
        """
        Resets the board to its initial configuration with pieces in starting positions.
        """
        # Initialize central empty board region
        for x, z in generate_two_player_board_coords():
            self.nodes[(x, z)] = node(x, z, GameState.EMPTY)


        # Add neighbors to each node based on 6 directions in a hex grid
        DIRECTIONS = [(1, 0), (1, -1), (0, -1),
                      (-1, 0), (-1, 1), (0, 1)]
        for (x, z), node_obj in self.nodes.items():
            for dx, dz in DIRECTIONS:
                neighbor_coord = (x + dx, z + dz)
                if neighbor_coord in self.nodes:
                    node_obj.neighbors.add(neighbor_coord)
                    

    def moveNode(self, current_pos, new_pos):
        """
        Moves a piece from current_pos to new_pos if the move is valid.
        Updates both the board state and the player's set.
        """
        if current_pos in self.nodes and new_pos in self.nodes:
            current_node = self.nodes[current_pos]
            new_node = self.nodes[new_pos]

            if current_node.state != GameState.EMPTY and new_node.state == GameState.EMPTY:
                if current_node.state == GameState.PLAYER:
                    new_node.state = GameState.PLAYER
                    current_node.state = GameState.EMPTY
                    self.player_nodes.remove(current_pos)
                    self.player_nodes.add(new_pos)

                elif current_node.state == GameState.AI:
                    new_node.state = GameState.AI
                    current_node.state = GameState.EMPTY
                    self.ai_nodes.remove(current_pos)
                    self.ai_nodes.add(new_pos)


#Example usage
board = gameBoard()
board.resetGameBoard()