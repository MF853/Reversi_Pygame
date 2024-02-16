import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
FPS = 60

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (113, 167, 196)

# Placeholder asset filenames for menu
MENU_BACKGROUND_IMAGE = "./ReversiAssets/Tela_inicialBoard.png"
START_BUTTON_IMAGE = "./ReversiAssets/StartGameButton.png"
SHUTDOWN_BUTTON_IMAGE = "./FinalAssets/shutdownButton.png"
GAME_NAME_LABEL_IMAGE = "./FinalAssets/reversi.png"

def draw_rounded_rect(surface, color, rect, border_radius, width=0):
    """
    Draw a rectangle with rounded corners on a surface.
    """
    radius = border_radius
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0,0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
    pygame.draw.circle(circle, color, (radius, radius), radius)
    circle.set_colorkey((0,0,0))

    rectangle.blit(circle, (0, 0))
    rectangle.blit(circle, (0, rect.height - radius*2))
    rectangle.blit(circle, (rect.width - radius*2, 0))
    rectangle.blit(circle, (rect.width - radius*2, rect.height - radius*2))

    rect_tmp = pygame.Rect(0, radius, rect.width, rect.height - radius*2)
    rect_tmp2 = pygame.Rect(radius, 0, rect.width - radius*2, rect.height)

    pygame.draw.rect(rectangle, color, rect_tmp)
    pygame.draw.rect(rectangle, color, rect_tmp2)

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha), special_flags=pygame.BLEND_RGBA_MIN)

    surface.blit(rectangle, pos)
def main_menu():
    menu_running = True

    # Set up screen
    screen = pygame.display.set_mode((1920, 1080)) #pygame.FULLSCREEN
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Reversi Main Menu")
    clock = pygame.time.Clock()

    menu_background = pygame.image.load(MENU_BACKGROUND_IMAGE)
    start_button = pygame.image.load(START_BUTTON_IMAGE)
    shutdown_button = pygame.image.load(SHUTDOWN_BUTTON_IMAGE)
    game_name_label = pygame.image.load(GAME_NAME_LABEL_IMAGE)
    screen_width, screen_height = screen.get_size()
    menu_background_width, menu_background_height = menu_background.get_size()

    # Scale images
    menu_background = pygame.transform.scale(menu_background, (menu_background_width*screen_height/menu_background_height, screen_height))
    start_button = pygame.transform.scale(start_button, (int(start_button.get_width() * 100 / start_button.get_height()), 100))
    shutdown_button = pygame.transform.scale(shutdown_button, (50, 50))
    game_name_label = pygame.transform.scale(game_name_label, (int(game_name_label.get_width() * 0.8), int(game_name_label.get_height() * 0.8)))
    
    start_button_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    shutdown_button_rect = shutdown_button.get_rect(bottomleft=(10, HEIGHT - 10))
    game_name_label_rect = game_name_label.get_rect(midtop=(WIDTH // 2, 150))

    def confirm(message):
        """
        Display a confirmation box with Yes and No buttons.
        Returns True if Yes is clicked, False if No is clicked.
        """
        font = pygame.font.SysFont(None, 24)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(400, 300))
        draw_rounded_rect(screen, WHITE, (300, 250, 200, 100), 10)
        pygame.draw.rect(screen, BLACK, (300, 250, 200, 100), 2, 10)
        screen.blit(text, text_rect)

        yes_button = pygame.Rect(350, 300, 50, 30)
        no_button = pygame.Rect(450, 300, 50, 30)

        pygame.draw.rect(screen, BLACK, yes_button)
        pygame.draw.rect(screen, BLACK, no_button)

        yes_text = font.render("Yes", True, WHITE)
        no_text = font.render("No", True, WHITE)

        screen.blit(yes_text, (360, 305))
        screen.blit(no_text, (460, 305))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if yes_button.collidepoint(x, y):
                        return True
                    elif no_button.collidepoint(x, y):
                        return False

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                if start_button_rect.collidepoint(mouseX, mouseY):
                    # Run reversi.py
                    subprocess.run(["python", "reversi.py"])
                    return  # Exit main menu loop after starting the game

                elif shutdown_button_rect.collidepoint(mouseX, mouseY):
                    # Ask user if they want to shut down
                    response = confirm("Are you sure you want to shutdown?")
                    if response:
                        # Shutdown system
                        print("Shutting down...")
                        # Uncomment the line below to actually shut down the system
                        # subprocess.run(["shutdown", "/s", "/t", "0"])
                    else:
                        pass  # Do nothing if user selects No

        screen.fill(BLUE)  # Fill the background with green
        # Calculate the position to center the background
        bg_x = (WIDTH - menu_background.get_width()) // 2
        bg_y = (HEIGHT - menu_background.get_height()) // 2
        #screen.blit(menu_background, (bg_x, bg_y))
        screen.blit(start_button, start_button_rect)
        screen.blit(shutdown_button, shutdown_button_rect)
        screen.blit(game_name_label, game_name_label_rect)

        # Draw "Reversi" label
        draw_rounded_rect(screen, BLACK, (WIDTH // 2 - 50, 450, 100, 30), 10)
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 50, 450, 100, 30), 0, 10)
        font = pygame.font.SysFont(None, 24)
        text = font.render("Reversi", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, 465))
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()
