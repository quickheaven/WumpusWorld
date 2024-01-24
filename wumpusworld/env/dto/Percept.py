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

    @property
    def is_terminated(self):
        return self._is_terminated

    @property
    def reward(self):
        return self._reward