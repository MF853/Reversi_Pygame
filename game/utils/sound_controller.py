import pygame
import sys

class SoundController:
    MOVE = 'player-move.wav'
    START = 'board-start.wav'
    WIN = 'win.wav'
    BACKGROUND_1 = 'music1.wav'
    BACKGROUND_2 = 'music2.wav'
    BACKGROUND_3 = 'music3.wav'
    BACKGROUND_4 = 'music4.wav'
    BACKGROUND_5 = 'music5.wav'
    BACKGROUND_6 = 'music6.wav'

    BACKGROUND_7 = 'music7.wav'
    BACKGROUND_8 = 'music8.wav'
    BACKGROUND_9 = 'music9.wav'
    BACKGROUND_10 = 'music10.wav'
    BACKGROUND_11 = 'music11.wav'
    BACKGROUND_12 = 'music12.wav'

    def __init__(self, get_path):
        self.status = AUDIO_STATUS.IDLE
        self.get_path = get_path
        self.audio_paths = {name: value for name, value in vars(self.__class__).items() if isinstance(value, str) and not name.startswith('__')}
        self.audios = {}
        self.current_bg = 3
        self.music_playing = False

        for audio_name, audio_path in self.audio_paths.items():
            self.audios[audio_path] = self.loadAudio(audio_path)
            
            if audio_name == "BACKGROUND_1":
                break

    def loadAudio(self, audio):
        try:
            return pygame.mixer.Sound(self.get_path(audio))
        except pygame.error as e:
            print("Error loading sound file:", e)
            return None
        
    def play(self, audio, repeat = False, volume = 1.0):
        self.audios[audio].stop()

        if self.status == AUDIO_STATUS.IDLE:
            a = self.audios[audio].play(loops=0 if not repeat else -1)
            a.set_volume(volume)

    def change_music(self, music):
        if self.music_playing and self.current_bg == music + 3:
            return
        
        self.current_bg = music + 3
        
        if self.status == AUDIO_STATUS.IDLE:
            self.music_playing = False
            self.play_bg()

    def play_bg(self):
        if self.music_playing:
            return
        
        bg_k = list(self.audios.keys())[-1]

        self.audios[bg_k].stop()

        bg = list(self.audio_paths.values())[self.current_bg]
        self.audios[bg_k] = self.loadAudio(bg)

        if self.status == AUDIO_STATUS.IDLE:
            a = self.audios[bg_k].play(loops=-1)
            a.set_volume(.1)

            self.music_playing = True
        
    def toggle_mute(self):
        for audio in self.audios:
            self.audios[audio].stop()

        self.status = AUDIO_STATUS.MUTED if self.status == AUDIO_STATUS.IDLE else AUDIO_STATUS.IDLE

        if self.status == AUDIO_STATUS.IDLE:
            self.music_playing = False
            self.play_bg()
        
class AUDIO_STATUS:
    MUTED = False
    IDLE = True