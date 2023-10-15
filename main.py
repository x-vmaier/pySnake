import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from time import sleep
import random

# Definition der Konstanten für das Spielfenster
WINDOW_WIDTH = 670
WINDOW_HEIGHT = 670
GRID_LENGTH = 32
SLEEP_TIME = 0.2
NUMBER_BOARD_FIELDS = 20

class PlaneGame:
    def __init__(self):
        """Initialisiert das Plane-Spiel und das Spielfenster."""
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.grid_length = GRID_LENGTH
        self.sleep_time = SLEEP_TIME
        self.number_board_fields = NUMBER_BOARD_FIELDS
        self.num_exhaust_plumes = 10
        self.direction = (0, 0)

        # Definiert die Begrenzungen des Spielfelds: 20 Pixel Abstand von jeder Seite
        self.x_left = 16
        self.y_up = 16
        self.x_right = self.x_left + self.number_board_fields * self.grid_length
        self.y_down = self.y_up + self.number_board_fields * self.grid_length

        # Setzt die Startposition des Fliegers
        self.start_position = [
            self.x_left + self.grid_length * 0.5 + self.number_board_fields // 2 * self.grid_length,
            self.y_up + self.grid_length * 0.5 + self.number_board_fields // 2 * self.grid_length,
        ]
        self.plane_position = list(self.start_position)

        # Erstellt leere Arrays für Spielobjekte
        self.exhaust_plumes = []
        self.fuel = None
        self.fuel_position = []

        # Erstellt das Spielfenster
        self.window = tk.Tk()
        self.window.title('Snake')
        self.canvas = Canvas(self.window, height=self.height, width=self.width, bg='white')
        self.canvas.pack()

        # Lädt die Tiles für den Hintergrund
        self.image_objects = {}
        self.images = {
            'plane': 'images/plane.png',
            'exhaust' : 'images/exhaust.png',
            'fuel': 'images/fuel.png',
            0: 'images/tiles/grass.png',
            1: 'images/tiles/tree.png',
            2: 'images/tiles/tree_pair.png',
            3: 'images/tiles/house.png',
            4: 'images/tiles/ocean.png',
            5: 'images/tiles/ocean_border (3).png',
            6: 'images/tiles/ocean_border (4).png',
            7: 'images/tiles/ocean_border (8).png',
            8: 'images/tiles/ocean_border (5).png',
        }
        self.load_images()

        # Definiert die Tilemap
        self.tilemap = [
            [1, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 2],
            [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2],
            [0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 1, 2],
            [0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 8, 5, 5, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 4, 4, 4],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 5, 5, 6, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 6, 4, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
        self.draw_tilemap()

        # Zeichnet die Begrenzungslinien des Spielfelds
        self.canvas.create_line(self.x_left, self.y_up, self.x_left, self.y_down, width=5, fill='black')
        self.canvas.create_line(self.x_right, self.y_up, self.x_right, self.y_down, width=5, fill='black')
        self.canvas.create_line(self.x_left, self.y_up, self.x_right, self.y_up, width=5, fill='black')
        self.canvas.create_line(self.x_left, self.y_down, self.x_right, self.y_down, width=5, fill='black')

        # Erstellt Event-Listener für Tastatureingabe
        self.canvas.bind_all('<Key>', self.handle_input)

    def load_images(self):
        rotation_mapping = {
            'plane': {0: 'up', 90: 'left', 180: 'down', -90: 'right'}
        }

        for key, image_path in self.images.items():
            # Öffnet das Bild und ändert die Größe, damit es ins Grid passt
            image = Image.open(image_path)
            image = image.resize((self.grid_length, self.grid_length), Image.LANCZOS)

            # Rotiert das Bild, falls es im rotations_mapping enthalten ist
            if key in rotation_mapping:
                rotation_angles = rotation_mapping[key]

                # Erzeugt eine gedrehte Versionen des Bildes und speichere sie für jede Richtung
                for angle, direction in rotation_angles.items():
                    rotated_image = image.rotate(angle)
                    image_tk = ImageTk.PhotoImage(rotated_image)
                    self.image_objects[f'{key}_{direction}'] = image_tk

            if key == 'exhaust':
                # Konvertiert das Bild in den RGBA-Modus, um Transparenz zu ermöglichen
                image = image.convert('RGBA')

                # Iteriert durch jedes Pixel und erhöhe die Transparenz, falls es nicht transparent ist
                for x in range(image.width):
                    for y in range(image.height):
                        pixel = image.getpixel((x, y))
                        if pixel[3] > 0:
                            rgba_pixel = pixel[:3] + (180,)  # Setzt den Alphakanal auf 180
                            image.putpixel((x, y), rgba_pixel)

                image_tk = ImageTk.PhotoImage(image)
                self.image_objects['exhaust'] = image_tk

            # Lade jedes andere Bild außer 'plane' und 'exhaust' als ImageTk-Objekt
            else:
                image_tk = ImageTk.PhotoImage(image)
                self.image_objects[key] = image_tk

    def draw_tilemap(self):
        """Rendert die Tilemap als Hintergrund."""
        for row_index, row in enumerate(self.tilemap):
            for col_index, tile_id in enumerate(row):
                if tile_id in self.images:
                    image_tk = self.image_objects[tile_id]

                    self.canvas.create_image(self.x_left + self.grid_length * col_index + self.number_board_fields - 1, self.y_up + self.grid_length * row_index + self.number_board_fields - 1, image=image_tk)

    def handle_input(self, event):
        """
        Verarbeitet Tastatureingaben, um die Richtung des Fliegers zu ändern und
        verhindert eine Richtungsänderung entgegen der aktuellen Richtung.

        :param event: Das tkinter-Ereignisobjekt, das die Tastatureingabe darstellt.
        """
        if event.keysym == 'w':
            if self.direction != (0, 1):
                self.direction = (0, -1)
                self.plane_image = self.image_objects['plane_up']
        if event.keysym == 'a':
            if self.direction != (1, 0):
                self.direction = (-1, 0)
                self.plane_image = self.image_objects['plane_left']
        if event.keysym == 's':
            if self.direction != (0, -1):
                self.direction = (0, 1)
                self.plane_image = self.image_objects['plane_down']
        if event.keysym == 'd':
            if self.direction != (-1, 0):
                self.direction = (1, 0)
                self.plane_image = self.image_objects['plane_right']

    def update(self):
        """Bewegt den Flieger um ein Feld im Raster in die aktuelle Richtung."""
        self.plane_position[0] += self.direction[0] * self.grid_length
        self.plane_position[1] += self.direction[1] * self.grid_length

    def draw_snake(self):
        """Zeichnet den Fliger oder/und den Abgasstrahl auf dem Spielfeld."""
        plane_image = self.canvas.create_image(self.plane_position[0], self.plane_position[1], image=self.plane_image)
        exhaust_image = self.image_objects['exhaust']

        self.exhaust_plumes.insert(0, plane_image)

        if len(self.exhaust_plumes) == self.num_exhaust_plumes:
            # Wenn die Anzahl der Abgas-Teile das Limit überschreitet, wird das älteste Abgas-Bild entfernt.
            self.canvas.delete(self.exhaust_plumes.pop(-1))

        # Setze alle verbleibenden Bilder zu Abgas-Bilder
        for i in range(1, len(self.exhaust_plumes)):
            self.canvas.itemconfig(self.exhaust_plumes[i], image=exhaust_image)

    def generate_fuel_position(self):
        """
        Generiert eine zufällige Position im Raster für die x- und y-Komponenten
        eines Treibstofftanks und stellt sicher, dass es nicht auf dem Abgasstrahl oder dem Flieger liegt.

        :return: Eine Liste mit x- und y-Koordinaten im Raster, die nicht auf einem Abgasstrahl oder dem Flieger liegen.
        """
        while True:
            x = self.x_left + self.grid_length * 0.5 + random.randint(0, self.number_board_fields - 1) * self.grid_length
            y = self.y_up + self.grid_length * 0.5 + random.randint(0, self.number_board_fields - 1) * self.grid_length
            candidate = [x, y]

            if all(candidate != self.canvas.coords(exhaust_plume) for exhaust_plume in self.exhaust_plumes):
                return candidate

    def draw_fuel(self):
        """Zeichnet den Treibstofftank auf dem Spielfeld an seiner aktuellen Position."""

        if self.fuel:
            self.canvas.delete(self.fuel)

        self.fuel_position = self.generate_fuel_position()
        self.fuel = self.canvas.create_image(self.fuel_position[0], self.fuel_position[1], image=self.image_objects['fuel'])

    def is_outside_board(self):
        """
        Überprüft, ob der Flieger außerhalb des Spielfelds ist.

        :return: True, wenn der Flieger außerhalb des Spielfelds ist, False, wenn er sich innerhalb des Spielfelds befindet.
        """
        return (
                self.plane_position[0] < self.x_left or
                self.plane_position[0] > self.x_right or
                self.plane_position[1] < self.y_up or
                self.plane_position[1] > self.y_down
        )

    def is_flying_into_jet_wash(self):
        """
        Überprüft, ob der Flieger in den Abgasstrahl.

        :return: True, wenn der Flieger in den Abgasstrahl fliegt, False, wenn nicht.
        """
        for exhaust_plume in self.exhaust_plumes:
            x, y = self.canvas.coords(exhaust_plume)
            if self.plane_position[0] == x and self.plane_position[1] == y:
                return True
        return False

    def is_plane_fueling(self):
        """
        Überprüft, ob der Flieger tankt.

        :return: True, wenn der Flieger die x- und y-Position des Treibstofftanks erreicht, ansonsten False.
        """
        return self.plane_position[0] == self.fuel_position[0] and self.plane_position[1] == self.fuel_position[1]

    def run_game(self):
        """Startet die Hauptschleife des Spiels."""
        while True:
            # Generiert den ersten Treibstofftank
            self.fuel_position = self.generate_fuel_position()
            self.draw_fuel()

            # Setzt die Standardrichtung auf rechts und den Flieger auf die Startposition
            self.direction = (1, 0)
            self.plane_position = list(self.start_position)
            for exhaust_plume in self.exhaust_plumes:
                self.canvas.delete(exhaust_plume)

            # Initialisiert das Array des Fligers und die Anzahl der Abgas-Bilder
            self.exhaust_plumes = []
            self.num_exhaust_plumes = 10
            self.plane_image = self.image_objects['plane_right']

            while True:
                # Aktualisiert das Spiel
                self.update()

                # Überprüft verschiedene Bedingungen, bevor der Fliger gerendert wird
                if self.is_outside_board():
                    break
                if self.is_flying_into_jet_wash():
                    break
                if self.is_plane_fueling():
                    # Erzeugt einen neuen Treibstofftank
                    self.fuel_position = self.generate_fuel_position()
                    self.draw_fuel()
                    self.num_exhaust_plumes += 10  # Verlängert den Abgasstrahl um 1

                # Rendert den Flieger
                self.draw_snake()
                self.window.update()

                # Setzt die Geschwindigkeit des Fliegers
                sleep(self.sleep_time)

if __name__ == "__main__":
    game = PlaneGame()
    game.run_game()