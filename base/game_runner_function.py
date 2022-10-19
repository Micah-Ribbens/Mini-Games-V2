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

    if cycle_time < .06:
        time.sleep(.06 - cycle_time)

    if is_start_time:
        cycle_time = time.time() - cycle_time

    if cycle_time > .06:
        cycle_time = .06

    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = cycle_time + (random() * pow(10, -9))



