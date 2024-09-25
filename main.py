"""Main Escape Room Game"""

from stages.WelcomeScreen import WelcomeScreen
from stages.MemoryGame import MemoryGameStage
from stages.MovieGame import MovieGameStage
from stages.WinScreen import WinScreen


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class EscapeRoomGame(App):

    def build(self):

        # Screen manager to switch between game stages
        sm = ScreenManager()

        # Declare stages
        welcome_screen = WelcomeScreen(name="welcome_screen")
        memory_stage_1 = MemoryGameStage("memory_stage_1", [f"assets/1_{n}.png" for n in range(1,9)])
        movie_stage_1 = MovieGameStage(name="movie_stage")
        win_stage = WinScreen(name="win_screen")

        # Add them to the Screen manager
        sm.add_widget(welcome_screen)
        sm.add_widget(memory_stage_1)
        sm.add_widget(movie_stage_1)
        sm.add_widget(win_stage)

        return sm

if __name__ == '__main__':
    EscapeRoomGame().run()
