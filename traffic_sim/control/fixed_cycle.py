from dataclasses import dataclass
from .policy_base import TrafficSignalPolicy

@dataclass
class FixedCyclePolicy(TrafficSignalPolicy):
    green_ns: float = 8.0
    yellow_ns: float = 2.0
    green_ew: float = 8.0
    yellow_ew: float = 2.0

    def decide(self, intersection, now_s: float):
        cycle = self.green_ns + self.yellow_ns + self.green_ew + self.yellow_ew
        t = now_s % cycle
        if t < self.green_ns:
            return ("NS", "GREEN")
        elif t < self.green_ns + self.yellow_ns:
            return ("NS", "YELLOW")
        elif t < self.green_ns + self.yellow_ns + self.green_ew:
            return ("EW", "GREEN")
        else:
            return ("EW", "YELLOW")