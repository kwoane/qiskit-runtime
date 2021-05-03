# This code is part of mthree.
#
# (C) Copyright IBM Quantum 2021.
#
# This code is for internal IBM Quantum use only.
# pylint: disable=no-name-in-module
"""mthree classes"""

from math import sqrt
from .probability import ProbDistribution


class QuasiDistribution(dict):
    """A dict-like class for representing qasi-probabilities.
    """
    def __init__(self, data, shots=None):
        """Builds a quasiprobability distribution object.

        Parameters:
            data (dict): Input quasiprobability data.
            shots (int): Number of shots the distribution was derived from.
        """
        self.shots = shots
        super().__init__(data)

    def nearest_probability_distribution(self, return_distance=False):
        """Takes a quasiprobability distribution and maps
        it to the closest probability distribution as defined by
        the L2-norm.

        Parameters:
            return_distance (bool): Return the L2 distance between distributions.

        Returns:
            ProbDistribution: Nearest probability distribution.
            float: Euclidean (L2) distance of distributions.

        Notes:
            Method from Smolin et al., Phys. Rev. Lett. 108, 070502 (2012).
        """
        probs, dist = quasi_to_probs(self)
        if return_distance:
            return probs, dist
        return probs


def quasi_to_probs(quasiprobs):
    """Takes a quasiprobability distribution and maps
    it to the closest probability distribution as defined by
    the L2-norm.

    Parameters:
        quasiprobs (QuasiDistribution): Input quasiprobabilities.

    Returns:
        dict: Nearest probability distribution
        float: Distance between distributions

    Notes:
        Method from Smolin et al., Phys. Rev. Lett. 108, 070502 (2012).
    """
    sorted_probs = dict(sorted(quasiprobs.items(), key=lambda item: item[1]))
    num_elems = len(sorted_probs)
    new_probs = {}
    beta = 0
    for key, val in sorted_probs.items():
        temp = val+beta/num_elems
        if temp < 0:
            beta += val
            num_elems -= 1
            diff += val*val
        else:
            diff += (beta/num_elems)*(beta/num_elems)
            new_probs[key] = sorted_probs[key] + beta/num_elems
    return ProbDistribution(new_probs, quasiprobs.shots), sqrt(diff)
