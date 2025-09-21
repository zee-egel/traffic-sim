import random
from typing import List
from traffic_sim.core.simulation import Simulation
from traffic_sim.control.fixed_cycle import FixedCyclePolicy
from traffic_sim.ui.pygame_tiles import PygameTilesRenderer
from traffic_sim.ui.tilecodes import TILES
from traffic_sim.models.grid_world import build_world_from_grid
from traffic_sim.models.vehicle import Vehicle
from traffic_sim.models.world import World

# Simple 16x10 map. ' ' = empty; use '-', '|', '+', 'L', 'T' etc.
GRID_STR = [
    "    ----+-----    ",
    "    |   |     |   ",
    "----+---+-----+---",
    "    |         |   ",
    "    +----+----+   ",
    "    |    |        ",
    "----+----+----    ",
    "    |         |   ",
    "    +---------+   ",
    "                  ",
]
# Convert to 2D list of chars
GRID = [list(row) for row in GRID_STR]

def road_tiles(grid: List[List[str]]):
    coords = []
    for r,row in enumerate(grid):
        for c,ch in enumerate(row):
            if ch != " ":
                coords.append((r,c))
    return coords

import random
# ...

CAR_KINDS = [
    "police","taxi","sports_blue","van",
    "sports_yellow","ambulance","sedan_red","motor_blue","motor_red"
]

def simple_spawn(now_s: float, world: World):
    spawned = []
    if random.random() < 0.15:
        left_edge_roads = [r for r in world.roads if getattr(r, "from_tile", (0,0))[1] == 0]
        if left_edge_roads:
            rd = random.choice(left_edge_roads)
            kind = random.choice(CAR_KINDS)
            vid = len(world.vehicles) + 1
            car = Vehicle(id=vid, road=rd, pos_m=0.0, enter_time_s=now_s,
                          kind=kind, sprite_key=kind)
            # optional: color diversity by slight speed jitter
            car.target_speed *= random.uniform(0.9, 1.1)
            world.vehicles.append(car)
            spawned.append(car)
    return spawned

if __name__ == "__main__":
    random.seed(42)
    world, nodes = build_world_from_grid(GRID)
    policy = FixedCyclePolicy(green_ns=6, yellow_ns=2, green_ew=6, yellow_ew=2)

    # Render with tile atlas (put your PNG here)
    renderer = PygameTilesRenderer(world, GRID, TILES, sheet_path="assets/tiles/roads_2w.png")

    def render(_w):
        renderer.render_frame()

    # Temporary: simple spawner that pushes cars onto any horizontal road heading east
    def simple_spawn(now_s: float, world: World):
        spawned = []
        if random.random() < 0.15:
            # find a road on the left edge to go right
            left_edge_roads = [r for r in world.roads if getattr(r, "from_tile", (0,0))[1] == 0]
            if left_edge_roads:
                rd = random.choice(left_edge_roads)
                vid = len(world.vehicles) + 1
                car = Vehicle(id=vid, road=rd, pos_m=0.0, enter_time_s=now_s)
                car.route = [rd]  # you can compute full BFS route and assign here
                world.vehicles.append(car)
                spawned.append(car)
        return spawned

    sim = Simulation(world, policy, simple_spawn, render_fn=render, dt=0.25, max_time=120)
    summary = sim.run()
    print("SUMMARY:", summary)