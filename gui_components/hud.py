from gui_components.grid import Grid
from base.colors import *
from gui_components.component import Component
from base.important_variables import *
from gui_components.text_box import TextBox
from base.dimensions import Dimensions

class HUD(Component):
    player_points_fields = []
    other_fields = []
    high_score_field = None
    components = []

    def __init__(self, number_of_points_fields, other_fields, length, height, rows, columns):
        self.player_points_fields = []
        self.high_score_field = TextBox("", 28, pleasing_green, white, True)

        colors = [blue, red, black, orange, purple, yellow]

        for x in range(number_of_points_fields):
            self.player_points_fields.append(TextBox("", 28, white, colors[x], True))

        self.components = other_fields + self.player_points_fields + [self.high_score_field]

        grid = Grid(Dimensions(0, 0, length, height), rows, columns)
        grid.turn_into_grid(self.components, None, None)

    def update(self, player_points, high_score):
        for x in range(len(player_points)):
            self.player_points_fields[x].text = f"Player #{x + 1}: {player_points[x]}"

        self.high_score_field.text = f"High Score: {high_score}"

    def render(self):
        for component in self.components:
            component.render()
