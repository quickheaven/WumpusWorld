from abc import abstractmethod
from typing import Self


class Orientation:

    @abstractmethod
    def turn_left(self) -> Self:
        pass

    @abstractmethod
    def turn_right(self) -> Self:
        pass
