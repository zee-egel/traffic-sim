from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Metrics:
    completed_times: List[float] = field(default_factory=list)
    entered: int = 0
    exited: int = 0

    def on_enter(self):
        self.entered += 1

    def on_exit(self, t: float, car):
        self.exited += 1
        self.completed_times.append(max(0.0, t - car.enter_time_s))

    def summary(self) -> Dict[str, float]:
        avg = sum(self.completed_times)/len(self.completed_times) if self.completed_times else 0.0
        return {"entered": self.entered, "exited": self.exited, "avg_travel_time_s": round(avg, 2)}