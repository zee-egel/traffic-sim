"""Simple road model."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Road:
    name: str
    length_m: float
    speed_mps: float
    to_intersection: "Intersection | None" = None
    approach_dir: str = "NS"

    def clamp_pos(self, pos_m: float) -> float:
        """Clamp a position to the road bounds."""
        if pos_m < 0.0:
            return 0.0
        if pos_m > self.length_m:
            return self.length_m
        return pos_m


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .intersection import Intersection
