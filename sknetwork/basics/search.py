#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jul 24, 2019
"""

import numpy as np
from scipy import sparse


def breadth_first_search(adjacency: sparse.csr_matrix, starting_node: int,
                         directed: bool = True, return_predecessors: bool = True):
    """Return a breadth-first ordering starting with specified node.

    Based on SciPy (scipy.sparse.csgraph.breadth_first_order)

    Parameters
    ----------
    adjacency:
        The adjacency matrix of the graph
    starting_node:
        The node from which to start the ordering
    directed:
        Denotes if the graph is directed
    return_predecessors:
        If ``True``, the size predecessor matrix is returned

    Returns
    -------
    node_array: np.ndarray
        The breadth-first list of nodes, starting with specified node. The length of node_array is the number of nodes
        reachable from the specified node.
    predecessors: np.ndarray
        Returned only if ``return_predecessors == True``. The list of predecessors of each node in a breadth-first tree.
        If node ``i`` is in the tree, then its parent is given by ``predecessors[i]``. If node ``i`` is not in the tree
        (and for the parent node) then ``predecessors[i] = -9999``.

    """
    return sparse.csgraph.breadth_first_order(adjacency, starting_node, directed, return_predecessors)


def depth_first_search(adjacency: sparse.csr_matrix, starting_node: int,
                       directed: bool = True, return_predecessors: bool = True):
    """Return a depth-first ordering starting with specified node.

    Based on SciPy (scipy.sparse.csgraph.depth_first_order)

    Parameters
    ----------
    adjacency:
        The adjacency matrix of the graph
    starting_node:
        The node from which to start the ordering
    directed:
        Denotes if the graph is directed
    return_predecessors:
        If ``True``, the size predecessor matrix is returned

    Returns
    -------
    node_array: np.ndarray
        The depth-first list of nodes, starting with specified node. The length of node_array is the number of nodes
        reachable from the specified node.
    predecessors: np.ndarray
        Returned only if ``return_predecessors == True``. The list of predecessors of each node in a depth-first tree.
        If node ``i`` is in the tree, then its parent is given by ``predecessors[i]``. If node ``i`` is not in the tree
        (and for the parent node) then ``predecessors[i] = -9999``.

    """
    return sparse.csgraph.depth_first_order(adjacency, starting_node, directed, return_predecessors)
