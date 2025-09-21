"""Vehicle dynamics for the simplified traffic simulation."""
from __future__ import annotations

from dataclasses import dataclass

from .road import Road


@dataclass
class Vehicle:
    id: str
    road: Road
    pos_m: float = 0.0
    length_m: float = 4.5
    max_accel: float = 2.0
    max_decel: float = 4.5
    target_speed: float | None = None
    finished: bool = False
    enter_time_s: float = 0.0
    exit_time_s: float = 0.0

    def __post_init__(self) -> None:
        if self.target_speed is None:
            self.target_speed = self.road.speed_mps

    def update(self, dt: float, intersection) -> None:
        if self.finished:
            return

        stop_line = self.road.length_m - 2.0
        is_green = intersection.signal.is_green_for(self.road.approach_dir)

        if self.pos_m >= stop_line and not is_green:
            # wait at the stop line until green
            return

        move = (self.target_speed or 0.0) * dt
        self.pos_m = self.road.clamp_pos(self.pos_m + move)

        if self.pos_m >= self.road.length_m:
            self.finished = True
