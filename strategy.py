from logging import info
from math import inf
import math
from time import process_time_ns
from typing import List, Optional
from logic import GameState, Move, apply_move
from utils import num_degree,freeNeighbor
import random
import sys
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
        print(f'Move retourné : {move}')
        return move

    def maxValue(self,state :GameState,player :int, depth: int) -> tuple[int,Move | None]:
        legal_move = get_legal_moves(state,state.G,player)
        if not legal_move: 
            return (-sys.maxsize -1,None)
        elif depth == 0:
            sommetPlayer = state.endpoints[player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,player,state),None)

        v = -inf
        move = None
        for a in legal_move:
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
            return (sys.maxsize,None)
        elif depth == 0:
            sommetPlayer = state.endpoints[1 - player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,1 - player,state),None)
        
        v = inf
        move = None
        for a in legal_move:
            nextState = copy.deepcopy(state)
            apply_move(nextState,player,a)
            v2,a2 = self.maxValue(nextState,1-player,depth - 1)
            if v2 < v:
                v = v2
                move = a
        return (v,move)

class AlphaBetaStrategy(Strategy):

    # def min_max_search(self, state: GameState,player : int)
    def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
        depth = 4

        move = None
        (value,move) = self.maxValue(state,player, depth,-inf,inf)
        print(f'Move retourné : {move}')
        return move

    def maxValue(self,state :GameState,player :int, depth: int, α, β) -> tuple[int,Move | None]:
        legal_move = get_legal_moves(state,state.G,player)
        if not legal_move: 
            return (-sys.maxsize -1,None)
        elif depth == 0:
            sommetPlayer = state.endpoints[player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,player,state),None)

        v = -inf
        move = None
        for a in legal_move:
            nextState = copy.deepcopy(state)
            apply_move(nextState,player,a)
            v2,a2 = self.minValue(nextState,1-player,depth - 1,α,β)
            if v2 > v:
                v = v2
                move = a
                if v > α:
                    α = v
            if v >= β:
                return (v,move)

        return (v,move)

    def minValue(self,state:GameState,player :int, depth:int, α, β)-> tuple[int,Move | None]:
        legal_move = get_legal_moves(state,state.G,player)
        if not legal_move: 
            return (sys.maxsize,None)
        elif depth == 0:
            sommetPlayer = state.endpoints[1 - player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,1 - player,state),None)
        
        v = inf
        move = None
        for a in legal_move:
            nextState = copy.deepcopy(state)
            apply_move(nextState,player,a)
            v2,a2 = self.maxValue(nextState,1-player,depth - 1,α,β)
            if v2 < v:
                v = v2
                move = a

                if v<β:
                    β = v
            if v <= α:
                return (v,move)

        return (v,move)

class MCTSNode:
    def __init__(self, state: GameState, parent=None, move= None, player_to_move=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.player_to_move = player_to_move
        self.children = []
        self.wins = 0
        self.visits = 0

        self.untried_moves = get_legal_moves(state, state.G, player_to_move)
class MonteCarloTreeSearchStrategy(Strategy):
        '''
        Réalisation avec l'aide de Gemini
        '''
        def select_move(self, state: GameState, G: Dict[int, Set[int]], player: int) -> Optional[Move]:
            iter = 1000
            start = MCTSNode(state=state, parent=None, move=None, player_to_move=player)

            if not start.untried_moves:
                return None
            
            for _ in range(iter):
                node = self.selection(start, player)
                node = self.expansion(node, player)
                winner = self.simulation(node.state, node.player_to_move)
                self.backpropagation(node, winner, player)

            if not start.children:
                return None
            
            # On prend l'enfant avec le plus de visites 
            best_child = max(start.children, key=lambda c: c.visits)
            return best_child.move
        
        def selection(self, node: MCTSNode, player: int) -> MCTSNode:
            # tant que enfant et pas de coup non essayé
            while node.children and not node.untried_moves:
                node = self.get_best_child(node, player)
            return node
        
        def get_best_child(self, node: MCTSNode, player: int) -> MCTSNode:

            best_score = -float('inf')
            best_child = None

            for child in node.children:
                #UCB1(i) = winrate + C * sqrt(ln(N) / n)
                score = (child.wins / child.visits) + math.sqrt(2) * math.sqrt(math.log(node.visits) / child.visits)
                
                # choix du meilleur enfant
                if score > best_score:
                    best_score = score
                    best_child = child
            return best_child
        
        def expansion(self, node: MCTSNode, player: int) -> MCTSNode:

            if not node.untried_moves:
                return node 
            
            # on choisit un coup non encore essayé
            move = node.untried_moves.pop()
            new_state = copy.deepcopy(node.state)

            apply_move(new_state, node.player_to_move, move)

            next_player = 1 - node.player_to_move
            child_node = MCTSNode(state=new_state, parent=node, move=move, player_to_move=next_player)
            node.children.append(child_node)
            return child_node

        
        def simulation(self, state: GameState, player: int) -> int:
            
            current_state = copy.deepcopy(state)
            current_player = player

            while True:
                legal_moves = get_legal_moves(current_state, current_state.G, current_player)
                
                if not legal_moves:
                    return 1 - current_player  # L'autre joueur a gagné

                move = random.choice(legal_moves)
                apply_move(current_state, current_player, move)
                current_player = 1 - current_player
        
        def backpropagation(self, node: MCTSNode, winner: int, player: int):
            while node is not None:
                node.visits += 1
                
                player_moved = 1 - node.player_to_move

                if winner == player_moved:
                    node.wins += 1

                node = node.parent

# Registry of available strategies.
# Add your new strategies here to run them from main.py.
STRATEGIES = {
    "random": RandomStrategy,
    "greedy": GreedyMaxDegreeStrategy,
    "minmax": MinMaxStrategy,
    "mcts": MonteCarloTreeSearchStrategy,
    "alphabeta": AlphaBetaStrategy
}
