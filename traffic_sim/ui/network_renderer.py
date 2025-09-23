import math
from typing import Dict

import pygame

from .sprite_loader import DEFAULT_CAR_NAMES, load_cars_manifest

TILE_PX = 64
LANE_W = 14  # px half-lane-ish width

class NetworkRenderer:
    def __init__(self, world, title="Traffic Sim"):
        pygame.init()
        self.world = world
        xs, ys = [], []
        for rd in world.roads:
            (x0,y0),(x1,y1) = rd.screen_points
            xs += [x0,x1]; ys += [y0,y1]
        w = max(xs) - min(xs) + TILE_PX
        h = max(ys) - min(ys) + TILE_PX
        self.offset = (min(xs) - TILE_PX//2, min(ys) - TILE_PX//2)
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        raw = load_cars_manifest("assets/sprites/cars.png", names=DEFAULT_CAR_NAMES)
        self.cars_scaled: Dict[str, pygame.Surface] = {}
        for name, surf in raw.items():
            self.cars_scaled[name] = pygame.transform.smoothscale(surf, (18, 36))  # portrait
        self.font = pygame.font.SysFont("monospace", 14)

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.running = False

    def _apply_offset(self, x, y):
        ox, oy = self.offset
        return int(x-ox), int(y-oy)

    def draw_roads(self):
        s = self.screen
        s.fill((78, 92, 64))  # grass
        for rd in self.world.roads:
            (x0,y0),(x1,y1) = rd.screen_points
            x0,y0 = self._apply_offset(x0,y0)
            x1,y1 = self._apply_offset(x1,y1)
            pygame.draw.line(s, (64,64,64), (x0,y0), (x1,y1), LANE_W*2)  # asphalt
            pygame.draw.line(s, (200,200,200), (x0,y0), (x1,y1), 2)       # center line

    def draw_lights(self):
        for inter in self.world.intersections:
            # place a dot at any incoming road end (tile center)
            attach = None
            for rd in self.world.roads:
                if getattr(rd, "to_intersection", None) is inter:
                    attach = rd
                    break
            if not attach: continue
            (x,y) = attach.screen_points[-1]
            x,y = self._apply_offset(x,y)
            c = inter.signal.color
            col = (60,200,90) if c=="GREEN" else (230,210,70) if c=="YELLOW" else (220,70,70)
            pygame.draw.circle(self.screen, col, (x, y), 6)

    def draw_cars(self):
        for v in self.world.vehicles:
            if v.finished: continue
            (x0,y0),(x1,y1) = v.road.screen_points
            t = max(0.0, min(1.0, v.pos_m / max(1e-6, v.road.length_m)))
            x = x0 + (x1-x0)*t
            y = y0 + (y1-y0)*t
            heading = math.atan2((y1 - y0), (x1 - x0))
            ang = -math.degrees(heading) + 90  # portrait sprite is 'up'
            img = self.cars_scaled.get(v.sprite_key or v.kind) or next(iter(self.cars_scaled.values()))
            rot = pygame.transform.rotate(img, ang)
            rect = rot.get_rect(center=self._apply_offset(x,y))
            self.screen.blit(rot, rect)

    def draw_hud(self, summary=None):
        if not summary: return
        txt = f"cars: {len([v for v in self.world.vehicles if not v.finished])} | entered: {summary['entered']} | exited: {summary['exited']} | avg_tt: {summary['avg_travel_time_s']:.2f}s"
        surf = self.font.render(txt, True, (0,0,0))
        self.screen.blit(surf, (10,10))

    def flip(self, fps=60):
        pygame.display.flip()
        self.clock.tick(fps)

    def frame(self, summary=None):
        self.handle()
        if not self.running: raise SystemExit
        self.draw_roads()
        self.draw_lights()
        self.draw_cars()
        self.draw_hud(summary)
        self.flip(60)
