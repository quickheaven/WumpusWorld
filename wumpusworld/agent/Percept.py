from __future__ import annotations


class Percept:

    def __init__(self, stench: bool, breeze: bool, glitter: bool, bump: bool, scream: bool, is_terminated: bool,
                 reward: float):
        self._stench = stench
        self._breeze = breeze
        self._glitter = glitter
        self._bump = bump
        self._scream = scream
        self._is_terminated = is_terminated
        self._reward = reward

    def __str__(self):
        return ('PERCEPTION Stench: {}, Breeze: {}, Glitter: {}, Bump: {}, Scream: {}, Is_Terminated: {}, Reward: {}'
                .format(self._stench, self._breeze, self._glitter, self._bump, self._scream, self._is_terminated,
                        self._reward))

    @property
    def is_terminated(self):
        return self._is_terminated

    @property
    def reward(self):
        return self._reward

    @property
    def glitter(self):
        return self._glitter

    @property
    def breeze(self):
        return self._breeze

    @property
    def stench(self):
        return self._stench

    @property
    def scream(self):
        return self._scream

    @property
    def bump(self):
        return self._bump
