"""Main Escape Room Game"""

import logging
import os

from stages.WelcomeScreen import WelcomeScreen
from stages.MemoryGame import MemoryGameStage
from stages.MovieGame import MovieGameStage
from stages.WinScreen import WinScreen


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class EscapeRoomGame(App):

    def build(self):

        # Screen manager to switch between game stages
        sm = ScreenManager()
        logging.info("***** Running The Great Escape Room -- Spanish Christmas Level *****")
        logging.info("IS_RPI: %s", config.IS_RPI)

        # Init bg music
        self.init_loop_bg_music()

        # Declare stages
        welcome_screen = WelcomeScreen(name="welcome_screen")
        memory_stage_1 = MemoryGameStage("memory_stage_1", [f"assets/img/1_{n}.png" for n in range(1,9)])
        movie_stage_1 = MovieGameStage(name="movie_stage")
        win_stage = WinScreen(name="win_screen")

        # Add them to the Screen manager
        sm.add_widget(welcome_screen)
        sm.add_widget(memory_stage_1)
        sm.add_widget(movie_stage_1)
        sm.add_widget(win_stage)

        return sm

    def init_loop_bg_music(self):

        # Load all files from the assets/music dir
        bg_music_dir = "assets/bg_loop_music"
        self.music_files = [
            os.path.join(bg_music_dir, filename)
            for filename in sorted(os.listdir(bg_music_dir))
            if (
                os.path.isfile(os.path.join(bg_music_dir, filename))
                and filename.endswith(".mp3") # Ignore .DS_Store annoyingly
            )
        ]

        logging.info("Initializing BGM with %s tracks", len(self.music_files))

        # Init state
        self.current_track_index = 0
        self.current_music = None

        # Start playing the first track
        Clock.schedule_once(self.play_next_track, 0)

    def play_next_track(self, _):

        logging.debug("Playing next track")

        # Unload current music if existing
        if self.current_music:
            self.current_music.unload()

        # Load current idx
        next_track_filename = self.music_files[self.current_track_index]
        self.current_music = SoundLoader.load(next_track_filename)

        # Play loaded music
        self.current_music.play()
        logging.info("Playing BGM %s", next_track_filename)

        # Schedule next track when current one finishes
        self.current_music.bind(on_stop=self.play_next_track)

        # Update the index to the next track
        self.current_track_index = (self.current_track_index + 1) % len(self.music_files)

    def on_stop(self):
        # Stop the current track when the app is closed
        if self.current_music:
            self.current_music.stop()

if __name__ == '__main__':
    EscapeRoomGame().run()
