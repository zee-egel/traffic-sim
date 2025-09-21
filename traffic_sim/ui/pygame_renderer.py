import pygame

PX_PER_M = 4
LANE_HALF_W = 6  # px half-width per lane strip
BG = (32, 34, 36)
ROAD = (64, 68, 72)
CAR = (220, 220, 220)
NS_COLOR = (120, 200, 255)
EW_COLOR = (255, 200, 120)
RED = (220, 64, 64)
YEL = (230, 200, 60)
GRN = (64, 200, 96)

class PygameRenderer:
    def __init__(self, world, width=800, height=600, title="Traffic Sim"):
        pygame.init()
        self.world = world
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.center = (width // 2, height // 2)
        self.running = True

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False

    def clear(self):
        self.screen.fill(BG)

    def _m2px(self, meters: float) -> int:
        return int(meters * PX_PER_M)

    def draw_world(self):
        cx, cy = self.center

        # Draw NS road (vertical)
        ns = [r for r in self.world.roads if r.approach_dir == "NS"][0]
        half_len_ns = self._m2px(ns.length_m // 2)
        pygame.draw.rect(
            self.screen, ROAD,
            pygame.Rect(cx - LANE_HALF_W, cy - half_len_ns, LANE_HALF_W * 2, half_len_ns * 2),
            border_radius=8
        )

        # Draw EW road (horizontal)
        ew = [r for r in self.world.roads if r.approach_dir == "EW"][0]
        half_len_ew = self._m2px(ew.length_m // 2)
        pygame.draw.rect(
            self.screen, ROAD,
            pygame.Rect(cx - half_len_ew, cy - LANE_HALF_W, half_len_ew * 2, LANE_HALF_W * 2),
            border_radius=8
        )

        # Draw traffic light (simple circles)
        inter = self.world.intersections[0]
        d, c = inter.signal.direction, inter.signal.color
        def col(s):
            if s == "RED": return RED
            if s == "YELLOW": return YEL
            return GRN
        # NS lamp
        pygame.draw.circle(self.screen, col("GREEN" if d=="NS" and c=="GREEN" else "RED"), (cx, cy-28), 6)
        # EW lamp
        pygame.draw.circle(self.screen, col("GREEN" if d=="EW" and c=="GREEN" else "RED"), (cx+28, cy), 6)

        # Draw vehicles
        for v in self.world.vehicles:
            if v.finished:
                continue
            if v.road.approach_dir == "NS":
                # pos_m grows southward: map 0 at far north to length at far south
                y = cy - half_len_ns + self._m2px(v.pos_m)
                x = cx
                color = NS_COLOR
                rect = pygame.Rect(0, 0, 10, 18)
                rect.center = (x, y)
            else:  # EW
                x = cx - half_len_ew + self._m2px(v.pos_m)
                y = cy
                color = EW_COLOR
                rect = pygame.Rect(0, 0, 18, 10)
                rect.center = (x, y)
            pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def flip(self, fps_limit=60):
        pygame.display.flip()
        # limit for visual smoothness; your simulation dt is independent
        self.clock.tick(fps_limit)