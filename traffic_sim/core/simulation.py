"""Main simulation loop implementation."""
from __future__ import annotations

from typing import Callable, Optional

from .timekeeper import SimClock
from ..metrics.collectors import Metrics


class Simulation:
    """Coordinates the policy, world state, spawning, and rendering."""

    def __init__(
        self,
        world,
        policy,
        spawn_fn: Callable[[float, object], list] | None,
        render_fn: Optional[Callable[[object], str]] = None,
        dt: float = 1.0,
        max_time: float = 120.0,
        clock: Optional[SimClock] = None,
    ) -> None:
        self.world = world
        self.policy = policy
        self.spawn_fn = spawn_fn or (lambda now_s, world: [])
        self.render_fn = render_fn
        self.dt = dt
        self.clock = clock or SimClock(dt=dt)
        self.max_time = max_time
        self.metrics = Metrics()

    def run(self) -> dict:
        if not self.world.intersections:
            raise ValueError("World must contain at least one intersection")
        intersection = self.world.intersections[0]

        while self.clock.now() <= self.max_time:
            now_s = self.clock.now()

            intersection.apply_policy(self.policy, now_s)

            new_cars = self.spawn_fn(now_s, self.world) or []
            for _ in new_cars:
                self.metrics.on_enter()

            self.world.tick(self.dt)

            for vehicle in self.world.vehicles:
                if vehicle.finished and vehicle.exit_time_s == 0.0:
                    vehicle.exit_time_s = now_s
                    self.metrics.on_exit(now_s, vehicle)

            if self.render_fn is not None:
                frame = self.render_fn(self.world)
                if frame:
                    print(frame)

            self.clock.tick()

        return self.metrics.summary()
