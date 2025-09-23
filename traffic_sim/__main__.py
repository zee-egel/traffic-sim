import random
from traffic_sim.core.simulation import Simulation
from traffic_sim.control.fixed_cycle import FixedCyclePolicy
from traffic_sim.models.grid_world import build_world_from_grid
from traffic_sim.models.world import World
from traffic_sim.models.vehicle import Vehicle
from traffic_sim.ui.network_renderer import NetworkRenderer

# Simple four-way layout: a single central intersection with straight
# north/south and east/west approaches extending to the map edges. This keeps
# the rendering architecture intact while giving a minimal scene that's easier
# to parse.
GRID_STR = [
    "    |    ",
    "    |    ",
    "----+----",
    "    |    ",
    "    |    ",
]
GRID = [list(row) for row in GRID_STR]
CAR_KINDS = ["police","taxi","sports_blue","van","sports_yellow","ambulance","sedan_red","motor_blue","motor_red"]

def spawn_city(now_s: float, world: World):
    spawned = []
    # keep car count reasonable
    if sum(1 for v in world.vehicles if not v.finished) > 50:
        return spawned
    if random.random() < 0.25:
        # any entry road whose from_tile is on the border
        H, W = world._grid_size
        entries = [r for r in world.roads
                   if r.from_tile[0] in (0, H-1) or r.from_tile[1] in (0, W-1)]
        if entries:
            rd = random.choice(entries)
            kind = random.choice(CAR_KINDS)
            vid = len(world.vehicles) + 1
            car = Vehicle(id=vid, road=rd, pos_m=0.0, enter_time_s=now_s,
                          kind=kind, sprite_key=kind)
            car.target_speed *= random.uniform(0.9, 1.1)
            world.vehicles.append(car)
            spawned.append(car)
    return spawned

if __name__ == "__main__":
    random.seed(42)
    world = build_world_from_grid(GRID)
    policy = FixedCyclePolicy(green_ns=7, yellow_ns=2, green_ew=7, yellow_ew=2)
    renderer = NetworkRenderer(world)

    def render(_world, summary):
        renderer.frame(summary)

    sim = Simulation(world, policy, spawn_city, render_fn=render, dt=0.25, max_time=1e9)
    summary = sim.run()
    print("SUMMARY:", summary)
