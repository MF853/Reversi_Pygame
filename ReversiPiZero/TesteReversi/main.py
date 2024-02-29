import pygame
import sys
import math
import os
from constants import *
from assets import *

# Initialize Pygame
pygame.init()

# Game variables
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
board[3][3], board[4][4] = 1, 1  # Player 1
board[3][4], board[4][3] = 2, 2  # Player 2

# Calculate the total width and height of the grid
grid_width = GRID_SIZE * CELL_SIZE
grid_height = GRID_SIZE * CELL_SIZE

# Calculate the horizontal and vertical offsets to center the grid
horizontal_offset = (screen_width - grid_width) // 2
vertical_offset = (screen_height - grid_height) // 2


# Load music files
music_files = [os.path.join(MUSIC_DIRECTORY, filename) for filename in os.listdir(MUSIC_DIRECTORY)]

# Index to track the currently playing music
current_music_index = 0

# Load the first music file
if music_files:
    pygame.mixer.music.load(music_files[current_music_index])
music_playing = True


player_turn = 1
possible_moves = set()


def draw_board():
    # Draw the board image centered on the screen
    screen.blit(board_image, (board_x, board_y))
    screen.blit(start_button, (start_button_x, start_button_y))
    screen.blit(end_game_button, (end_game_button_x, end_game_button_y))

    grid_width = int(board_image.get_width() * scale_value)
    grid_height = int(board_image.get_height() * scale_value)

    # Calculate offsets for the grid to be centered within the board image
    horizontal_offset = board_x + (board_image.get_width() - grid_width) // 2
    vertical_offset = board_y + (board_image.get_height() - grid_height) // 2

    # Draw the grid cells and player pieces
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Calculate the position of each cell relative to the centered grid
            cell_x = horizontal_offset + j * (grid_width // GRID_SIZE)
            cell_y = vertical_offset + i * (grid_height // GRID_SIZE)

            # Draw player pieces and possible moves
            if board[i][j] == 1:
                screen.blit(player1_image, (cell_x, cell_y))
            elif board[i][j] == 2:
                screen.blit(player2_image, (cell_x, cell_y))

    # Draw possible moves
    for move in possible_moves:
        move_x = horizontal_offset + move[1] * (grid_width // GRID_SIZE)
        move_y = vertical_offset + move[0] * (grid_height // GRID_SIZE)
        if player_turn == 1:
            screen.blit(possible_move_image1, (move_x, move_y))
        else:
            screen.blit(possible_move_image2, (move_x, move_y))

    # Draw the player tab image on both sides
    screen.blit(player_tab_image, (player1_tab_x, player1_tab_y))
    screen.blit(player_tab_image, (player2_tab_x, player2_tab_y))
    screen.blit(player1_image, (player1_tab_x + (player_tab_width-player1_image.get_width())/2, player1_tab_y + 100))
    screen.blit(player2_image, (player2_tab_x + (player_tab_width-player2_image.get_width())/2, player2_tab_y + 100))
    screen.blit(mute_button, (mute_button_x, mute_button_y))


def update_score():
    player1_score = sum(row.count(1) for row in board)
    player2_score = sum(row.count(2) for row in board)
    return player1_score, player2_score

def get_valid_moves():
    valid_moves = set()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0 and is_valid_move(i, j):
                valid_moves.add((i, j))
    return valid_moves


def is_valid_move(row, col):
    global player_turn
    opponent = 3 - player_turn  # Opponent's player number

    if board[row][col] != 0:
        return False

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            x, y = row + i, col + j
            flips = 0

            while 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[x][y] == opponent:
                x += i
                y += j
                flips += 1

            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[x][y] == player_turn and flips > 0:
                return True

    return False


def make_move(row, col):
    global player_turn

    if (row, col) in possible_moves:
        board[row][col] = player_turn

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                x, y = row + i, col + j
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[x][y] == 3 - player_turn:
                    flip_tiles(row, col, i, j)

        player_turn = 3 - player_turn  # Switch player turn


def flip_tiles(row, col, dr, dc):
    opponent = 3 - player_turn
    x, y = row + dr, col + dc
    tiles_to_flip = []

    while 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[x][y] == opponent:
        tiles_to_flip.append((x, y))
        x += dr
        y += dc

    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[x][y] == player_turn:
        for tile in tiles_to_flip:
            board[tile[0]][tile[1]] = player_turn


def play_music():
    # Check if there are music files available
    if not music_files:
        print("No music files found.")
        return

    # Load and play the current music file
    pygame.mixer.music.load(music_files[current_music_index])
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    
def is_click_inside_button(mouse_x, mouse_y):
    return mute_button_x < mouse_x < mute_button_x + mute_button_width and mute_button_y < mouse_y < mute_button_y + mute_button_height


def stop_music():
    # Stop the currently playing music
    pygame.mixer.music.pause()


def get_game_time():
    # Get the elapsed time since the game started
    milliseconds = pygame.time.get_ticks()
    seconds = milliseconds // 1000
    minutes = seconds // 60

    # Calculate remaining minutes and seconds after hours
    minutes %= 60
    seconds %= 60

    # Format the time string
    time_str = "{:02}:{:02}".format(minutes, seconds)

    return time_str


# Add a variable to track whether the game has started
game_started = False

game_in_progress = False

def start_game():
    global game_started, possible_moves, board, game_in_progress
    game_started = True
    possible_moves = get_valid_moves()
    # Reset the board to its initial state
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    board[3][3], board[4][4] = 1, 1  # Player 1
    board[3][4], board[4][3] = 2, 2  # Player 2
    # Reset the game time when the game starts
    game_in_progress = True
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Start the timer with 1 second intervals

player1_wins = 0
player2_wins = 0

def display_winner(winner):
    global player1_wins, player2_wins
    font = pygame.font.Font(None, 72)
    if winner == 1:
        player1_wins += 1
        text = font.render("Player 1 wins!", True, YELLOW)
    elif winner == 2:
        player2_wins += 1
        text = font.render("Player 2 wins!", True, YELLOW)
    else:
        text = font.render("It's a draw!", True, YELLOW)
    screen.blit(text, ((screen_width-text.get_width()) // 2, screen_height // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    global possible_moves, player_turn, current_music_index, game_started
    global player1_wins, player2_wins
    running = True
    # Keep track of music state
    music_playing = True
    play_music()  # Start playing music when the game starts

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                if is_click_inside_button(mouseX, mouseY):
                    # Toggle music
                    if music_playing:
                        stop_music()
                    else:
                        play_music()
                    music_playing = not music_playing  # Toggle music state

                elif game_started:
                    # Calculate the mouse position relative to the centered grid
                    col, row = (mouseX - horizontal_offset) // CELL_SIZE, (mouseY - vertical_offset) // CELL_SIZE

                    if (row, col) in possible_moves:
                        make_move(row, col)
                        possible_moves = get_valid_moves()
            
                else:
                    # Check if the start button is clicked
                    if start_button_x < mouseX < start_button_x + start_button_width and start_button_y < mouseY < start_button_y + start_button_height:
                        start_game()  # Start the game

                    # Check if the end game button is clicked
                    elif end_game_button_x < mouseX < end_game_button_x + end_game_button_width and end_game_button_y < mouseY < end_game_button_y + end_game_button_height:
                        running = False  # Stop the main loop and close the game    
                

        # Clear the screen by filling it with the background color
        screen.fill(BLUE)

        draw_board()
        player1_score, player2_score = update_score()
        font_labels = pygame.font.Font(None, 36)
        font_numbers = pygame.font.Font(None, 72)

        # Render and blit player 1 score on the left side of the screen
        points_text = font_labels.render(f"Points", True, YELLOW)
        screen.blit(points_text, (player1_tab_x + (player_tab_width- points_text.get_width())/2, player1_tab_y + player_tab_height/3))
        p1_point_text = font_numbers.render(f"{player1_score}", True, YELLOW)
        screen.blit(p1_point_text, (player1_tab_x + (player_tab_width- p1_point_text.get_width())/2, 35 + player1_tab_y + player_tab_height/3))

        # Render and blit player 2 score on the right side of the screen
        screen.blit(points_text, (player2_tab_x + (player_tab_width- points_text.get_width())/2, player2_tab_y + player_tab_height/3))
        p2_point_text = font_numbers.render(f"{player2_score}", True, YELLOW)
        screen.blit(p2_point_text, (player2_tab_x + (player_tab_width- p2_point_text.get_width())/2, 35 + player2_tab_y + player_tab_height/3))

        # Render and blit game time on the top right corner of the screen
        font_time = pygame.font.Font(None, 42)
        time_str = get_game_time()
        time_text = font_time.render(f"{time_str}", True, YELLOW)
        time_text_x = (screen_width - time_text.get_width())/2
        time_text_y = mute_button_y + 15
        
        # Blit Backplate and time
        screen.blit(backplate_image, (time_text_x-(backplate_image.get_width()-time_text.get_width())/2, time_text_y-(backplate_image.get_height()-time_text.get_height())/2))
        screen.blit(time_text, (time_text_x, time_text_y))

        # Render and blit the mute button
        screen.blit(mute_button, (mute_button_x, mute_button_y))

        if len(possible_moves) == 0 and game_started:
            # If there are no valid moves for the current player, but there are still available spaces on the board
            if any(0 in row for row in board):
                print("No valid moves")
                # Switch the turn to the other player
                player_turn = 3 - player_turn
                # Get valid moves for the new player
                possible_moves = get_valid_moves()
            else:
                # If neither player has valid moves and there are no available spaces on the board, the game ends
                player1_score, player2_score = update_score()
                if player1_score > player2_score:
                    display_winner(1)
                elif player2_score > player1_score:
                    display_winner(2)
                else:
                    display_winner(0)
                game_started = False

        # Render and blit the number of wins for each player
        laps_text = font_labels.render(f"Laps", True, YELLOW)
        
        screen.blit(laps_text, (player1_tab_x + (player_tab_width- laps_text.get_width())/2, player1_tab_y + player_tab_height*2/3))
        player1_wins_text = font_numbers.render(f"{player1_wins}", True, YELLOW)
        screen.blit(player1_wins_text, (player1_tab_x + (player_tab_width- player1_wins_text.get_width())/2, 35 + player1_tab_y + player_tab_height*2/3))
        
        screen.blit(laps_text, (player2_tab_x + (player_tab_width- laps_text.get_width())/2, player2_tab_y + player_tab_height*2/3))
        player2_wins_text = font_numbers.render(f"{player2_wins}", True, YELLOW)
        screen.blit(player2_wins_text, (player2_tab_x + (player_tab_width- player2_wins_text.get_width())/2, 35 + player2_tab_y + player_tab_height*2/3))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
