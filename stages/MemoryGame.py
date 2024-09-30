"""Memory game"""

import random
import logging
from os import PathLike
from typing import List, Optional

from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

import utils

class MemoryGameStage(Screen):

    def __init__(self, screen_name: str, img_paths: List[PathLike]):

        super().__init__(name=screen_name)

        logging.debug("Initializing memory game")

        # Raise on 0 image paths
        if len(img_paths) == 0:
            raise AssertionError("No image paths passed")

        # Save orginal paths
        self.original_image_paths = img_paths

        # Init state
        self.tiles: List[Button] = []
        self.last_pressed_tile: Optional[Button] = None

        # Init squares
        self.create_grid()
        self.create_tiles()
        self.remaining_tiles = len(self.tiles)

        # Reset before starting
        self.reset_game()

    def create_grid(self):
        """Create the grid layout"""

        logging.debug("Creating grid")

        # Calculate number of rows and cols of the grid layout
        total_squares = len(self.original_image_paths) * 2
        rows, cols = utils.find_squarest_factors(total_squares)

        # Create grid layout
        self.layout = GridLayout(cols=cols, rows=rows, spacing=70, padding=70)
        self.add_widget(self.layout)

        logging.info("Created grid of %sx%s", rows, cols)

    def create_tiles(self):
        """Create the individual tiles"""

        # Duplicate and shuffle original list of paths
        list_of_image_paths = self.original_image_paths * 2
        random.shuffle(list_of_image_paths)

        logging.info("Creating %s tiles", len(list_of_image_paths))

        # Create squares
        for img_path in list_of_image_paths:

            # Create tile and attach metadata
            tile = Button()
            tile.img_path = img_path
            tile.original_color = utils.get_random_christmas_color()
            tile.is_revealed = False
            print(img_path)

            # Attach press listener
            tile.bind(on_press=self.on_square_press)

            # Add it do the grid layour
            self.layout.add_widget(tile)

            # Add it to the list of tiles
            self.tiles.append(tile)

            logging.info("Created tile with background image: %s", img_path)

    def reset_game(self):
        """Sets the game to an initial state, assuming the grid and tiles have already been created"""

        logging.info("Resetting global state")

        # Reset global state
        if (self.remaining_tiles) != len(self.tiles):
            self.remaining_tiles += 1
        self.last_pressed_tile = None

        # Reset tiles' state (only those that are not correct)
        for tile in self.tiles:
            if tile.is_revealed:
                continue
            tile.canvas.after.clear()
            tile.background_color = tile.original_color
            tile.background_normal = ''
            tile.interactions_enabled = True


    def on_square_press(self, instance):
        """Logic when pressing each button"""

        # Do nothing if interactions are not enabled
        if not instance.interactions_enabled:
            return

        logging.info("Pressed square")

        # Do nothing if the square was already pressed
        if instance.background_normal == instance.img_path:
            return

        # Always reveal tile
        logging.info("Revealing tile")
        # instance.background_normal = instance.img_path
        self.set_tile_image_with_aspect_ratio(instance, instance.img_path)
        instance.background_color = (0, 0, 0, 0)

        # If we made wrong, disable interactions and reset grid after 2 seconds
        if (self.last_pressed_tile is not None) and (self.last_pressed_tile.img_path != instance.img_path):
            logging.info("Wrong tile pressed")
            self.disable_tiles()
            Clock.schedule_once(self.reset_after_fail, 2)
            return

        # -- Assume correct press


        # Deduct remaining stiles
        self.remaining_tiles -= 1

        logging.info("Remaining tiles: %s", self.remaining_tiles)

        # Set last pressed square accordingly
        if self.last_pressed_tile is None:
            self.last_pressed_tile = instance

            logging.info("Current tile is beggining of new pair")
        else:
            self.last_pressed_tile.is_revealed = True
            self.last_pressed_tile = None
            instance.is_revealed = True
            logging.info("Current tile revealed last tile")

        # Check if we finished
        if self.remaining_tiles == 0:
            Clock.schedule_once(self.go_to_next_stage, 2)

    def set_tile_image_with_aspect_ratio(self, tile, img_path):
        """Set the background image for a tile while preserving the aspect ratio."""

        # Load the image
        image = CoreImage(img_path)

        # Get the original image size
        img_width, img_height = image.size

        # Clear the canvas before drawing new image
        with tile.canvas.after:
            # Add a white background to make the image stand out
            self.rect = Rectangle(texture=image.texture, size=tile.size, pos=tile.pos)
            self.update_background(tile, img_width, img_height)

    def update_background(self, tile, img_width, img_height):
        """Update the image size while maintaining aspect ratio."""

        # Get the size of the tile
        tile_width, tile_height = tile.size

        # Calculate aspect ratios
        tile_ratio = tile_width / tile_height
        img_ratio = img_width / img_height

        # Adjust the image to fit within the tile while preserving aspect ratio
        if tile_ratio > img_ratio:
            # Tile is wider than the image; fit based on height
            new_height = tile_height
            new_width = new_height * img_ratio
        else:
            # Tile is taller than the image; fit based on width
            new_width = tile_width
            new_height = new_width / img_ratio

        # Set the rectangle's size and position to center it
        self.rect.size = (new_width, new_height)
        self.rect.pos = (tile.center_x - new_width / 2, tile.center_y - new_height / 2)

    def disable_tiles(self):
        for tile in self.tiles:
            tile.interactions_enabled = False
        logging.info("Disabled all tiles")

    def reset_after_fail(self, _):
        self.reset_game()

    def go_to_next_stage(self, _):
        logging.info("Going to next stage")
        self.manager.current = 'movie_stage'
