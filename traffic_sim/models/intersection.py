"""Intersection model that hosts a single traffic light."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .traffic_light import TrafficLight


@dataclass
class Intersection:
    name: str
    signal: TrafficLight = field(default_factory=TrafficLight)

    def __post_init__(self) -> None:
        self.world = None
        self._incoming_roads: Dict[str, List] = {"NS": [], "EW": []}

    def register_road(self, road) -> None:
        """Register an incoming road for lookup by direction."""
        self._incoming_roads.setdefault(road.approach_dir, []).append(road)

    def incoming_roads(self, direction: str) -> List:
        return list(self._incoming_roads.get(direction, []))

    def vehicles_for(self, direction: str):
        if not getattr(self, "world", None):
            return []
        return [v for v in self.world.vehicles if v.road.approach_dir == direction and not v.finished]

    def apply_policy(self, policy, now_s: float) -> None:
        direction, color = policy.decide(self, now_s)
        self.signal.set_state(direction, color)

