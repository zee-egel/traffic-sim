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

    def tick(self, dt: float) -> None:
        if not self.intersections:
            return
        intersection = self.intersections[0]
        for vehicle in self.vehicles:
            vehicle.update(dt, intersection)

