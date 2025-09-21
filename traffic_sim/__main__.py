import random
from traffic_sim.models.world import World
from traffic_sim.models.road import Road
from traffic_sim.models.intersection import Intersection
from traffic_sim.models.vehicle import Vehicle
from traffic_sim.core.simulation import Simulation
from traffic_sim.control.fixed_cycle import FixedCyclePolicy
from traffic_sim.ui.pygame_renderer import PygameRenderer

def build_demo_world():
    inter = Intersection(name="X1")
    road_ns = Road(name="North→South", length_m=120.0, speed_mps=10.0, to_intersection=inter, approach_dir="NS")
    road_ew = Road(name="East→West",   length_m=120.0, speed_mps=10.0, to_intersection=inter, approach_dir="EW")
    return World(roads=[road_ns, road_ew], intersections=[inter], vehicles=[])

def spawn_fn(now_s: float, world: World):
    spawned = []
    for road in world.roads:
        if random.random() < 0.15:
            vid = len(world.vehicles) + 1
            car = Vehicle(id=vid, road=road, pos_m=0.0, enter_time_s=now_s)
            world.vehicles.append(car)
            spawned.append(car)
    return spawned

if __name__ == "__main__":
    random.seed(42)
    world = build_demo_world()
    policy = FixedCyclePolicy(green_ns=8, yellow_ns=2, green_ew=8, yellow_ew=2)

    renderer = PygameRenderer(world, width=900, height=700)
    # render_fn will be a small closure that draws and flips each tick
    def render(_world):
        renderer.handle_events()
        if not renderer.running:
            raise SystemExit
        renderer.clear()
        renderer.draw_world()
        renderer.flip(fps_limit=60)
        return None  # nothing to print

    sim = Simulation(world, policy, spawn_fn, render_fn=render, dt=0.5, max_time=120)
    summary = sim.run()
    print("SUMMARY:", summary)