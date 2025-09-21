import pygame
from dataclasses import dataclass
from typing import Dict, Tuple, List

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

def load_cars_manifest(sheet_path: str, cell_w: int, cell_h: int,
                       grid_cols: int, grid_rows: int,
                       names: List[str]) -> Dict[str, pygame.Surface]:
    """
    Slices a regular grid sprite sheet. If your sheet layout changes,
    only tweak these numbers & names – no code changes elsewhere.
    """
    ss = SpriteSheet(sheet_path)
    sprites: Dict[str, pygame.Surface] = {}
    idx = 0
    for r in range(grid_rows):
        for c in range(grid_cols):
            if idx >= len(names):
                break
            x, y = c * cell_w, r * cell_h
            spr = ss.extract(pygame.Rect(x, y, cell_w, cell_h))
            sprites[names[idx]] = spr
            idx += 1
        if idx >= len(names):
            break
    return sprites