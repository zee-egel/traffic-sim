from dataclasses import dataclass

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
    kind: str = "sedan"
    sprite_key: str | None = None

    def __post_init__(self):
        if self.target_speed is None:
            self.target_speed = self.road.speed_mps
        if self.kind.startswith("motor"):
            self.target_speed *= 0.85
        elif self.kind in ("van", "ambulance", "truck"):
            self.target_speed *= 0.9
        elif self.kind.startswith("sports"):
            self.target_speed *= 1.2

    # Movement handled in World.tick (car-following + signals)
    def update(self, dt: float, intersection: "Intersection"):  # noqa: ARG002
        return