from dataclasses import dataclass, field
from .traffic_light import TrafficLight

@dataclass
class Intersection:
    name: str
    signal: TrafficLight = field(default_factory=TrafficLight)
    phase_offset_s: float = 0.0  # to desync lights city-wide

    def apply_policy(self, policy, now_s: float):
        direction, color = policy.decide(self, now_s + self.phase_offset_s)
        self.signal.set_state(direction, color)