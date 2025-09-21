import random

def build_demo_world():
    inter = Intersection(name="X1")
    road_ns = Road(name="North-South", length_m=120.0, speed_mps=10.0, to_intersection=inter, approach_dir="NS")
    road_ew = Road(name="East-West", length_m=100.0, speed_mps=8.0, to_intersection=inter, approach_dir="EW")
    return World(roads=[road_ns, road_ew], intersections=[inter], vehicles=[])

def spawn_fn(now_s: float, world: World) -> list[Vehicle]:
    spawned = []
    for road in world.roads:
        if random.random() < 0.15 # tune demand
        vid = len(world.vehicles) + 1
        car = Vehicle(id=vid, road=road, pos_m=0.0, enter_time_s=now_s)
        world.vehicles.append(car)
        spawned.append(car)
    return spawned

if __name__ == "__main__":
    random.seed(42) 
    world = build_demo_world()
    policy = FixedCyclePolicy(green_ns=8, yellow_ns=2, green_ew=8, yellow_ew=2)
    sim = Simulation(world, policy, spawn_fn, render_fn=lambda w: draw(w), dt=1.0, max_time=60.0)