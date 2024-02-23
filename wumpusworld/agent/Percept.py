from __future__ import annotations


class Percept:

    def __init__(self, stench: bool, breeze: bool, glitter: bool, bump: bool, scream: bool, is_terminated: bool,
                 reward: float):
        self._stench = stench
        self._breeze = breeze
        self._glitter = glitter
        self._bump = bump
        self._screem = scream
        self._is_terminated = is_terminated
        self._reward = reward

    def __str__(self):
        return ('PERCEPTION Stench: {}, Breeze: {}, Glitter: {}, Bump: {}, Scream: {}, Is_Terminated: {}, Reward: {}'
                .format(self._stench, self._breeze, self._glitter, self._bump, self._screem, self._is_terminated,
                        self._reward))

    def is_terminated(self):
        return self._is_terminated

    def reward(self):
        return self._reward

    def glitter(self):
        return self._glitter
