from enum import Enum


class GameState(Enum):
    EMPTY = 0
    PLAYER = 1
    AI = 2


class node:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.neighbors = set()
        self.state = state  # 0: empty, 1: player, 2: ai


class gameBoard:
    def __init__(self):
        self.nodes = {}  # dictionary to store the game board (all nodes)
        self.player_nodes = set()  # set to store tuple of (x,z) coordinates of player nodes
        self.ai_nodes = set()  # set to store tuple of (x,z) coordinates of ai nodes
        self.resetGameBoard()  # initialize the game board

    def resetGameBoard(self):
        # reset the game board to its initial state
        self.nodes[(0,0)] = node(0, 0, GameState.EMPTY)
        
        # central empty node
        for x in range(-4,5):
            for z in range(-4,5):
                y=-x-z
                if abs(y) <= 4:
                    self.nodes[(x,z)] = node(x, z, GameState.EMPTY)
        
        # player nodes
        self.player_nodes = {(-4, 5), (-3, 5), (-2, 5), (-1, 5),
                                (-4, 6), (-3, 6), (-2, 6), 
                                (-4, 7), (-3, 7), 
                                (-4, 8)}
        
        for (x,z) in self.player_nodes:
            self.nodes[(x,z)]=node(x,z,GameState.PLAYER)
            
        # ai nodes
        self.ai_nodes = {(1, -5),(2, -5),(3, -5),(4, -5),
                            (2, -6), (3, -6), (4, -6),
                            (3, -7), (4, -7),
                            (4, -8)}
        
        for (x,z) in self.ai_nodes:
            self.nodes[(x,z)]=node(x,z,GameState.AI)
            
        # add neighbors to each node
        
            
    # move a node from current_pos to new_pos
    def moveNode(self, current_pos, new_pos):
        if current_pos in self.nodes and new_pos in self.nodes:
            if current_pos.state != GameState.EMPTY and new_pos.state == GameState.EMPTY:
                if current_pos.state == GameState.PLAYER:
                    new_pos.state = GameState.PLAYER
                    current_pos.state = GameState.EMPTY
                    self.player_nodes.remove(current_pos)
                    self.player_nodes.add(new_pos)
                elif current_pos.state == GameState.AI:
                    new_pos.state = GameState.AI
                    current_pos.state = GameState.EMPTY
                    self.ai_nodes.remove(current_pos)
                    self.ai_nodes.add(new_pos)
                
# Example usage
        
       
            

board = gameBoard()
board.resetGameBoard()


# dictionary to store the game board (all nodes)
# 3 sets to store tuple of (x,z) coordinates of player, ai, and empty nodes
# class gameBoard:
#     def __init__(self):
