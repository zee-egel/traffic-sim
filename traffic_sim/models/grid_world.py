from typing import List, Tuple, Dict
from .world import World
from .road import Road
from .intersection import Intersection

TILE_PX = 64
TILE_M  = 8.0

def is_road(ch: str) -> bool:
    return ch != " "

DIRS = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

def build_world_from_grid(grid: List[List[str]]) -> World:
    H, W = len(grid), len(grid[0])
    nodes: Dict[Tuple[int, int], Intersection] = {}
    roads: List[Road] = []

    # intersections per road tile
    for r in range(H):
        for c in range(W):
            if is_road(grid[r][c]):
                inter = Intersection(name=f"I{r}_{c}")
                inter.phase_offset_s = ((r * 37 + c * 17) % 13) * 0.5
                nodes[(r, c)] = inter

    def center_px(rc: Tuple[int, int]) -> Tuple[int, int]:
        rr, cc = rc
        return int((cc + 0.5) * TILE_PX), int((rr + 0.5) * TILE_PX)

    # directed roads between neighbors
    for (r, c), a in nodes.items():
        for d, (dr, dc) in DIRS.items():
            r2, c2 = r + dr, c + dc
            if (r2, c2) in nodes:
                b = nodes[(r2, c2)]
                approach = "EW" if r == r2 else "NS"
                name = f"R{r}_{c}_to_{r2}_{c2}"
                rd = Road(
                    name=name,
                    length_m=TILE_M,
                    speed_mps=10.0,
                    to_intersection=b,
                    approach_dir=approach,
                )
                rd.screen_points = [center_px((r, c)), center_px((r2, c2))]
                rd.from_tile = (r, c)
                rd.to_tile = (r2, c2)
                roads.append(rd)

    world = World(roads=roads, intersections=list(nodes.values()), vehicles=[])
    world._grid_size = (H, W)  # hint for border exits
    return world