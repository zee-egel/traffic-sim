# BEFORE
# @dataclass
# class Road:

# AFTER
from dataclasses import dataclass

@dataclass(eq=False)   # identity-based equality & hash, safe for dict keys
class Road:
    name: str
    length_m: float
    speed_mps: float
    to_intersection: "Intersection"
    approach_dir: str  # "NS" or "EW"
    screen_points: list[tuple[int, int]] | None = None
    from_tile: tuple[int, int] | None = None
    to_tile: tuple[int, int] | None = None

    def clamp_pos(self, x: float) -> float:
        return max(0.0, min(self.length_m, x))