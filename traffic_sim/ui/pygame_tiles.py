"""Tile-based Pygame renderer for the grid world variant."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import pygame

from .sprite_loader import DEFAULT_CAR_NAMES, load_cars_manifest
from .tilecodes import Tile, TILES

TILE_PX = 32
FRAME_RATE = 30
BG_COLOR = (74, 86, 57)


class TileAtlas:
    """Slices a tile atlas PNG into individual cell surfaces."""

    def __init__(self, sheet_path: str | Path, tile_px: int = TILE_PX) -> None:
        if not pygame.get_init():  # ensure pygame is ready for image loading
            pygame.init()
        self.tile_px = tile_px
        path = Path(sheet_path)
        self.sheet = pygame.image.load(str(path)).convert_alpha()
        self._cache: Dict[Tuple[int, int], pygame.Surface] = {}

    def get(self, tile: Tile) -> pygame.Surface:
        key = (tile.col, tile.row)
        if key not in self._cache:
            x = tile.col * self.tile_px
            y = tile.row * self.tile_px
            rect = pygame.Rect(x, y, self.tile_px, self.tile_px)
            surf = pygame.Surface((self.tile_px, self.tile_px), pygame.SRCALPHA)
            surf.blit(self.sheet, (0, 0), rect)
            self._cache[key] = surf
        return self._cache[key]


class PygameTilesRenderer:
    """Render the grid world using a tile atlas and vehicle sprites."""

    def __init__(
        self,
        world,
        grid: List[List[str]],
        tilemap: Dict[str, Tile] | None = None,
        sheet_path: str | Path = "assets/sprites/roads_2w.png",
        title: str = "Traffic Sim",
    ) -> None:
        pygame.init()
        self.world = world
        self.grid = grid
        self.tilemap = tilemap or TILES
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        self.screen = pygame.display.set_mode((cols * TILE_PX, rows * TILE_PX))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.atlas = TileAtlas(sheet_path, tile_px=TILE_PX)

        self.car_sprites = load_cars_manifest(
            "assets/sprites/cars.png",
            names=DEFAULT_CAR_NAMES,
        )
        self.scaled_cars: Dict[str, pygame.Surface] = {}
        self._prepare_scaled_sprites()

    def _prepare_scaled_sprites(self) -> None:
        target_w_ns, target_h_ns = 12, 22
        target_w_ew, target_h_ew = 22, 12
        for name, surf in self.car_sprites.items():
            ns = pygame.transform.smoothscale(surf, (target_w_ns, target_h_ns))
            ew = pygame.transform.smoothscale(surf, (target_w_ew, target_h_ew))
            self.scaled_cars[f"{name}:NS"] = ns
            self.scaled_cars[f"{name}:EW"] = pygame.transform.rotate(ew, 90)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                self.running = False

    def _draw_grid(self) -> None:
        for r, row in enumerate(self.grid):
            for c, code in enumerate(row):
                tile = self.tilemap.get(code)
                if tile is None:
                    continue
                tile_surface = self.atlas.get(tile)
                self.screen.blit(tile_surface, (c * TILE_PX, r * TILE_PX))

    def _draw_cars(self) -> None:
        for vehicle in self.world.vehicles:
            if vehicle.finished:
                continue
            path = getattr(vehicle.road, "screen_points", None)
            if not path:
                continue
            (x0, y0), (x1, y1) = path[0], path[-1]
            progress = max(0.0, min(1.0, vehicle.pos_m / max(1e-6, vehicle.road.length_m)))
            x = x0 + (x1 - x0) * progress
            y = y0 + (y1 - y0) * progress

            sprite_name = vehicle.sprite_key or vehicle.kind or "sedan_red"
            orient = "NS" if vehicle.road.approach_dir in {"NS", "SN"} else "EW"
            key = f"{sprite_name}:{orient}"
            sprite = self.scaled_cars.get(key)
            if sprite is None and self.scaled_cars:
                sprite = next(iter(self.scaled_cars.values()))
            if sprite is None:
                continue
            rect = sprite.get_rect(center=(int(x), int(y)))
            self.screen.blit(sprite, rect)

    def render_frame(self) -> None:
        if not self.running:
            return
        self._handle_events()
        self.screen.fill(BG_COLOR)
        self._draw_grid()
        self._draw_cars()
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)

    def close(self) -> None:
        pygame.quit()

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        if pygame.get_init():
            pygame.quit()
