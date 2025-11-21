import argparse
from utils import random_erdos_renyi, hypercube, pick_random_start, num_vertices
from game import Game
from ui import interactive_view
from strategy import STRATEGIES

# Feel free to edit this file and to add new ones!

def parse_args():
    ap = argparse.ArgumentParser(description="Snake-in-the-Box Game Runner")
    ap.add_argument("--graph", type=str, default="erdos", choices=["erdos", "cube"], help="Graph type")
    ap.add_argument("--n", type=int, default=30, help="Graph size (Erdos-Renyi)")
    ap.add_argument("--p", type=float, default=0.08, help="Edge probability (Erdos-Renyi)")
    ap.add_argument("--d", type=int, default=5, help="Dimension for hypercube")
    ap.add_argument("--s0", type=str, default="random", help="Strategy for player 0")
    ap.add_argument("--s1", type=str, default="random", help="Strategy for player 1")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for start positions")
    ap.add_argument("--verbose", action="store_true", help="Print moves")
    ap.add_argument("--ui", action="store_true", help="Run using the graphical UI instead of strategies")
    return ap.parse_args()

def build_graph(args):
    if args.graph == "erdos":
        return random_erdos_renyi(args.n, args.p, seed=args.seed)
    elif args.graph == "cube":
        return hypercube(args.d)

def run():
    args = parse_args()
    G = build_graph(args)
    a, b = pick_random_start(G, seed=args.seed)

    # UI mode
    if getattr(args, 'ui', False):
        if num_vertices(G) > 50:
            print("UI mode is not supported for large graphs. Falling back to normal mode.")
        else:
            print("Launching UI mode…")
            interactive_view(G, a, b, pause=0.7)
            return

    # Strategy mode
    s0 = STRATEGIES[args.s0]()
    s1 = STRATEGIES[args.s1]()

    game = Game(G, a, b)
    winner = game.play_game(s0, s1, verbose=args.verbose)
    print("Winner:", winner)

if __name__ == '__main__':
    run()
