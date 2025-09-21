"""Simple metrics collectors for the simulation."""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean


@dataclass
class Metrics:
    entered: int = 0
    exited: int = 0
    completed_times: list[float] = field(default_factory=list)

    def on_enter(self) -> None:
        self.entered += 1

    def on_exit(self, now_s: float, vehicle) -> None:
        self.exited += 1
        travel_time = now_s - vehicle.enter_time_s
        self.completed_times.append(travel_time)

    def summary(self) -> dict:
        avg = mean(self.completed_times) if self.completed_times else 0.0
        return {
            "entered": self.entered,
            "exited": self.exited,
            "avg_travel_time_s": round(avg, 2),
        }
