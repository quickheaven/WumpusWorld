from pomegranate.distributions import Categorical

"""
Copied from sample code provided.
"""
class Predicate():
    def __init__(self, prob: float):
        self.p = prob

    def toList(self):
        return [1 - self.p, self.p]

    def toCategorical(self):
        return Categorical([self.toList()])
