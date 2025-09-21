import pygame
from dataclasses import dataclass
from typing import Tuple, Dict, List
from .sprites import load_cars_manifest

TILE_PX = 32
PX_PER_M = 4
BG = (74, 86, 57)

@dataclass(frozen=True)
class Tile:
    col: int
    row: int

class TileAtlas:
    ...
    # (keep as you already have)

class PygameTilesRenderer:
    def __init__(self, world, grid: List[List[str]], tilemap: Dict[str, Tile],
                 sheet_path: str = "assets/tiles/roads_2w.png", title="Traffic Sim"):
        pygame.init()
        self.world = world
        self.grid = grid
        self.tilemap = tilemap
        self.atlas = TileAtlas(sheet_path)
        h, w = len(grid), len(grid[0])
        self.screen = pygame.display.set_mode((w * TILE_PX, h * TILE_PX))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.cache: Dict[Tuple[int,int], pygame.Surface] = {}

        # NEW: load car sprites (adjust cell size if your sheet differs)
        self.car_sprites = load_cars_manifest(
            "assets/sprites/cars.png",
            cell_w=256, cell_h=256,      # <— tweak if needed
            grid_cols=4, grid_rows=3,    # <— tweak if needed
            names=[
                "police","taxi","sports_blue","van",
                "sports_yellow","ambulance","sedan_red","motor_blue",
                "motor_red"
            ]
        )
        # Pre-scale car sprites to lane-ish width
        self.pre_scaled: Dict[str, pygame.Surface] = {}
        self._prepare_scaled()

    def _prepare_scaled(self):
        # fit ~12 px cross-section for a single-lane vibe
        target_w_ns, target_h_ns = 12, 22
        target_w_ew, target_h_ew = 22, 12
        for name, surf in self.car_sprites.items():
            # north-south base (upright)
            ns = pygame.transform.smoothscale(surf, (target_w_ns, target_h_ns))
            ew = pygame.transform.smoothscale(surf, (target_w_ew, target_h_ew))
            # store both orientations
            self.pre_scaled[name + ":NS"] = ns
            self.pre_scaled[name + ":EW"] = pygame.transform.rotate(ew, 90)

    ...
    # draw_grid stays the same

    def draw_cars(self):
        for v in self.world.vehicles:
            if v.finished: 
                continue
            path = getattr(v.road, "screen_points", None)
            if not path:
                continue
            (x0,y0), (x1,y1) = path[0], path[-1]
            s = max(0.0, min(1.0, v.pos_m / max(1e-6, v.road.length_m)))
            x = x0 + (x1 - x0) * s
            y = y0 + (y1 - y0) * s

            sprite_name = v.sprite_key or v.kind
            orient = "NS" if v.road.approach_dir in ("NS","SN") else "EW"
            key = f"{sprite_name}:{orient}"
            img = self.pre_scaled.get(key)
            if img is None:
                # fallback: any sprite
                img = next(iter(self.pre_scaled.values()))
            rect = img.get_rect(center=(int(x), int(y)))
            self.screen.blit(img, rect)

    ...