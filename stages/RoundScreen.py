"""Screen for a round"""

from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout

class RoundScreen(Screen):
    def __init__(self, name: str, round_number: int, next_stage_name: str):

        super().__init__(name=name)
        self.next_stage_name = next_stage_name

        # Adding background image
        self.add_widget(Image(source="assets/img/bg.jpeg", allow_stretch=True, keep_ratio=False))

        # Add big centered text
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        big_text = Label(text=f"Round {round_number}", font_size="50sp")
        anchor_layout.add_widget(big_text)
        self.add_widget(anchor_layout)

    def on_touch_down(self, _):
        """Detect any touch/click event and go to the next screen"""
        self.manager.current = self.next_stage_name
