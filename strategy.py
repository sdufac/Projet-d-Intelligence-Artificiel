from logging import info
from math import inf
from typing import List, Optional
from logic import GameState, Move
from utils import num_degree,freeNeighbor
import random
from game import Game
import copy
from logic import _check_induced_path_property

# This file as well as utils.py should be the only ones you have to edit!

class Strategy:
    """
    Base strategy class. Students should subclass this and implement select_move,
    as well as any helper methods they need.
    """
    def select_move(self, state: GameState, player: int, legal_moves: List[Move]) -> Optional[Move]:
        """
        Select a move for the given player in the given state.

        :param state: (GameState) The current game state.
        :param player: (int) The ID of the current player, 0 or 1.
        :param legal_moves: (List[Move]) A list of legal moves available to the given player.
        :return: (Optional[Move]) The selected move, or None to forfeit.
        """
        raise NotImplementedError
    


class RandomStrategy(Strategy):
    """
    Pick a random legal move.
    """
    def select_move(self, state : GameState, player : int , legal_moves : list[Move]):
        if legal_moves:
            return random.choice(legal_moves)
        else:
            return None




class GreedyMaxDegreeStrategy(Strategy):
    """
    Pick the move that gives your endpoint the highest number of free neighbors after the move.

    Simple and explainable baseline.
    """
    def select_move(self, state : GameState, player : int , legal_moves : list[Move]):
        bestMove: Move = None
        bestMoveD: int = -1
        for move in legal_moves:
            currentD = freeNeighbor(state.G,move.to_node,state)
            if  currentD > bestMoveD:
                bestMove = move
                bestMoveD =  currentD

        return bestMove

# TODO: You should implement your own strategies here (Minimax, MCTS, etc.)

class MinMaxStrategy(Strategy):
    # def min_max_search(self, state: GameState,player : int)

    def __init__(self,game:Game,playerToMax:int):
        super().__init__()
        self.game: Game = copy.deepcopy(game)
        self.playerMax = playerToMax
        self.playerMin = 1 - playerToMax

    def select_move(self, state : GameState,player:int, legal_moves : list[Move]) -> Move:
        # TODO
        (value,move) = self.maxValue(self.game,state,0)
        assert move is not None
        return move

    def maxValue(self,game :Game,state :GameState,player :int) -> tuple[int,Move | None]:
        if not _check_induced_path_property(state.occupied,state.G): 
            sommetPlayer = state.endpoints[player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,sommetPlayer,state),None)
        
        v = 999999
        move = None
        actions = game.legal_moves(player)
        for a in actions:
            v2,a2 = self.minValue(game,state,1-player)
            if v2 < v:
                v = v2
                move = a2
        return (v,move)



    def minValue(self,game:Game,state:GameState,player :int)-> tuple[int,Move | None]:
        if not _check_induced_path_property(state.occupied,state.G): 
            sommetPlayer = state.endpoints[player]
            assert sommetPlayer is not None
            return (freeNeighbor(state.G,sommetPlayer,state),None)
        
        v = -999999
        move = None
        actions = game.legal_moves(player)
        for a in actions:
            v2,a2 = self.maxValue(game,state,1 - player)
            if v2 > v:
                v = v2
                move = a2
        return (v,move)



    

# Registry of available strategies.
# Add your new strategies here to run them from main.py.
STRATEGIES = {
    "random": RandomStrategy,
    "greedy": GreedyMaxDegreeStrategy,
    "minmax": MinMaxStrategy
}
