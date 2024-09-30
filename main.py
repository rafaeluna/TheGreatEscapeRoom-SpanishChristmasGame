"""Main Escape Room Game"""

import logging
import os

from stages.WelcomeScreen import WelcomeScreen
from stages.MemoryGame import MemoryGameStage
from stages.MovieGame import MovieGameStage, MovieGameData
from stages.WinScreen import WinScreen


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import config

class EscapeRoomGame(App):

    def build(self):

        # Screen manager to switch between game stages
        sm = ScreenManager()
        logging.info("***** Running The Great Escape Room -- Spanish Christmas Level *****")
        logging.info("IS_RPI: %s", config.IS_RPI)

        # Init bg music
        # self.init_loop_bg_music()

        # Declare stages
        # welcome_screen = WelcomeScreen(name="welcome_screen")
        # memory_stage_1 = MemoryGameStage("memory_stage_1", [f"assets/img/1_{n}.png" for n in range(1,9)])

        # Movie Stage 1 - Polar Express
        movie_stage_1 = MovieGameStage(MovieGameData(
            "movie_1", "01_polar_express.jpg",
            [
                "the polar express",
                "polar express",
            ],
            "round_2_welcome"
        ))

        # Movie Stage 2 - Santa Clause 2
        movie_stage_2 = MovieGameStage(MovieGameData(
            "movie_2", "02_santa_clause_2.jpg",
            [
                "the santa clause two",
                "santa clause two",
            ],
            "round_3_welcome"
        ))

        # Movie Stage 3 - Elf
        movie_stage_3 = MovieGameStage(MovieGameData("movie_3", "03_elf.jpg", ["elf"], "win_screen"),)

        win_stage = WinScreen(name="win_screen")

        # Add them to the Screen manager
        # sm.add_widget(welcome_screen)
        # sm.add_widget(memory_stage_1)
        sm.add_widget(movie_stage_3)
        sm.add_widget(win_stage)

        return sm

    def init_loop_bg_music(self):

        # Get mp3 filepaths from the assets/music dir
        bg_music_dir = "assets/bg_loop_music"
        music_filepaths = [
            os.path.join(bg_music_dir, filename)
            for filename in sorted(os.listdir(bg_music_dir))
            if (
                os.path.isfile(os.path.join(bg_music_dir, filename))
                and filename.endswith(".mp3") # Ignore .DS_Store annoyingly
            )
        ]

        # Load them all into memory
        self.bgm_tracks = [SoundLoader.load(file) for file in music_filepaths]

        logging.info("Initializing BGM with %s tracks", len(self.bgm_tracks))

        # Init state
        self.current_track_index = 0
        self.current_music = None

    def play_next_track(self):

        logging.debug("Playing next track")

        # Get current track
        current_track = self.bgm_tracks[self.current_track_index]

        # Play it
        current_track.play()

        # Schedule next track when current one finishes
        current_track.bind(on_stop=self.play_next_track)

        # Update the index to the next track
        self.current_track_index = (self.current_track_index + 1) % len(self.bgm_tracks)

if __name__ == '__main__':
    EscapeRoomGame().run()
