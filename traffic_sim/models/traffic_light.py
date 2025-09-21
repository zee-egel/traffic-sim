"""Traffic light state helpers."""
from __future__ import annotations

from dataclasses import dataclass

VALID_DIRECTIONS = {"NS", "EW"}
VALID_COLORS = {"GREEN", "YELLOW", "RED"}


@dataclass
class TrafficLight:
    direction: str = "NS"
    color: str = "RED"

    def set_state(self, direction: str, color: str) -> None:
        if direction not in VALID_DIRECTIONS:
            raise AssertionError(f"Invalid direction: {direction}")
        if color not in VALID_COLORS:
            raise AssertionError(f"Invalid color: {color}")
        self.direction = direction
        self.color = color

    def is_green_for(self, approach_dir: str) -> bool:
        if approach_dir not in VALID_DIRECTIONS:
            raise AssertionError(f"Invalid direction: {approach_dir}")
        return self.direction == approach_dir and self.color == "GREEN"

    def is_yellow_for(self, approach_dir: str) -> bool:
        if approach_dir not in VALID_DIRECTIONS:
            raise AssertionError(f"Invalid direction: {approach_dir}")
        return self.direction == approach_dir and self.color == "YELLOW"
