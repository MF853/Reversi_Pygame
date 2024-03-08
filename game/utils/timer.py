import pygame

class Timer:
    def __init__(self, timer_end_callback, max_interval_sec=60):
        self.timer_end_callback = timer_end_callback
        self.max_interval_sec = max_interval_sec
        self.remaining_time_sec = max_interval_sec
        self.running = False
        self.start_ticks = 0

    def start(self):
        if not self.running:
            self.running = True
            self.start_ticks = pygame.time.get_ticks()

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.remaining_time_sec = self.max_interval_sec
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        if self.running:
            elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
            remaining_secs = int(max(self.max_interval_sec - elapsed_ticks / 1000, 0))

            if remaining_secs == 0:
                self.timer_end_callback()

            if remaining_secs != self.remaining_time_sec:
                self.remaining_time_sec = remaining_secs
                return True
            
            else:
                self.remaining_time_sec = remaining_secs
                return False

    def get_time(self):
        minutes = int(self.remaining_time_sec // 60)
        seconds = int(self.remaining_time_sec % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        return time_text