import pygame
import os

class Setup:
    def __init__(self):
        # Initializes the audio mixer
        self.initAudioMixer(pre=True)

        # Initializes the game
        pygame.init()

        # pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN])
        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])

        # Initializes the audio mixer again
        self.initAudioMixer(pre=False)

        # Get the current path to the files
        self.current_dir = os.path.dirname(__file__)
        self.current_dir = os.path.dirname(self.current_dir)

        # Initializes the screen parameters
        self.initScreen()

        # Initializes the fonts
        self.initFonts()

    def initScreen(self):
        # Get the display size
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        # Set up the screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        # self.modes = pygame.display.list_modes()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

        # Set the caption for the window
        pygame.display.set_caption("Reversi")
    
    def initFonts(self):
        # Set up font
        self.font_normal = pygame.font.Font(self.fontAssetPath("Oswald/Oswald-SemiBold.ttf"), 80)
        self.font_big = pygame.font.Font(self.fontAssetPath("Oswald/Oswald-SemiBold.ttf"), 150)
        self.text_color = (255, 202, 0)

    def initAudioMixer(self, pre):
        if pre:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.mixer.init()
        else:
            pygame.mixer.quit()
            pygame.mixer.init(44100, -16, 1, 512)

    def fontAssetPath(self, font):
        print(os.path.join(self.current_dir, f"assets/fonts/{font}"))
        return os.path.join(self.current_dir, f"assets/fonts/{font}")

    def audioAssetPath(self, audio):
        print(os.path.join(self.current_dir, f"assets/audio/{audio}"))
        return os.path.join(self.current_dir, f"assets/audio/{audio}")

    def imageAssetPath(self, img):
        print(os.path.join(self.current_dir, f"assets/img/{img}"))
        return os.path.join(self.current_dir, f"assets/img/{img}")