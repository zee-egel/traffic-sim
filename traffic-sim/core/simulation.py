from typing import Callable, Optional

from .timekeeper import SimClock
from ..metrics.collectors import Metrics


class Simulation:
    """Main simulation loop for the traffic sim.

    Responsibilities
    - Advance the simulation clock in fixed time steps
    - Apply the traffic-signal policy to intersections
    - Spawn vehicles (via user-provided spawn_fn)
    - Step the world forward (vehicle motion, etc.)
    - Record exits and compute simple metrics
    - Optionally render an ASCII frame each tick
    """

    def __init__(
        self,
        world,
        policy,
        spawn_fn: Callable,  # (now_s: float, world) -> list[new_vehicles]
        render_fn: Optional[Callable] = None,  # (world) -> str
        dt: float = 1.0,
        max_time: float = 120.0,
        clock: Optional[SimClock] = None,
    ) -> None:
        self.world = world
        self.policy = policy
        self.spawn_fn = spawn_fn
        self.render_fn = render_fn
        self.clock = clock or SimClock(dt=dt)
        self.max_time = max_time
        self.metrics = Metrics()

    def run(self):
        # For the prototype we assume a single intersection world
        if not self.world.intersections:
            raise ValueError("World must contain at least one intersection")
        inter = self.world.intersections[0]

        # Main loop
        while self.clock.now() <= self.max_time:
            now_s = self.clock.now()

            # 1) Signal control policy decides the current phase/state
            inter.apply_policy(self.policy, now_s)

            # 2) Spawn new vehicles for this tick
            new_cars = self.spawn_fn(now_s, self.world) or []
            for _ in new_cars:
                self.metrics.on_enter()

            # 3) Advance world state by dt (vehicles move, etc.)
            self.world.tick(self.clock.step.dt)

            # 4) Record vehicles that have completed their road
            for v in list(self.world.vehicles):
                if v.finished and v.exit_time_s == 0.0:
                    v.exit_time_s = now_s
                    self.metrics.on_exit(now_s, v)

            # 5) Optional render
            if self.render_fn:
                frame = self.render_fn(self.world)
                if frame:
                    print(frame)

            # Advance time
            self.clock.tick()

        return self.metrics.summary()