#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on November 12 2019
@author: Quentin Lutz <qlutz@enst.fr>
"""
from math import log
from typing import Union, Optional

import numpy as np
from scipy import sparse

from sknetwork.basics import shortest_path, is_connected
from sknetwork.ranking.base import BaseRanking
from sknetwork.utils.checks import check_format, is_square


class Closeness(BaseRanking):
    """
    Compute the closeness centrality of each node in a connected graph, corresponding to the average length of the
    shortest paths from that node to all the other ones.

    For a directed graph, the closeness centrality is computed in terms of outgoing paths.

    Parameters
    ----------
    method :
        Denotes if the results should be exact or approximate.
    tol:
        If ``method=='approximate'``, the allowed tolerance on each score entry.
    n_jobs:
        If an integer value is given, denotes the number of workers to use (-1 means the maximum number will be used).
        If ``None``, no parallel computations are made.

    Attributes
    ----------
    scores_ : np.ndarray
        Closeness centrality of each node.

    Example
    -------
    >>> from sknetwork.data import rock_paper_scissors
    >>> closeness = Closeness()
    >>> adjacency = rock_paper_scissors()
    >>> np.round(closeness.fit(adjacency).scores_, 2)
    array([0.67, 0.67, 0.67])

    References
    ----------
    Eppstein, D., & Wang, J. (2001, January).
    `Fast approximation of centrality.
    <http://jgaa.info/accepted/2004/EppsteinWang2004.8.1.pdf>`_
    In Proceedings of the twelfth annual ACM-SIAM symposium on Discrete algorithms (pp. 228-229).
    Society for Industrial and Applied Mathematics.
    """

    def __init__(self, method: str = 'exact', tol: float = 1e-1, n_jobs: Optional[int] = None):
        super(Closeness, self).__init__()

        self.method = method
        self.tol = tol
        self.n_jobs = n_jobs

    def fit(self, adjacency: Union[sparse.csr_matrix, np.ndarray]) -> 'Closeness':
        """
        Closeness centrality for connected graphs.

        Parameters
        ----------
        adjacency :
            Adjacency matrix of the graph.

        Returns
        -------
        self: :class:`Closeness`
        """
        adjacency = check_format(adjacency)
        n = adjacency.shape[0]
        if not is_square(adjacency):
            raise ValueError("The adjacency is not square. Please use 'bipartite2undirected' or "
                             "'bipartite2directed'.")

        if not is_connected(adjacency):
            raise ValueError("The graph must be connected.")

        if self.method == 'exact':
            nb_samples = n
            indices = np.arange(n)
        elif self.method == 'approximate':
            nb_samples = min(int(log(n) / self.tol ** 2), n)
            indices = np.random.choice(np.arange(n), nb_samples, replace=False)
        else:
            raise ValueError("Method should be either 'exact' or 'approximate'.")

        paths = shortest_path(adjacency, n_jobs=self.n_jobs, indices=indices)

        self.scores_ = ((n - 1) * nb_samples / n) / paths.T.dot(np.ones(nb_samples))

        return self
