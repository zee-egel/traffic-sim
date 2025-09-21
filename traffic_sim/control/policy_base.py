"""Base interface for traffic signal control policies."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple


class TrafficSignalPolicy(ABC):
    """Interface that all signal controllers must implement."""

    @abstractmethod
    def decide(self, intersection, now_s: float) -> Tuple[str, str]:
        """Return the direction and color to display at *now_s*.

        The returned direction must be either ``"NS"`` or ``"EW"`` and the
        color must be one of ``"GREEN"``, ``"YELLOW"``, or ``"RED"``.
        """

