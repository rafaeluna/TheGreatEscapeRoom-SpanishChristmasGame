import logging

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App

import config

if config.IS_RPI:
    import RPi.GPIO as GPIO

class WinScreen(Screen):
    def __init__(self, name: str):

        super().__init__(name=name)

        # Adding background image
        self.add_widget(Image(source="assets/img/bg.jpeg", allow_stretch=True, keep_ratio=False))

        # Add big centered text
        anchor_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        big_text = Label(
            text="¡Bravo!\nMerry Christmas\n2024",
            font_size="50sp",
            halign="center",
            valign="middle",
        )
        anchor_layout.add_widget(big_text)
        self.add_widget(anchor_layout)

        # Add images anchored to the 4 corners with a 40px margin
        corners = [
            ("assets/img/win_screen/top_left.JPG", "left", "top"),
            ("assets/img/win_screen/top_right.JPG", "right", "top"),
            ("assets/img/win_screen/bottom_left.JPG", "left", "bottom"),
            ("assets/img/win_screen/bottom_right.JPG", "right", "bottom")
        ]
        for img_source, anchor_x, anchor_y in corners:
            anchor_layout = AnchorLayout(anchor_x=anchor_x, anchor_y=anchor_y, padding=[40, 40, 40, 40])
            image = Image(source=img_source, size_hint=(None, None), allow_stretch=True)
            image.size = (400, 400)
            anchor_layout.add_widget(image)
            self.add_widget(anchor_layout)

        # Add bottm centered text
        bottom_text_layout = FloatLayout()
        bottom_text = Label(
            text="Complete for a 4-digit code",
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "bottom": 1},
            font_size="30sp"
        )
        bottom_text_layout.add_widget(bottom_text)
        self.add_widget(bottom_text_layout)

        # Setup action to restart game
        if config.IS_RPI:
            GPIO.setmode(GPIO.BCM)
            self.gpio_pin = config.GPIO_RESTART_PIN
            GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Schedule the GPIO check
            Clock.schedule_interval(self.check_gpio_input, 0.1)
        else:
            # If not on Raspberry Pi, use key event for simulation
            Window.bind(on_key_down=self.on_key_down)

    def check_gpio_input(self, dt):
        # If GPIO input detected (button pressed)
        if GPIO.input(self.gpio_pin) == GPIO.LOW:
            self.restart_full_game()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # Listen for a specific key press (e.g., space bar, keycode 32)
        if key == 114:  # Space key
            self.restart_full_game()

    def restart_full_game(self):
        logging.debug("Trying to go to WelcomeScreen from WinScreen, current screen: %s", self.manager.current)
        if (self.manager.current == self.name):
            logging.info("Restarting game from WinScreen (should go to WelcomeScreen)...")
            app = App.get_running_app()
            app.restart_music("bogus_arg")
            app.reset_all_states()
            self.manager.current = "welcome_screen"
