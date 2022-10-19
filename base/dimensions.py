class Dimensions:
    left_edge = 0
    top_edge = 0
    length = 0
    height = 0

    def __init__(self, left_edge, top_edge, length, height):
        self.left_edge, self.top_edge, self.length, self.height = left_edge, top_edge, length, height

    @property
    def right_edge(self):
        return self.left_edge + self.length

    @property
    def bottom_edge(self):
        return self.top_edge + self.height

    @property
    def horizontal_midpoint(self):
        return self.left_edge + self.length / 2

    @property
    def vertical_midpoint(self):
        return self.top_edge + self.height / 2

    def number_set_dimensions(self, left_edge, top_edge, length, height):
        self.left_edge, self.top_edge, self.length, self.height = left_edge, top_edge, length, height

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height, horizontal_number, vertical_number):
        self.left_edge = horizontal_number * percent_right / 100
        self.length = horizontal_number * percent_length / 100
        self.top_edge = vertical_number * percent_down / 100
        self.height = vertical_number * percent_height / 100