from dataclasses import dataclass, field

@dataclass
class Vehicle:
    id: int
    road: "Road"
    pos_m: float = 0.0
    length_m: float = 4.5
    max_accel: float = 2.0
    max_decel: float = 4.5
    target_speed: float = None
    finished: bool = False
    enter_time_s: float = 0.0
    exit_time_s: float = 0.0

    # NEW: visual/behavioral flavor
    kind: str = "car"          # e.g. "police","taxi","sports","van","ambulance","sedan","truck","bike_blue","bike_red"
    sprite_key: str | None = None

    def __post_init__(self):
        if self.target_speed is None:
            self.target_speed = self.road.speed_mps
        # tiny behavior tweaks by kind (can tweak later)
        if self.kind in ("sports",):
            self.target_speed *= 1.2
        elif self.kind in ("van","truck","ambulance"):
            self.target_speed *= 0.9
        elif self.kind.startswith("bike"):
            self.target_speed *= 0.8

    def update(self, dt: float, intersection: "Intersection"):
        if self.finished:
            return
        stop_line = self.road.length_m - 2.0
        can_go = intersection.signal.is_green_for(self.road.approach_dir) if intersection else True
        should_stop = not can_go

        v = self.target_speed
        if should_stop and self.pos_m >= stop_line:
            v = 0.0

        self.pos_m = self.road.clamp_pos(self.pos_m + v * dt)
        if self.pos_m >= self.road.length_m:
            self.finished = True