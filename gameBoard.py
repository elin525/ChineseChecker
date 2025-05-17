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
        for x in range(-4, 5):
            for z in range(-4, 5):
                y = -x - z
                if abs(y) <= 4:
                    self.nodes[(x, z)] = node(x, z, GameState.EMPTY)


        # Define initial positions for ai pieces
        self.ai_nodes = {
            (-4, 5), (-3, 5), (-2, 5), (-1, 5),
            (-4, 6), (-3, 6), (-2, 6),
            (-4, 7), (-3, 7),
            (-4, 8)
        }
        for (x, z) in self.ai_nodes:
            self.nodes[(x, z)] = node(x, z, GameState.AI)

        # Define initial positions for player pieces
        self.player_nodes = {
            (1, -5), (2, -5), (3, -5), (4, -5),
            (2, -6), (3, -6), (4, -6),
            (3, -7), (4, -7),
            (4, -8)
        }
        for (x, z) in self.player_nodes:
            self.nodes[(x, z)] = node(x, z, GameState.PLAYER)

        # Add neighbors to each node based on 6 directions in a hex grid
        DIRECTIONS = [(1, 0), (1, -1), (0, -1),
                      (-1, 0), (-1, 1), (0, 1)]
        for (x, z), node_obj in self.nodes.items():
            for dx, dz in DIRECTIONS:
                neighbor_coord = (x + dx, z + dz)
                if neighbor_coord in self.nodes:
                    node_obj.neighbors.add(neighbor_coord)
                    

    def moveNode(self, start, end):
        """
        Moves a piece from current_pos to new_pos if the move is valid.
        Updates both the board state and the player's set.
        """
        moving_state = self.nodes[start].state
        self.nodes[start].state = GameState.EMPTY
        self.nodes[end].state = moving_state
        if moving_state == GameState.PLAYER:
            self.player_nodes.remove(start)
            self.player_nodes.add(end)
        elif moving_state == GameState.AI:
            self.ai_nodes.remove(start)
            self.ai_nodes.add(end)


#Example usage
board = gameBoard()
board.resetGameBoard()