from typing import List
from dataclasses import dataclass

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

class MovieGameStage(Screen):


    def __init__(self, name: str, poster_filename: str, acceptable_answers: List[str], next_stage_name: str):

        super().__init__(name=name)

        # Save acceptable answers
        self.next_stage_name = next_stage_name
        self.acceptable_answers = [answer.lower() for answer in acceptable_answers]

        # Set the background color to white
        with self.canvas.before:
            Color(0, 0, 0, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # Load movie poster image into memory
        self.movie_image = Image(source=f"assets/img/movie_games/{poster_filename}")

        # Add image, input, and keyboard
        layout.add_widget(self.movie_image)
        layout.add_widget(self.get_input_layout())
        layout.add_widget(self.get_keyboard_layout())



        self.add_widget(layout)

    def get_input_layout(self):
        """Get the layout for the input section"""

        # Label and text input for user to guess the movie name
        # input_layout = BoxLayout(orientation="horizontal", spacing=5, size_hint_y=0.4)
        input_layout = GridLayout(cols=5, spacing=5, size_hint_y=0.2)

        # Label
        label = Label(text="Enter movie title:", color=(1, 1, 1, 1), size_hint_x=1)  # Black label text
        input_layout.add_widget(label)

        # Input
        self.text_input = TextInput(
            multiline=False,
            background_color=(0.8, 0, 0, 1),  # Christmasy red
            foreground_color=(1, 1, 1, 1),  # White text
            cursor_color=(1, 1, 1, 1),
            focus=True,
            size_hint_x=2,
            padding=[10, 30, 0, 0]
        )
        input_layout.add_widget(self.text_input)

        # Backspace button
        backspace_button = Button(text="< Delete", size_hint_x=0.5)
        backspace_button.bind(on_press=self.on_backspace)
        input_layout.add_widget(backspace_button)

        # Submit button
        submit_button = Button(text="Submit", size_hint_x=1)
        submit_button.bind(on_press=self.check_answer)
        input_layout.add_widget(submit_button)

        return input_layout


    def get_keyboard_layout(self):
        """Get the keyboard layout"""

        # Main layout for keyboard rows
        keyboard_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=0.75)

        # Row 0: 1234567890
        row0_layout = GridLayout(cols=10, spacing=5)
        for key in "1234567890":
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            row0_layout.add_widget(button)
        keyboard_layout.add_widget(row0_layout)

        # Row 1: QWERTYUIOP
        row1_layout = GridLayout(cols=10, spacing=5)
        for key in "QWERTYUIOP":
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            row1_layout.add_widget(button)
        keyboard_layout.add_widget(row1_layout)

        # Row 2: ASDFGHJKL
        row2_layout = GridLayout(cols=9, spacing=5, padding=[30, 0, 30, 0])  # Add padding to center keys
        for key in "ASDFGHJKL":
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            row2_layout.add_widget(button)
        keyboard_layout.add_widget(row2_layout)

        # Row 3: ZXCVBNM
        row3_layout = GridLayout(cols=7, spacing=5, padding=[150, 0, 150, 0])
        for key in "ZXCVBNM":
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            row3_layout.add_widget(button)
        keyboard_layout.add_widget(row3_layout)

        # Row 4: Spacebar
        space_layout = BoxLayout(spacing=5)
        space_button = Button(text="Space", size_hint_x=1)
        space_button.bind(on_press=self.on_space)
        space_layout.add_widget(space_button)
        keyboard_layout.add_widget(space_layout)

        return keyboard_layout

    # Event handlers for key presses
    def on_key_press(self, instance):
        """Handle key presses from the virtual keyboard."""
        if instance.text.lower() in "qwertyuiopasdfghjklzxcvbnm12345678890": # Ignore unknown input
            self.text_input.text += instance.text

    def on_backspace(self, _):
        """Handle backspace functionality."""
        self.text_input.text = self.text_input.text[:-1]

    def on_enter_key_press(self, instance):
        """Handle enter key functionality."""
        # For now, just call check_answer
        self.check_answer(instance)

    def on_space(self, _):
        """Handle space functionality."""
        if not self.text_input.text.endswith(" "): # Ignore multiple spacing
            self.text_input.text += ' '

    def check_answer(self, _):
        """Check if the answer is correct"""
        if self.text_input.text.strip().lower() in self.acceptable_answers:
            self.manager.current = self.next_stage_name

    def _update_rect(self, *args):
        """Update the background rectangle size and position."""
        self.rect.pos = self.pos
        self.rect.size = self.size
