import pygame
from utils.board import *
import sys
from utils.widgets import *
from utils.timer import Timer
from utils.sound_controller import SoundController

class Reversi:
    def __init__(self, setup):
        # Game variables
        self.state = GAME_STATE.OVERLAY

        # Start game music variable
        self.bg_music_started = False
        
        # Capturing the created instance of setup
        self.setup = setup
        
        # Creating an instance of the game board
        self.board = Board(
            (self.setup.screen_width * .275, self.setup.screen_height * .155), 
            (self.setup.screen_width * .45, self.setup.screen_height * .802), 
            self.set_info,
            lambda: self.end_game(GAME_STATE.WIN),
        )

        # Creating the timer
        self.timer = Timer(timer_end_callback = self.skip)

        # Loading the background image
        self.loadBackgroundImage()

        # Loading the audio
        self.sound_controller = SoundController(self.setup.audioAssetPath)

    # def skip(self):
    #     self.board.user_skip()
    #     self.timer.reset()

    def skip(self):
        self.end_game(GAME_STATE.SURRENDER)

    def set_info(self, info):
        self.info_started = True

        self.info = info
        self.start_time = pygame.time.get_ticks()

        self.draw_info()

    def draw_info(self):
        if self.info != "":
            self.info_textbox.text = self.info
            self.info_textbox.color = (0, 0, 0, 80)

    def clear_info(self):
        self.info_started = False

        if self.info != "":
            self.info = ""
            self.info_textbox.text = self.info
            self.info_textbox.color = (0, 0, 0, 0)

    def loadBackgroundImage(self):
        self.background_n_image = pygame.image.load(self.setup.imageAssetPath("background_normal.jpg")).convert()
        self.background_n_image = pygame.transform.scale(self.background_n_image, (self.setup.screen_width, self.setup.screen_height))
        
        self.background_w_image = pygame.image.load(self.setup.imageAssetPath("background_branco.jpg")).convert()
        self.background_w_image = pygame.transform.scale(self.background_w_image, (self.setup.screen_width, self.setup.screen_height))
        
        self.background_b_image = pygame.image.load(self.setup.imageAssetPath("background_preto.jpg")).convert()
        self.background_b_image = pygame.transform.scale(self.background_b_image, (self.setup.screen_width, self.setup.screen_height))
        
        self.background_w_image_pisca = pygame.image.load(self.setup.imageAssetPath("background_branco_pisca.jpg")).convert()
        self.background_w_image_pisca = pygame.transform.scale(self.background_w_image_pisca, (self.setup.screen_width, self.setup.screen_height))
        
        self.background_b_image_pisca = pygame.image.load(self.setup.imageAssetPath("background_preto_pisca.jpg")).convert()
        self.background_b_image_pisca = pygame.transform.scale(self.background_b_image_pisca, (self.setup.screen_width, self.setup.screen_height))
        
        self.background_numbers = pygame.image.load(self.setup.imageAssetPath("background_numbers.jpg")).convert_alpha()
        self.background_numbers = pygame.transform.scale(self.background_numbers, (self.setup.screen_width, self.setup.screen_height))
        
        


    def start_game(self):
        # Start the timer
        self.timer.start()

        if not self.bg_music_started:
            self.bg_music_started = True
            self.sound_controller.play_bg()

        self.sound_controller.play(SoundController.START, volume=.5)

        self.set_state(GAME_STATE.PLAYING)

    def set_state(self, state):
        self.state = state

    def end_game(self, state):
        self.set_state(state)
        
        if state is GAME_STATE.WIN:
            # Stop the timer
            self.timer.stop()

            # Play the win sound
            self.sound_controller.play(SoundController.WIN, volume=.5)

        elif state is GAME_STATE.SURRENDER:
            # Stop the timer
            self.timer.stop()

            # Reset the game
            self.board.surrender()

            # Play the win sound
            self.sound_controller.play(SoundController.WIN, volume=.5)
        
        else:
            # Stop and reset the timer
            self.timer.reset()
            self.timer.stop()

            self.board.reset()

    def play(self):
        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Create the start game overlay
        self.start_overlay = Overlay(self.board.position, self.board.size, color=(0, 0, 0, 180))

        # Create the mute button
        mute_button_size = (self.setup.screen_width * .055, self.setup.screen_height * .1)
        mute_button_position = ((self.setup.screen_width - mute_button_size[0]) * .084, (self.setup.screen_height - mute_button_size[1]) * .03)
        self.mute_button = CircleButton(mute_button_position, mute_button_size)

        # Create the end game button
        end_game_button_size = (self.setup.screen_width * .22, self.setup.screen_height * .082)
        end_game_button_position = ((self.setup.screen_width - end_game_button_size[0]) * .243, (self.setup.screen_height - end_game_button_size[1]) * .039)
        self.end_game_button = RoundedRectBorderButton(end_game_button_position, end_game_button_size)

        # Create the timer text
        timer_textbox_size = (self.setup.screen_width * .152, self.setup.screen_height * .082)
        timer_textbox_position = ((self.setup.screen_width - timer_textbox_size[0]) * .5, (self.setup.screen_height - timer_textbox_size[1]) * .045)
        timer_text = "00:00"
        self.timer_textbox = TextBox(timer_textbox_position, timer_textbox_size, timer_text, self.setup.font_normal, self.setup.text_color)

        # Create the start game button
        start_game_button_size = (self.setup.screen_width * .22, self.setup.screen_height * .082)
        start_game_button_position = ((self.setup.screen_width - start_game_button_size[0]) * .758, (self.setup.screen_height - start_game_button_size[1]) * .039)
        self.start_game_button = RoundedRectBorderButton(start_game_button_position, start_game_button_size)

        # Create the points (White) text
        white_points_textbox_size = (self.setup.screen_width * .1, self.setup.screen_height * .15)
        white_points_textbox_position = ((self.setup.screen_width - white_points_textbox_size[0]) * .125, (self.setup.screen_height - white_points_textbox_size[1]) * .55)
        white_points_text = str(self.board.cnt[O])
        self.white_points_textbox = TextBox(white_points_textbox_position, white_points_textbox_size, white_points_text, self.setup.font_big, self.setup.text_color)

        # Create the laps (White) text
        white_wins_textbox_size = (self.setup.screen_width * .1, self.setup.screen_height * .15)
        white_wins_textbox_position = ((self.setup.screen_width - white_wins_textbox_size[0]) * .125, (self.setup.screen_height - white_wins_textbox_size[1]) * .79)
        white_wins_text = str(self.board.wins[O])
        self.white_wins_textbox = TextBox(white_wins_textbox_position, white_wins_textbox_size, white_wins_text, self.setup.font_big, self.setup.text_color)

        # Create the points (Black) text
        black_points_textbox_size = (self.setup.screen_width * .1, self.setup.screen_height * .15)
        black_points_textbox_position = ((self.setup.screen_width - black_points_textbox_size[0]) * .875, (self.setup.screen_height - black_points_textbox_size[1]) * .55)
        black_points_text = str(self.board.cnt[X])
        self.black_points_textbox = TextBox(black_points_textbox_position, black_points_textbox_size, black_points_text, self.setup.font_big, self.setup.text_color)

        # Create the laps (Black) text
        black_wins_textbox_size = (self.setup.screen_width * .1, self.setup.screen_height * .15)
        black_wins_textbox_position = ((self.setup.screen_width - black_wins_textbox_size[0]) * .875, (self.setup.screen_height - black_wins_textbox_size[1]) * .79)
        black_wins_text = str(self.board.wins[X])
        self.black_wins_textbox = TextBox(black_wins_textbox_position, black_wins_textbox_size, black_wins_text, self.setup.font_big, self.setup.text_color)

        # Create the info text
        info_textbox_size = (self.setup.screen_width * .455, self.setup.screen_height * .05)
        info_textbox_position = ((self.setup.screen_width - info_textbox_size[0]) * .5, (self.setup.screen_height - info_textbox_size[1]) * .15)
        self.info = ""
        self.info_started = False
        self.info_textbox = TextBox(info_textbox_position, info_textbox_size, self.info, self.setup.font_normal, self.setup.text_color)

        # Create the music buttons
        rows = 2
        cols = 3
        music_button_size = (self.setup.screen_width * .0255, self.setup.screen_height * .0445)
        music_button_padding = (self.setup.screen_width * .003, self.setup.screen_height * .007)
        music_button_between = self.setup.screen_width * .676
        self.music_buttons = [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(2)]
        music_initial_position = ((self.setup.screen_width - music_button_size[0]) * .124, (self.setup.screen_height - music_button_size[1]) * .87)
        for b, _ in enumerate(self.music_buttons):
            for r, _ in enumerate(self.music_buttons[b]):
                for c, _ in enumerate(self.music_buttons[b][r]):
                    p_in = ((music_button_size[0] + music_button_padding[0]) * c, (music_button_size[1] + music_button_padding[1]) * r)
                    p_out = (music_button_between * b, 0)
                    p_box = tuple(map(sum, zip(music_initial_position, p_in, p_out)))
                    self.music_buttons[b][r][c] = Button(p_box, music_button_size)

        # Main loop
        running = 1
        while running:
            for event in pygame.event.get():
                # Check for key presses to quit fullscreen
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         running = 0

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mute_button.is_pressed(event.pos):
                        self.sound_controller.toggle_mute()

                    elif self.start_game_button.is_pressed(event.pos):
                        if self.state is GAME_STATE.OVERLAY:
                            self.start_game()

                    elif self.end_game_button.is_pressed(event.pos):
                        if self.state is GAME_STATE.PLAYING:
                            self.end_game(GAME_STATE.SURRENDER)

                        else:
                            self.end_game(GAME_STATE.OVERLAY)

                    else:
                        for b, _ in enumerate(self.music_buttons):
                            for r, _ in enumerate(self.music_buttons[b]):
                                for c, _ in enumerate(self.music_buttons[b][r]):
                                    if self.music_buttons[b][r][c].is_pressed(event.pos):
                                        linear_i = 6*b + 3*r + c
                                        self.sound_controller.change_music(linear_i)
                                        break
                                    
                        if self.state is GAME_STATE.PLAYING and not self.board.moving:
                            result = self.board.catch_press(event.pos)

                            if result != None:
                                row, col = result[0], result[1]
                                if self.board.user_move(row, col):
                                    self.timer.reset()
                                    self.sound_controller.play(SoundController.MOVE)

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Draw background image
            if self.state is GAME_STATE.PLAYING:
                if self.board.current_player == X:
                    self.setup.screen.blit(self.background_b_image, (0, 0))
                    if pygame.time.get_ticks() % 1000 < 500:  # Blink every half second
                        self.setup.screen.blit(self.background_b_image_pisca, (0, 0))
                else:
                    self.setup.screen.blit(self.background_w_image, (0, 0))
                    if pygame.time.get_ticks() % 1000 < 500:  # Blink every half second
                        self.setup.screen.blit(self.background_w_image_pisca, (0, 0))
            else:
                self.setup.screen.blit(self.background_n_image, (0, 0))

            #Draw Numbers
            self.setup.screen.blit(self.background_numbers, (0,0))

            # Draw the mute button
            self.mute_button.update_status(mouse_pos)
            self.mute_button.draw(self.setup.screen)

            # Draw the end game button
            self.end_game_button.update_status(mouse_pos, disabled = self.state is GAME_STATE.OVERLAY)
            self.end_game_button.draw(self.setup.screen)

            # Draw the timer text box
            self.timer.update()
            self.timer_textbox.text = self.timer.get_time()
            self.timer_textbox.draw(self.setup.screen)

            # Draw the start game button
            self.start_game_button.update_status(mouse_pos, disabled = self.state is not GAME_STATE.OVERLAY)
            self.start_game_button.draw(self.setup.screen)

            # Draw the White score
            white_points_text = str(self.board.cnt[O])
            self.white_points_textbox.text = white_points_text
            self.white_points_textbox.draw(self.setup.screen)

            # Draw the White laps
            white_wins_text = str(self.board.wins[O])
            self.white_wins_textbox.text = white_wins_text
            self.white_wins_textbox.draw(self.setup.screen)

            # Draw the Black score
            black_points_text = str(self.board.cnt[X])
            self.black_points_textbox.text = black_points_text
            self.black_points_textbox.draw(self.setup.screen)

            # Draw the Black laps
            black_wins_text = str(self.board.wins[X])
            self.black_wins_textbox.text = black_wins_text
            self.black_wins_textbox.draw(self.setup.screen)

            # Draw the board
            if self.state is not GAME_STATE.OVERLAY:
                if self.board.moving:
                    self.board.move_slowly()
                self.board.build_board(self.setup.screen)

            # Draw the overlay
            if self.state is not GAME_STATE.PLAYING :
                self.start_overlay.draw(self.setup.screen)

            if self.info_started:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.start_time
                if elapsed_time >= 3000:
                    self.clear_info()

            for b, _ in enumerate(self.music_buttons):
                for r, _ in enumerate(self.music_buttons[b]):
                    for c, _ in enumerate(self.music_buttons[b][r]):
                        self.music_buttons[b][r][c].update_status(mouse_pos, disabled=False)
                        self.music_buttons[b][r][c].draw(self.setup.screen)
            
            self.info_textbox.draw(self.setup.screen)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

class GAME_STATE:
    PLAYING = (1,1)
    WIN = (1,0)
    SURRENDER = (0,1)
    OVERLAY = (0,0)