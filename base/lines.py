class Point:
    x_coordinate = 0
    y_coordinate = 0

    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate


class LineSegment:
    start_point = None
    end_point = None
    slope = None
    y_intercept = None

    def __init__(self, start_point, end_point):
        self.start_point, self.end_point = start_point, end_point

        if start_point.x_coordinate == end_point.x_coordinate:
            end_point.x_coordinate += pow(10, -9)

        self.slope = (end_point.y_coordinate - start_point.y_coordinate) / (end_point.x_coordinate - start_point.x_coordinate)
        self.y_intercept = start_point.y_coordinate - self.slope * start_point.x_coordinate

    def get_y_coordinate(self, x_coordinate):
        return x_coordinate * self.slope + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        return (y_coordinate - self.y_intercept) / self.slope

    def contains_x_coordinate(self, x_coordinate):
        smaller_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate < self.end_point.x_coordinate else self.end_point.x_coordinate
        bigger_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate > self.end_point.x_coordinate else self.end_point.x_coordinate

        return x_coordinate >= smaller_x_coordinate and x_coordinate <= bigger_x_coordinate

    def contains_y_coordinate(self, y_coordinate):
        smaller_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate < self.end_point.y_coordinate else self.end_point.y_coordinate
        bigger_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate > self.end_point.y_coordinate else self.end_point.y_coordinate

        return y_coordinate >= smaller_y_coordinate and y_coordinate <= bigger_y_coordinate

    def contains_point(self, point):
        contains_coordinates = self.contains_x_coordinate(point.x_coordinate) and self.contains_y_coordinate(point.y_coordinate)
        correct_y_coordinate = point.y_coordinate == self.get_y_coordinate(point.x_coordinate)

        return contains_coordinates and correct_y_coordinate



