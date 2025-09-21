"""Time management helpers for the traffic simulation."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeStep:
    """Immutable container describing the fixed step size."""

    dt: float


class SimClock:
    """Simple fixed-step simulation clock."""

    def __init__(self, dt: float = 1.0) -> None:
        self.step = TimeStep(dt=dt)
        self._t = 0.0

    def tick(self) -> None:
        """Advance the clock by one time step."""
        self._t += self.step.dt

    def now(self) -> float:
        """Return the current simulation time in seconds."""
        return self._t
