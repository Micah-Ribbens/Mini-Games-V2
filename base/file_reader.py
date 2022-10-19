import os

from base.utility_functions import get_items


class FileReader:
    name_to_data = {}

    def __init__(self, file_path):
        lines = self.get_lines(file_path)

        for line in lines:
            delimiter_start = line.index(":")

            name = line[:delimiter_start]

            data = line[delimiter_start + 1:]

            self.name_to_data[name] = data

    def get_lines(self, file_path):
        enter = """
"""
        file = open(os.getcwd() + "\\" + file_path, "r+")
        lines = get_items(file.read(), enter)
        file.close()
        return lines

    def get_int(self, name):
        return int(self.name_to_data[name])

    def get_float(self, name):
        return float(self.name_to_data[name])

    def get_boolean(self, name):
        return self.name_to_data[name] == "True"

    def get_string_list(self, name):
        return get_items(self.name_to_data[name][1:-1], ",")

    def get_float_list(self, name):
        string_list = self.get_string_list(name)
        float_list = []

        for item in string_list:
            float_list.append(float(item))

        return float_list

    def get_string(self, name):
        return self.name_to_data[name]





