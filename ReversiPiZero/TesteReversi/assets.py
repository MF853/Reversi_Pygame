import pygame
from constants import *

# Scale images to match the cell size
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))
player1_image = pygame.transform.scale(player1_image, (CELL_SIZE*scale_value, CELL_SIZE*scale_value))
player2_image = pygame.transform.scale(player2_image, (CELL_SIZE*scale_value, CELL_SIZE*scale_value))
possible_move_image1 = pygame.transform.scale(possible_move_image1, (CELL_SIZE*scale_value, CELL_SIZE*scale_value))
possible_move_image2 = pygame.transform.scale(possible_move_image2, (CELL_SIZE*scale_value, CELL_SIZE*scale_value))

# Calculate the positions for the player tab image
player_tab_width, player_tab_height = player_tab_image.get_size()
player_tab_image = pygame.transform.scale(player_tab_image, (player_tab_width*1.18, player_tab_height*1.18))
player_tab_width, player_tab_height = player_tab_image.get_size()

# Define board Position
board_x = (screen_width - board_image.get_width()) // 2
board_y = (screen_height - board_image.get_height()) // 2

# Define Player_Tab Position
player1_tab_x, player1_tab_y = (board_x-player_tab_width), board_y
player2_tab_x, player2_tab_y = (board_x + board_width), board_y

# Define Top Bar Button Positions
mute_button_width, mute_button_height  = mute_button.get_size()
mute_button_x = player1_tab_x + 10
mute_button_y =  board_y - mute_button.get_height() - 6

start_button_width, start_button_height = start_button.get_size()
start_button_x = mute_button_x + mute_button_width +10
start_button_y = mute_button_y

end_game_button_width, end_game_button_height = end_game_button.get_size()
end_game_button_x = start_button_x + start_button_width + backplate_image.get_width()
end_game_button_y = start_button_y -4