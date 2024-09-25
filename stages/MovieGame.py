from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

class MovieGameStage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Display image (use a placeholder emoji here, but can be replaced with an actual image)
        self.movie_image = Image(source='assets/home_alone.png')  # Replace with actual image path
        layout.add_widget(self.movie_image)

        # Add text input for user to guess the movie name
        self.text_input = TextInput(hint_text="Enter movie name", multiline=False, readonly=True)  # Disable native input
        layout.add_widget(self.text_input)

        # Add custom virtual keyboard
        self.keyboard_layout = GridLayout(cols=10, spacing=5)
        keys = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for key in keys:
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            self.keyboard_layout.add_widget(button)

        # Add a backspace and spacebar
        backspace_button = Button(text='Backspace')
        backspace_button.bind(on_press=self.on_backspace)
        self.keyboard_layout.add_widget(backspace_button)

        space_button = Button(text='Space')
        space_button.bind(on_press=self.on_space)
        self.keyboard_layout.add_widget(space_button)

        layout.add_widget(self.keyboard_layout)

        # Submit button
        submit_button = Button(text="Submit", size_hint=(1, 0.2))
        submit_button.bind(on_press=self.check_answer)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def on_key_press(self, instance):
        """Handle key presses from the virtual keyboard."""
        self.text_input.text += instance.text

    def on_backspace(self, instance):
        """Handle backspace functionality."""
        self.text_input.text = self.text_input.text[:-1]

    def on_space(self, instance):
        """Handle space functionality."""
        self.text_input.text += ' '

    def check_answer(self, instance):
        correct_movie = "Home Alone"  # Example movie answer
        if self.text_input.text.strip().lower() == correct_movie.lower():
            self.manager.current = 'win_screen'
        else:
            self.text_input.text = ''  # Clear input if incorrect
