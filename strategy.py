from typing import List, Optional
from logic import GameState, Move

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
    # TODO: implement this class


class GreedyMaxDegreeStrategy(Strategy):
    """
    Pick the move that gives your endpoint the highest number of free neighbors after the move.

    Simple and explainable baseline.
    """
    # TODO: implement this class


# TODO: You should implement your own strategies here (Minimax, MCTS, etc.)

# Registry of available strategies.
# Add your new strategies here to run them from main.py.
STRATEGIES = {
    "random": RandomStrategy,
    "greedy": GreedyMaxDegreeStrategy,
}