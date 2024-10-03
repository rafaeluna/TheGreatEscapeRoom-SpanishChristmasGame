"""Main Escape Room Game"""

import logging
import os

from stages.WelcomeScreen import WelcomeScreen
from stages.RoundScreen import RoundScreen
from stages.MemoryGame import MemoryGameStage
from stages.MovieGame import MovieGameStage
from stages.WinScreen import WinScreen


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
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

        # -- Init

        # Init bg music
        self.init_loop_bg_music()
        sm.add_widget(WelcomeScreen(name="welcome_screen"))

        # -- ROUND 1

        # Memory
        sm.add_widget(MemoryGameStage(
            "memory_stage_1",
            [f"assets/img/memory_games/1_{n}.png" for n in range(1,3)],
            "movie_1"
        ))
        # Movie - Polar Express
        sm.add_widget(MovieGameStage(
            "movie_1", "01_polar_express.jpg",
            [
                "the polar express",
                "polar express",
                "pe"
            ],
            "round_2"
        ))

        # -- ROUND 2

        # Round
        sm.add_widget(RoundScreen("round_2", 2, "memory_stage_2"))
        # Memory
        sm.add_widget(MemoryGameStage(
            "memory_stage_2",
            [f"assets/img/memory_games/2_{n}.png" for n in range(1,3)],
            "movie_2"
        ))
        # Movie - Santa Clause 2
        sm.add_widget(MovieGameStage(
            "movie_2", "02_santa_clause_2.jpg",
            [
                "the santa clause two",
                "santa clause two",
                "sct"
            ],
            "round_3"
        ))

        # -- ROUND 3

        # Round
        sm.add_widget(RoundScreen("round_3", 3, "memory_stage_3"))
        # Memory
        sm.add_widget(MemoryGameStage(
            "memory_stage_3",
            [f"assets/img/memory_games/3_{n}.png" for n in range(1,3)],
            "movie_3"
        ))
        # Movie – Elf
        sm.add_widget(MovieGameStage("movie_3", "03_elf.jpg", ["elf"], "win_screen"))

        # -- Final screen
        sm.add_widget(WinScreen(name="win_screen"))

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

    def play_next_track(self, _):

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
