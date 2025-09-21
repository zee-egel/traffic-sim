"""CLI entry point for the traffic simulation demo."""
from __future__ import annotations

import random
from itertools import count

from .control.fixed_cycle import FixedCyclePolicy
from .core.simulation import Simulation
from .models.intersection import Intersection
from .models.road import Road
from .models.vehicle import Vehicle
from .models.world import World
from .ui.ascii import draw


def build_demo_world() -> World:
    world = World()
    intersection = Intersection("X1")
    world.add_intersection(intersection)

    road_ns = Road(name="North-South", length_m=120.0, speed_mps=10.0, to_intersection=intersection, approach_dir="NS")
    road_ew = Road(name="East-West", length_m=120.0, speed_mps=10.0, to_intersection=intersection, approach_dir="EW")

    world.add_road(road_ns)
    world.add_road(road_ew)

    return world


def make_spawn_fn():
    id_counter = count(1)

    def spawn(now_s: float, world: World):
        new_cars = []
        for road in world.roads:
            if random.random() < 0.15:
                vehicle_id = f"{road.name}-{next(id_counter)}"
                car = Vehicle(id=vehicle_id, road=road, pos_m=0.0, enter_time_s=now_s)
                world.add_vehicle(car)
                new_cars.append(car)
        return new_cars

    return spawn


def main() -> None:
    random.seed(42)

    world = build_demo_world()
    policy = FixedCyclePolicy(green_ns=8.0, yellow_ns=2.0, green_ew=8.0, yellow_ew=2.0)
    spawn_fn = make_spawn_fn()

    sim = Simulation(
        world=world,
        policy=policy,
        spawn_fn=spawn_fn,
        render_fn=draw,
        dt=1.0,
        max_time=60.0,
    )
    summary = sim.run()
    print("SUMMARY:", summary)


if __name__ == "__main__":  # pragma: no cover
    main()
