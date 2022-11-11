from fractions import Fraction
from math import sqrt

from base.important_variables import *
from pygame_library.utility_functions import *
import random


def key_is_pressed(key):
    return keyboard.get_key_event(key).happened_this_cycle

def key_is_hit(key):
    return keyboard.get_key_event(key).is_click()


def key_has_been_released(key):
    return keyboard.get_key_event(key).has_stopped()


def get_time_of_key_being_held_in(key):
    return keyboard.get_key_timed_event(key).current_time


def mouse_is_clicked():
    return keyboard.mouse_clicked_event.is_click()


def mouse_is_clicked():
    return keyboard.mouse_clicked_event.is_click()

def get_index_of_range(range_lengths, number):
    index = -1
    start_time = 0

    for x in range(len(range_lengths)):
        end_time = start_time + range_lengths[x]

        if number >= start_time and number <= end_time:
            index = x

        start_time = end_time

    return index

def get_items(data, new_item_ch):
    current_item = ""
    items = []

    for ch in data:
        if ch == new_item_ch:
            items.append(current_item)
            current_item = ""

        else:
            current_item += ch

    if current_item != "":
        items.append(current_item)

    return items

def rounded(number, places):
    """returns: double; the number rounded to that many decimal places"""

    rounded_number = int(number * pow(10, places))

    # Converting it back to the proper decimals once it gets rounded from above
    return rounded_number / pow(10, places)

def get_kwarg_item(kwargs, key, default_value):
    """ summary: finds the kwarg item

        params:
            kwargs: dict; the **kwargs
            key: Object; the key for the item
            default_value: Object; the value that will be obtained if the kwargs doesn't contain the key

        returns: Object; kwargs.get(key) if kwargs contains the key otherwise it will return the default_value
    """

    return kwargs.get(key) if kwargs.__contains__(key) else default_value

def solve_quadratic(a, b, c):
    """returns: List of double; [answer1, answer2] the answers to the quadratic
                and if the answer is an imaginary number it returns: float('nan')"""

    number_under_square_root = pow(b, 2) - 4 * a * c
    number_under_square_root = rounded(number_under_square_root, 4)

    if number_under_square_root < 0:
        return None

    square_root = sqrt(number_under_square_root)

    answer1 = (-b + square_root) / (2 * a)
    answer2 = (-b - square_root) / (2 * a)

    answers = [answer2, answer1]

    # If the answers are the same I should only return one of them
    return answers if answers[0] != answers[1] else [answers[0]]

def min_value(item1, item2):
    """returns: double; the smallest item"""

    if item1 is None:
        return item2

    if item2 is None:
        return item1

    return item1 if item1 < item2 else item2


def max_value(item1, item2):
    """returns double; the biggest item"""

    return item1 if item1 > item2 else item2


def is_within_screen(game_object):
    """returns: boolean; if the game_object is within the screen (can be seen on the screen)"""

    return (game_object.right_edge > 0 and game_object.left_edge < screen_length and
            game_object.bottom_edge > 0 and game_object.top_edge < screen_height)

def get_next_index(current_index, max_index):
    """returns: int; the index after current_index (it cycles, so once it gets beyond the max_index it goes back to 0)"""

    next_index = current_index + 1
    return next_index if next_index <= max_index else 0


def get_previous_index(current_index, max_index):
    """returns: int; the index before current_index (it cycles, so once it gets below 0 it goes to the max_index"""

    prev_index = current_index - 1
    return prev_index if prev_index >= 0 else max_index

def is_random_chance(probability: Fraction):
    """ summary: uses the probability for the random chance (for instance if the probability is 7/10 then 7 out of 10
        times it will return True and the other 3 times it will return False)

        params:
            probability: Fraction; the probability this function will return True

        returns: boolean; if the random number between 1-probability.denominator is >= probability.numerator
    """

    return random.randint(1, probability.denominator) <= probability.numerator


def is_beyond_screen_left(left_edge):
    """returns: boolean; if the left_edge is beyond the left side of the screen"""

    return left_edge <= 0


def is_beyond_screen_right(right_edge):
    """returns: boolean; if the right_edge is beyond the right side of the screen"""

    return right_edge >= screen_length