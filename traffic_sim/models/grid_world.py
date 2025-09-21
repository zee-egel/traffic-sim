from dataclasses import dataclass
from collections import deque
from typing import List, Tuple, Dict, Optional
from .world import World
from .road import Road
from .intersection import Intersection
from .vehicle import Vehicle

TILE_M = 8.0  # physical meters per tile
DIRS = {"N":(-1,0), "S":(1,0), "W":(0,-1), "E":(0,1)}
APPROACH_FOR = {("N","S"):"NS", ("S","N"):"NS", ("W","E"):"EW", ("E","W"):"EW"}

def is_road(code: str) -> bool:
    return code != " "

def neighbors(grid: List[List[str]], r:int, c:int):
    H, W = len(grid), len(grid[0])
    for d,(dr,dc) in DIRS.items():
        r2,c2 = r+dr, c+dc
        if 0 <= r2 < H and 0 <= c2 < W and is_road(grid[r2][c2]):
            yield d,(r2,c2)

def build_world_from_grid(grid: List[List[str]]) -> Tuple[World, Dict[Tuple[int,int], Intersection]]:
    H, W = len(grid), len(grid[0])
    nodes: Dict[Tuple[int,int], Intersection] = {}
    roads: List[Road] = []

    # create intersections at every road tile
    for r in range(H):
        for c in range(W):
            if is_road(grid[r][c]):
                nodes[(r,c)] = Intersection(name=f"I{r}_{c}")

    # connect neighbors with two directed Roads (both ways)
    for (r,c), inter in nodes.items():
        for d,(r2,c2) in neighbors(grid, r, c):
            inter2 = nodes[(r2,c2)]
            # straight length 1 tile
            length_m = TILE_M
            # approach_dir based on axis
            if r == r2:   # horizontal move
                approach = "EW"
            else:         # vertical move
                approach = "NS"
            name = f"R{r}_{c}_to_{r2}_{c2}"
            rd = Road(name=name, length_m=length_m, speed_mps=10.0,
                      to_intersection=inter2, approach_dir=approach)
            # Screen points (center of tiles) for renderer
            rd.screen_points = [((c+0.5)*32, (r+0.5)*32), ((c2+0.5)*32, (r2+0.5)*32)]
            rd.from_tile = (r,c)
            rd.to_tile = (r2,c2)
            roads.append(rd)

    world = World(roads=roads, intersections=list(nodes.values()), vehicles=[])
    return world, nodes

def bfs_route(world: World, nodes: Dict[Tuple[int,int], Intersection],
              start_tile: Tuple[int,int], goal_tile: Tuple[int,int]) -> Optional[List[Road]]:
    """Find a path as a sequence of Roads between tile centers."""
    # Build adjacency from Roads
    adj: Dict[Tuple[int,int], List[Road]] = {}
    for rd in world.roads:
        src = rd.from_tile
        adj.setdefault(src, []).append(rd)

    q = deque([start_tile])
    prev: Dict[Tuple[int,int], Tuple[Tuple[int,int], Road]] = {}
    seen = {start_tile}

    while q:
        u = q.popleft()
        if u == goal_tile:
            break
        for rd in adj.get(u, []):
            v = rd.to_tile
            if v in seen: continue
            seen.add(v)
            prev[v] = (u, rd)
            q.append(v)

    if goal_tile not in prev and start_tile != goal_tile:
        return None

    # reconstruct
    path_roads: List[Road] = []
    cur = goal_tile
    while cur != start_tile:
        pu, rd = prev[cur]
        path_roads.append(rd)
        cur = pu
    path_roads.reverse()
    return path_roads

def spawn_vehicle(world: World, start: Tuple[int,int], goal: Tuple[int,int], t_now: float) -> Optional[Vehicle]:
    # Find the first road that departs from start towards the route
    route = bfs_route(world, {}, start, goal)
    if not route:
        return None
    vid = len(world.vehicles) + 1
    car = Vehicle(id=vid, road=route[0], pos_m=0.0, enter_time_s=t_now)
    car.route = route  # attach planned route
    world.vehicles.append(car)
    return car

def advance_routing(world: World):
    """Move vehicles to next road when they finish the current one."""
    for v in list(world.vehicles):
        if v.finished and hasattr(v, "route"):
            # pop current road and move onto next, or mark fully done
            if v.route and v.road is v.route[0]:
                v.route.pop(0)
            if v.route:
                # reset for next edge
                v.finished = False
                v.pos_m = 0.0
                v.road = v.route[0]
            # else: no next road → keep finished=True