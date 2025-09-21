import pygame
from dataclasses import dataclass
from typing import Tuple, Dict, List

TILE_PX = 32       # your sheet is 32x32 tiles
PX_PER_M = 4       # rendering scale (1 m = 4 px) – keep sim units in meters

# Minimal palette
BG = (74, 86, 57)  # grassy bg under roads

@dataclass(frozen=True)
class Tile:
    col: int
    row: int

class TileAtlas:
    def __init__(self, sheet_path: str):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        self.cols = self.sheet.get_width() // TILE_PX
        self.rows = self.sheet.get_height() // TILE_PX

    def get(self, col: int, row: int) -> pygame.Surface:
        rect = pygame.Rect(col * TILE_PX, row * TILE_PX, TILE_PX, TILE_PX)
        surf = pygame.Surface((TILE_PX, TILE_PX), pygame.SRCALPHA)
        surf.blit(self.sheet, (0, 0), rect)
        return surf

class PygameTilesRenderer:
    """Renders a road grid + vehicles. Grid uses tile codes -> atlas coords."""
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
        # cache surfaces
        self.cache: Dict[Tuple[int,int], pygame.Surface] = {}

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.running = False

    def clear(self):
        self.screen.fill(BG)

    def draw_grid(self):
        for r, row in enumerate(self.grid):
            for c, code in enumerate(row):
                if code == " ":
                    continue
                t = self.tilemap[code]
                key = (t.col, t.row)
                surf = self.cache.get(key)
                if surf is None:
                    surf = self.atlas.get(t.col, t.row)
                    self.cache[key] = surf
                self.screen.blit(surf, (c * TILE_PX, r * TILE_PX))

    def draw_cars(self):
        # Vehicles’ positions are in meters along a Road; we’ll project to tile centerlines.
        for v in self.world.vehicles:
            if v.finished: continue
            # Each Road has a precomputed screen polyline [(x_px, y_px) ...].
            path = getattr(v.road, "screen_points", None)
            if not path: continue
            # Simple linear interpolation along the path using pos_m normalized
            length_m = v.road.length_m
            s = max(0.0, min(1.0, v.pos_m / length_m))
            # path has 2 points (straight); interpolate
            (x0,y0), (x1,y1) = path[0], path[-1]
            x = x0 + (x1 - x0) * s
            y = y0 + (y1 - y0) * s
            pygame.draw.rect(self.screen, (240,240,240),
                             pygame.Rect(int(x)-4, int(y)-7, 8, 14) if v.road.approach_dir in ("NS","SN")
                             else pygame.Rect(int(x)-7, int(y)-4, 14, 8), border_radius=3)

    def flip(self, fps=60):
        pygame.display.flip()
        self.clock.tick(fps)

    def render_frame(self):
        self.handle_events()
        if not self.running:
            raise SystemExit
        self.clear()
        self.draw_grid()
        self.draw_cars()
        self.flip(60)