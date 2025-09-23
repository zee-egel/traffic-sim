from dataclasses import dataclass

@dataclass(frozen=True)
class TimeStep:
    dt: float  # seconds

class SimClock:
    def __init__(self, dt: float = 1.0):
        self.t = 0.0
        self.step = TimeStep(dt)

    def tick(self):
        self.t += self.step.dt
        return self.step

    def now(self) -> float:
        return self.t