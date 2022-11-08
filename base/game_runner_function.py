import time
from random import random

from base.important_variables import *
from base.history_keeper import HistoryKeeper
from base.velocity_calculator import VelocityCalculator
from pygame_library.utility_functions import *

def run_game(main_screen):
    game_window.add_screen(main_screen)
    call_every_cycle(_run_game_every_cycle, game_window.run_on_close)

def _run_game_every_cycle(cycle_time, is_start_time):

    keyboard.run()
    game_window.run()
    min_cycle_time = 1.0 / 60.0 # There is no need to update the display more than 60 times per second
    start_time = 0

    if is_start_time:
        start_time = cycle_time
        cycle_time = time.time() - start_time

    if cycle_time < min_cycle_time:
        time.sleep(min_cycle_time - cycle_time)

    cycle_time = time.time() - start_time

    if cycle_time > .15:
        cycle_time = .15

    HistoryKeeper.times.append(VelocityCalculator.time)
    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = cycle_time + (random() * pow(10, -9))



