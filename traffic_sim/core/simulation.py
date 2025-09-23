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
        render_fn: Optional[Callable[..., str]] = None,
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

        while self.clock.now() <= self.max_time:
            now_s = self.clock.now()

            # Apply signal policy at every node (supports phase offsets per node)
            for inter in self.world.intersections:
                inter.apply_policy(self.policy, now_s)

            # Spawn vehicles
            new_cars = self.spawn_fn(now_s, self.world) or []
            for _ in new_cars:
                self.metrics.on_enter()

            # Advance world state
            self.world.tick(self.dt)

            # Record exits
            for vehicle in list(self.world.vehicles):
                if vehicle.finished and vehicle.exit_time_s == 0.0:
                    vehicle.exit_time_s = now_s
                    self.metrics.on_exit(now_s, vehicle)

            # Optional render (accepts (world, summary) or just (world))
            if self.render_fn is not None:
                try:
                    frame = self.render_fn(self.world, self.metrics.summary())
                except TypeError:
                    frame = self.render_fn(self.world)
                if frame:
                    print(frame)

            self.clock.tick()

        return self.metrics.summary()