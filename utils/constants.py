# Constants
BOARD_SIZE = 8  # 8x8

EMPTY = 0  # Empty
INF = 2000000000  # infinity

X = 1  # Blacks Player
O = -1  # Whites player

PEG_COLORS = {X: (0, 0, 0, 255), O: (255, 255, 255, 255)}  # Black and White colors
PLAYER_NAMES = {X: "Black", O: "White"}

PEG_MARGIN = 5
EMPTY_CELL_COLOR = (0, 0, 0, 0)  # Transparent

class BTN_STATUS:
    TEST = (0, 0, 0, 150)
    ACTIVE = (0, 0, 0, 0)
    HOVERED = (255, 255, 255, 70)
    DISABLED = (0, 0, 0, 150)