import pygame
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

@dataclass(frozen=True)
class SpriteInfo:
    name: str
    rect: pygame.Rect   # where to cut from the sheet
    scale: float = 1.0  # additional scaling factor

class SpriteSheet:
    def __init__(self, path: str):
        self.sheet = pygame.image.load(path).convert_alpha()

    def extract(self, rect: pygame.Rect) -> pygame.Surface:
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        surf.blit(self.sheet, (0, 0), rect)
        return surf

# These bounds were extracted automatically from the sprite sheet so we
# don't rely on an even grid that crops vehicles awkwardly. Coordinates
# are inclusive of all opaque pixels, leaving the surrounding padding in place.
_CAR_SPRITE_BOUNDS: List[SpriteInfo] = [
    SpriteInfo("police", pygame.Rect(50, 50, 800, 1945)),
    SpriteInfo("taxi", pygame.Rect(1200, 50, 800, 1918)),
    SpriteInfo("sports_blue", pygame.Rect(2300, 50, 900, 1915)),
    SpriteInfo("van", pygame.Rect(3600, 50, 1000, 2188)),
    SpriteInfo("sports_yellow", pygame.Rect(50, 2600, 1000, 1995)),
    SpriteInfo("ambulance", pygame.Rect(1100, 2600, 1100, 2340)),
    SpriteInfo("sedan_red", pygame.Rect(2300, 2600, 1002, 2187)),
    SpriteInfo("motor_blue", pygame.Rect(3500, 2600, 600, 1557)),
    SpriteInfo("motor_red", pygame.Rect(4200, 2600, 700, 1408)),
]

DEFAULT_CAR_NAMES: Sequence[str] = [info.name for info in _CAR_SPRITE_BOUNDS]


def load_cars_manifest(
    sheet_path: str,
    names: Sequence[str] | None = None,
    overrides: Iterable[SpriteInfo] | None = None,
) -> Dict[str, pygame.Surface]:
    """Load named car sprites using precise bounding boxes."""

    ss = SpriteSheet(sheet_path)

    if overrides is not None:
        chosen_infos: List[SpriteInfo] = list(overrides)
    else:
        chosen_infos = list(_CAR_SPRITE_BOUNDS)

    if names is not None:
        lookup = {info.name: info for info in chosen_infos}
        try:
            chosen_infos = [lookup[name] for name in names]
        except KeyError as exc:  # pragma: no cover - developer error guard
            missing = exc.args[0]
            raise KeyError(f"Unknown car sprite '{missing}'") from None

    sprites: Dict[str, pygame.Surface] = {}
    for info in chosen_infos:
        spr = ss.extract(info.rect)
        if info.scale != 1.0:
            w = max(1, int(info.rect.width * info.scale))
            h = max(1, int(info.rect.height * info.scale))
            spr = pygame.transform.smoothscale(spr, (w, h))
        sprites[info.name] = spr
    return sprites
