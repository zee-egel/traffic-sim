"""World container holding roads, intersections, and vehicles."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class World:
    roads: List = field(default_factory=list)
    intersections: List = field(default_factory=list)
    vehicles: List = field(default_factory=list)

    def add_intersection(self, intersection) -> None:
        self.intersections.append(intersection)
        intersection.world = self

    def add_road(self, road) -> None:
        self.roads.append(road)
        if road.to_intersection is not None:
            road.to_intersection.register_road(road)

    def add_vehicle(self, vehicle) -> None:
        self.vehicles.append(vehicle)

    from .grid_world import advance_routing

    def tick(self, dt: float):
        inter = self.intersections[0] if self.intersections else None
        for car in list(self.vehicles):
            car.update(dt, inter)  # still using single signal; we’ll expand next
        try:
            advance_routing(self)
        except Exception:
            pass

