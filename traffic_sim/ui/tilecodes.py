from dataclasses import dataclass

@dataclass(frozen=True)
class Tile:
    col: int
    row: int

# Map simple ASCII codes to atlas positions (you can tweak)
TILES = {
    "-": Tile(1, 0),   # horizontal straight
    "|": Tile(0, 1),   # vertical straight
    "+": Tile(2, 0),   # 4-way intersection
    "L": Tile(3, 0),   # corner (turn)
    "T": Tile(4, 0),   # T-junction
    "E": Tile(5, 0),   # endcap
}