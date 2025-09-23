from dataclasses import dataclass

VALID_DIRS = {"NS", "EW"}
VALID_COLORS = {"RED", "YELLOW", "GREEN"}

@dataclass
class TrafficLight:
    direction: str = "NS"
    color: str = "RED"

    def set_state(self, direction: str, color: str):
        assert direction in VALID_DIRS and color in VALID_COLORS
        self.direction = direction
        self.color = color

    def is_green_for(self, approach_dir: str) -> bool:
        return self.direction == approach_dir and self.color == "GREEN"

    def is_yellow_for(self, approach_dir: str) -> bool:
        return self.direction == approach_dir and self.color == "YELLOW"