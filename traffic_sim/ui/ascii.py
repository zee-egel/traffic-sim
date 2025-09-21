"""ASCII renderer for the simple traffic simulation."""
from __future__ import annotations

from typing import Dict


def _build_line(width: int) -> list[str]:
    return ["."] * width


def _place_vehicle(line: list[str], road_length: float, pos: float) -> None:
    if road_length <= 0:
        return
    idx = int((pos / road_length) * (len(line) - 1))
    idx = max(0, min(len(line) - 1, idx))
    line[idx] = "C"


def draw(world, width: int = 60) -> str:
    """Return a two-line ASCII snapshot with cars marked as ``C``."""
    lines: Dict[str, list[str]] = {"NS": _build_line(width), "EW": _build_line(width)}

    for vehicle in world.vehicles:
        if vehicle.finished:
            continue
        road = vehicle.road
        if road.approach_dir in lines:
            _place_vehicle(lines[road.approach_dir], road.length_m, vehicle.pos_m)

    return "NS:" + "".join(lines["NS"]) + "\n" + "EW:" + "".join(lines["EW"])
