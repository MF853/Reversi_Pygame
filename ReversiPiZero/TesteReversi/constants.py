import pygame
# Constants
GRID_SIZE = 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (113, 167, 196)
YELLOW = (255, 201, 14)
GREEN_BACK = (26, 112, 122)

# Placeholder asset filenames
# BOARD_IMAGE = "./ReversiAssets/FinalBoard.png"
BOARD_IMAGE = "./ReversiAssets/FinalBoard.png"
PLAYER1_IMAGE = "./ReversiAssets/pedrabranca.png"
PLAYER2_IMAGE = "./ReversiAssets/pedrapreta.png"
POSSIBLE_MOVE_IMAGE1 = "./ReversiAssets/opçãodejogada1.png"
POSSIBLE_MOVE_IMAGE2 = "./ReversiAssets/opçãodejogada2test.png"
PLAYER_TAB_IMAGE_FILENAME = "./ReversiAssets/PlayerTab.png"
MUSIC_DIRECTORY = "./music"  # Directory containing music files
MUTE_BUTTON_IMAGE = "./ReversiAssets/mute_button.png"
START_BUTTON = "./ReversiAssets/start_game_button.png"
END_GAME_BUTTON = "./ReversiAssets/end_game_button.png"
BACKPLATE_IMAGE = "./ReversiAssets/time_backplate.png"

# Load assets
board_image = pygame.image.load(BOARD_IMAGE)
player1_image = pygame.image.load(PLAYER1_IMAGE)
player2_image = pygame.image.load(PLAYER2_IMAGE)
possible_move_image1 = pygame.image.load(POSSIBLE_MOVE_IMAGE1)
possible_move_image2 = pygame.image.load(POSSIBLE_MOVE_IMAGE2)
player_tab_image = pygame.image.load(PLAYER_TAB_IMAGE_FILENAME)
mute_button = pygame.image.load(MUTE_BUTTON_IMAGE)
backplate_image = pygame.image.load(BACKPLATE_IMAGE)
start_button = pygame.image.load(START_BUTTON)
end_game_button = pygame.image.load(END_GAME_BUTTON)

scale_value = 0.968
# Get the size of the board image and calculate cell size
board_width, board_height = board_image.get_size()
CELL_SIZE = board_width // GRID_SIZE

# Calculate window size based on the board image
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Initialize the screen
screen = pygame.display.set_mode((1920, 1080))  # Fullscreen mode -> pygame.FULLSCREEN
# Get the size of the screen and calculate cell size
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Reversi")
clock = pygame.time.Clock()