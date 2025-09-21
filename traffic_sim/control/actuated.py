"""Simple demand-actuated signal policy."""
from __future__ import annotations

from typing import Tuple

from .policy_base import TrafficSignalPolicy


class ActuatedPolicy(TrafficSignalPolicy):
    """Queue-detection-based signal switching with min/max green times."""

    def __init__(
        self,
        min_green: float = 6.0,
        max_green: float = 20.0,
        yellow: float = 2.0,
        queue_window_m: float = 25.0,
    ) -> None:
        self.min_green = float(min_green)
        self.max_green = float(max_green)
        self.yellow = float(yellow)
        self.queue_window_m = float(queue_window_m)
        self.current_direction = "NS"
        self.phase_start = 0.0
        self.current_color = "GREEN"

    def decide(self, intersection, now_s: float) -> Tuple[str, str]:
        time_in_phase = now_s - self.phase_start

        if self.current_color == "GREEN":
            if time_in_phase >= self.max_green:
                self._switch_to_yellow(now_s)
            elif time_in_phase >= self.min_green and not self._has_queue(intersection, self.current_direction):
                self._switch_to_yellow(now_s)

        elif self.current_color == "YELLOW":
            if time_in_phase >= self.yellow:
                self._switch_to_other_green(now_s)

        return self.current_direction, self.current_color

    def _switch_to_yellow(self, now_s: float) -> None:
        self.current_color = "YELLOW"
        self.phase_start = now_s

    def _switch_to_other_green(self, now_s: float) -> None:
        self.current_direction = "EW" if self.current_direction == "NS" else "NS"
        self.current_color = "GREEN"
        self.phase_start = now_s

    def _has_queue(self, intersection, direction: str) -> bool:
        for vehicle in intersection.vehicles_for(direction):
            distance_to_stop = vehicle.road.length_m - vehicle.pos_m
            if distance_to_stop <= self.queue_window_m:
                return True
        return False
