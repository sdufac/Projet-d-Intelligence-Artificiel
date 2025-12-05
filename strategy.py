from logging import info
from math import inf
from time import process_time_ns
from typing import List, Optional
from logic import GameState, Move, apply_move
from utils import num_degree,freeNeighbor
import random
from game import Game
import copy
from logic import _check_induced_path_property
from typing import List, Optional, Dict, Set
from logic import GameState, Move, get_legal_moves
import random

# This file as well as utils.py should be the only ones you have to edit!

class Strategy:
    """
    Base strategy class. Students should subclass this and implement select_move,
    as well as any helper methods they need.
    """
    def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
        """
        Select a move for the given player in the given state.

        :param state: (GameState) The current game state.
        :param G: (Dict[int, Set[int]]) Adjacency dictionary representing the graph.
        :param player: (int) The ID of the current player, 0 or 1.
        :param legal_moves: (List[Move]) A list of legal moves available to the given player.
        :return: (Optional[Move]) The selected move, or None to forfeit.
        """
        raise NotImplementedError

class RandomStrategy(Strategy):
    def __init__(self, seed: int = None):
        self.rnd = random.Random(seed)

    def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
        legal_moves = get_legal_moves(state, G, player)
        if not legal_moves:
            return None
        return self.rnd.choice(legal_moves)


class GreedyMaxDegreeStrategy(Strategy):
    """
    Pick the move that gives your endpoint the highest number of free neighbors after the move.
    Simple and explainable baseline. This is an example strategy class; you should design your own.
    """
    def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
        best = None
        best_score = -1
        legal_moves = get_legal_moves(state, G, player)
        for m in legal_moves:
            # simulate
            new_end = m.to_node
            free_neighbors = sum(1 for v in state.G[new_end] if v not in state.occupied)
            if free_neighbors > best_score:
                best_score = free_neighbors
                best = m
        return best

# TODO: You should implement your own strategies here (Minimax, MCTS, etc.)

class MinMaxStrategy(Strategy):

    # def min_max_search(self, state: GameState,player : int)
    def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
        depth = 4

        move = None
        (value,move) = self.maxValue(state,player, depth)
        return move

    def maxValue(self,state :GameState,player :int, depth: int) -> tuple[int,Move | None]:
        legal_move = get_legal_moves(state,state.G,player)
        if not legal_move: 
            return (-10000,None)
        elif depth < 0:
            sommetPlayer = state.endpoints[player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,sommetPlayer,state),None)

        v = -999999
        move = None
        actions = get_legal_moves(state,state.G,player)
        for a in actions:
            nextState = copy.deepcopy(state)
            apply_move(nextState,player,a)
            v2,a2 = self.minValue(nextState,1-player,depth - 1)
            if v2 > v:
                v = v2
                move = a
        return (v,move)



    def minValue(self,state:GameState,player :int, depth:int)-> tuple[int,Move | None]:
        legal_move = get_legal_moves(state,state.G,player)
        if not legal_move: 
            return (10000,None)
        elif depth < 0:
            sommetPlayer = state.endpoints[1 - player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,sommetPlayer,state),None)

        
        v = 999999
        move = None
        actions = get_legal_moves(state,state.G,player)
        for a in actions:
            nextState = copy.deepcopy(state)
            apply_move(nextState,player,a)
            v2,a2 = self.maxValue(nextState,1-player,depth - 1)
            if v2 < v:
                v = v2
                move = a
        return (v,move)

# Registry of available strategies.
# Add your new strategies here to run them from main.py.
STRATEGIES = {
    "random": RandomStrategy,
    "greedy": GreedyMaxDegreeStrategy,
    "minmax": MinMaxStrategy
}
