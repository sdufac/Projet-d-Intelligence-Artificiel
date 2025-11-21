from typing import Dict, Set, List
import random

# This file as well as strategy.py should be the only ones you have to edit!


def make_empty_graph(n: int) -> Dict[int, Set[int]]:
    """
    Create an empty graph with n nodes.

    :param n: (int) Number of nodes.
    :return: (Dict[int, Set[int]]) An empty graph with n nodes.
    """
    return {i: set() for i in range(n)}


def add_edge(G: Dict[int, Set[int]], u: int, v: int):
    """
    Add an edge to the graph.

    :param G: (Dict[int, Set[int]]) Adjacency dictionary representing the graph.
    :param u: (int) Node ID.
    :param v: (int) Node ID.
    :return: (None)
    """
    G[u].add(v)
    G[v].add(u)


def random_erdos_renyi(n: int, p: float, seed: int = None):
    """
    Create a random Erdos-Renyi graph with n nodes and edge probability p.

    :param n: (int) Number of nodes.
    :param p: (float) Probability of edge creation.
    :param seed: (int) Optional seed for random number generator.
    :return: (Dict[int, Set[int]]) An Erdos-Renyi graph with n nodes and edge probability p.
    """
    rnd = random.Random(seed)
    G = make_empty_graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            if rnd.random() < p:
                add_edge(G, i, j)
    return G


def random_regular(n: int, d: int, seed: int = None):
    """
    Create a random regular graph with n nodes and degree d.

    :param n: (int) Number of nodes.
    :param d: (int) Degree of the graph.
    :param seed: (int) Optional seed for random number generator.
    :return: (Dict[int, Set[int]]) A random regular graph with n nodes and degree d.
    """

    # simple configuration model with rejection (works for small sizes in teaching)
    # This should not be used for large graphs!
    # In general, prefer using random_erdos_renyi()
    rnd = random.Random(seed)
    if d >= n:
        raise ValueError('d must be < n')
    if (n * d) % 2 != 0:
        raise ValueError('n*d must be even')
    while True:
        stubs = []
        for i in range(n):
            stubs.extend([i] * d)
        rnd.shuffle(stubs)
        G = make_empty_graph(n)
        ok = True
        while stubs:
            a = stubs.pop()
            b = stubs.pop()
            if a == b or b in G[a]:
                ok = False
                break
            add_edge(G, a, b)
        if ok:
            return G


def hypercube(d: int):
    """
    Create a hypercube graph with d dimensions.
    This should be the preferred way of playing the game, as the generated graphs are symetric,
    thus ensuring that the game is always playable from any starting position.

    :param d: (int) Number of dimensions.
    :return: (Dict[int, Set[int]]) A hypercube graph with d dimensions.
    """
    n = 1 << d
    G = make_empty_graph(n)
    for x in range(n):
        for i in range(d):
            y = x ^ (1 << i)
            add_edge(G, x, y)
    return G


def pick_random_start(G, seed: int = None):
    """
    Pick two distinct random starting nodes from the graph.
    Feel free to change this function (or better, to add a new one) to pick your own starting points!

    :param G: (Dict[int, Set[int]]) Adjacency dictionary representing the graph.
    :param seed: (int) Optional seed for random number generator.
    :return: (int, int) Two distinct random starting nodes.
    """
    import random as _r
    rnd = _r.Random(seed)
    nodes = list(G.keys())
    a = rnd.choice(nodes)
    b = rnd.choice(nodes)
    while b == a:
        b = rnd.choice(nodes)
    return a, b

def num_vertices(G: dict) -> int:
    """
    Return the number of vertices in the graph.

    :param G: (dict) Adjacency dictionary representing the graph.
    :return: (int) Number of vertices.
    """
    return len(G)


def num_edges(G: dict) -> int:
    """
    Return the number of edges in the graph.

    :param G: (dict) Adjacency dictionary representing the graph.
    :return: (int) Number of edges.
    """
    counted = set()
    count = 0
    for u, neighbors in G.items():
        for v in neighbors:
            # Count each edge only once
            if (v, u) not in counted:
                counted.add((u, v))
                count += 1
    return count