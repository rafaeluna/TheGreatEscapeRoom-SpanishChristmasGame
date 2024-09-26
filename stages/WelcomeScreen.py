from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the image widget, setting `allow_stretch` to True to let the image expand, and
        # `keep_ratio` to True to preserve the aspect ratio.
        background_image = Image(source="assets/feliz_navidad_welcome_screen.jpeg", allow_stretch=True, keep_ratio=True)

        # Set the background color to white using Canvas instructions
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            # Bind size and pos to ensure the background fills the screen
            self.bind(size=self.update_background, pos=self.update_background)

        # Create a layout for the content overlay (like the label)
        layout = BoxLayout(orientation='vertical', padding=20)

        # Add the image as a background (behind other widgets)
        self.add_widget(background_image)

        # Add the label layout on top of the image
        self.add_widget(layout)

    def on_touch_down(self, touch):
        """Go to stage 1"""
        self.manager.current = "memory_stage_1"
        return super().on_touch_down(touch)

    def update_background(self, *args):
        """Update the size and position of the background rectangle."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
