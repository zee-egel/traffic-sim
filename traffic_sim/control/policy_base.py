from abc import ABC, abstractmethod
from typing import Tuple

class TrafficSignalPolicy(ABC):
    @abstractmethod
    def decide(self, intersection, now_s: float) -> Tuple[str, str]:
        """Return (direction, color) with direction in {'NS','EW'} and color in {'GREEN','YELLOW','RED'}."""
        ...