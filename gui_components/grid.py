from math import ceil, floor

from base.important_variables import screen_length, screen_height
from base.velocity_calculator import VelocityCalculator


class Grid:
    rows = None
    columns = None
    dimensions = None
    length_buffer = VelocityCalculator.get_measurement(screen_length, 1)
    height_buffer = VelocityCalculator.get_measurement(screen_height, 1)

    def __init__(self, dimensions, rows, columns):
        self.dimensions = dimensions
        self.rows, self.columns = rows, columns

    def turn_into_grid(self, items, item_max_length, item_max_height):
        rows, columns = self.rows, self.columns
        number_of_items = len(items)

        if rows is None:
            rows = self.get_grid_dimension(columns, number_of_items)

        if columns is None:
            columns = self.get_grid_dimension(rows, number_of_items)

        item_height = self.get_item_dimension(self.dimensions.height, rows, item_max_height, self.height_buffer)
        item_length = self.get_item_dimension(self.dimensions.length, columns, item_max_length, self.length_buffer)

        base_left_edge = self.dimensions.left_edge
        base_top_edge = self.dimensions.top_edge

        for x in range(number_of_items):
            column_number = x % columns
            row_number = floor(x / columns)

            left_edge = base_left_edge + self.get_dimension_change(column_number, item_length, self.length_buffer)
            top_edge = base_top_edge + self.get_dimension_change(row_number, item_height, self.height_buffer)

            items[x].number_set_dimensions(left_edge, top_edge, item_length, item_height)

    def get_grid_dimension(self, other_dimension, number_of_items):
        """returns: int; either the rows or columns depending on which is provided (rows if columns is provided + vice versa)"""

        return ceil(number_of_items / other_dimension)

    def get_item_dimension(self, grid_dimension_size, grid_dimension, item_dimension_max, buffer_between_items):
        """returns: double; the size of an item's dimension (either the length or height)"""

        remaining_dimension = grid_dimension_size - buffer_between_items * (grid_dimension - 1)

        item_dimension = remaining_dimension / grid_dimension

        if item_dimension_max is not None and item_dimension > item_dimension_max:
            item_dimension = item_dimension_max

        return item_dimension

    def get_dimension_change(self, grid_dimension, item_dimension, buffer_between_items):
        """returns: double; the change from the start of the grid to that item"""

        return grid_dimension * (item_dimension + buffer_between_items)