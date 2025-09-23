from dataclasses import dataclass, field
from typing import List, Dict
from .road import Road
from .vehicle import Vehicle
from .intersection import Intersection

MIN_GAP_M = 5.0  # min bumper distance

@dataclass
class World:
    roads: List[Road] = field(default_factory=list)
    intersections: List[Intersection] = field(default_factory=list)
    vehicles: List[Vehicle] = field(default_factory=list)

    def tick(self, dt: float):
        # Group vehicles by road and sort by position
        by_road: Dict[Road, List[Vehicle]] = {}
        for v in self.vehicles:
            if not v.finished:
                by_road.setdefault(v.road, []).append(v)
        for road, cars in by_road.items():
            cars.sort(key=lambda x: x.pos_m)

        # Car-following + lights
        for road, cars in by_road.items():
            inter = road.to_intersection
            stop_line = road.length_m - 2.0
            for i, v in enumerate(cars):
                desired = v.target_speed * dt

                # leader gap
                if i < len(cars) - 1:
                    leader = cars[i + 1]
                    max_pos = max(0.0, leader.pos_m - MIN_GAP_M)
                else:
                    max_pos = road.length_m

                # red/yellow constraint
                can_go = inter.signal.is_green_for(road.approach_dir)
                if not can_go:
                    max_pos = min(max_pos, stop_line)

                v.pos_m = min(max_pos, v.pos_m + desired)

                # at end
                if v.pos_m >= road.length_m - 1e-6:
                    if can_go:
                        nxt = self._choose_next_road(road)
                        if nxt is not None:
                            v.road = nxt
                            v.pos_m = 0.0
                            v.finished = False
                        else:
                            v.finished = True
                    else:
                        v.pos_m = stop_line  # wait

    def _choose_next_road(self, rd: Road) -> Road | None:
        """Pick outgoing road at intersection; sometimes exit at border."""
        from_tile = getattr(rd, "to_tile", None)
        prev_tile = getattr(rd, "from_tile", None)

        # optional: border exit
        grid_hints = getattr(self, "_grid_size", None)
        if grid_hints and from_tile is not None:
            H, W = grid_hints
            r, c = from_tile
            at_border = (r == 0 or r == H - 1 or c == 0 or c == W - 1)
            if at_border:
                import random
                if random.random() < 0.35:
                    return None

        # candidates (avoid immediate U-turn when other exits exist)
        cands: List[Road] = []
        for r2 in self.roads:
            if getattr(r2, "from_tile", None) == from_tile:
                if getattr(r2, "to_tile", None) != prev_tile:
                    cands.append(r2)

        if not cands:
            for r2 in self.roads:
                if getattr(r2, "from_tile", None) == from_tile:
                    return r2
            return None

        # prefer going straight if available
        straight = [r2 for r2 in cands if r2.approach_dir == rd.approach_dir]
        import random
        return random.choice(straight or cands)