"""Fixed cycle traffic signal policy."""
from __future__ import annotations

from typing import Tuple

from .policy_base import TrafficSignalPolicy


class FixedCyclePolicy(TrafficSignalPolicy):
    """Repeat a fixed NS/EW cycle with configurable green/yellow splits."""

    def __init__(
        self,
        green_ns: float = 8.0,
        yellow_ns: float = 2.0,
        green_ew: float = 8.0,
        yellow_ew: float = 2.0,
    ) -> None:
        self.green_ns = float(green_ns)
        self.yellow_ns = float(yellow_ns)
        self.green_ew = float(green_ew)
        self.yellow_ew = float(yellow_ew)
        self.cycle = self.green_ns + self.yellow_ns + self.green_ew + self.yellow_ew

    def decide(self, intersection, now_s: float) -> Tuple[str, str]:
        time_in_cycle = now_s % self.cycle

        if time_in_cycle < self.green_ns:
            return "NS", "GREEN"
        if time_in_cycle < self.green_ns + self.yellow_ns:
            return "NS", "YELLOW"
        if time_in_cycle < self.green_ns + self.yellow_ns + self.green_ew:
            return "EW", "GREEN"
        return "EW", "YELLOW"
