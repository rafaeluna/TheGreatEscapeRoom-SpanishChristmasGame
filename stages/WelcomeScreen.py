import logging

from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App

import config

if config.IS_RPI:
    import RPi.GPIO as GPIO

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the image widget, setting `allow_stretch` to True to let the image expand, and
        # `keep_ratio` to True to preserve the aspect ratio.
        background_image = Image(source="assets/img/fnws2.png", allow_stretch=True, keep_ratio=False)

        # Set the background color to white using Canvas instructions
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.bg_rect = Rectangle(size=(3000, 3000), pos=self.pos)

        # Create a layout for the content overlay (like the label)
        layout = BoxLayout(orientation='vertical')

        # Add the image as a background (behind other widgets)
        self.add_widget(background_image)

        # Add the label layout on top of the image
        self.add_widget(layout)

        if config.IS_RPI:
            GPIO.setmode(GPIO.BCM)
            self.gpio_pin = config.GPIO_START_PIN
            GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Schedule the GPIO check
            Clock.schedule_interval(self.check_gpio_input, 0.1)

        # Setup action to get to next screen
        Window.bind(on_key_down=self.on_key_down)

    def check_gpio_input(self, dt):
        # If GPIO input detected (button pressed)
        if GPIO.input(self.gpio_pin) == GPIO.LOW:
            self.go_to_next_screen()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # Listen for a specific key press (e.g., space bar, keycode 32)
        if key == 32:  # Space key
            self.go_to_next_screen()

    def go_to_next_screen(self):
        logging.debug("Trying to go to next screen from WelcomeScreen, current screen: %s", self.manager.current)
        if self.manager.current == self.name:
            logging.info("Going from Welcome Screen to Memory Stage 1")
            # Switch stage
            self.manager.current = "memory_stage_1"
            # Schedule BGM in the backgorund to avoid delays
            Clock.schedule_once(lambda dt: App.get_running_app().play_next_track("bogus_arg"), 0.1)

    def update_background(self, *args):
        """Update the size and position of the background rectangle."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
