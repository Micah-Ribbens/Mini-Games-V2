from base.history_keeper import HistoryKeeper
from base.velocity_calculator import VelocityCalculator


class Event:
    happened_this_cycle = False
    name = ""

    def __init__(self):
        self.name = id(self)

    def run(self, happened_this_cycle):
        self.happened_this_cycle = happened_this_cycle

        HistoryKeeper.add(happened_this_cycle, self.name)

    def happened_last_cycle(self):
        return HistoryKeeper.get_last(self.name)

    def is_click(self):
        return not self.happened_last_cycle() and self.happened_this_cycle

    def has_stopped(self):
        return self.happened_last_cycle() and not self.happened_this_cycle


class TimedEvent:
    current_time = 0
    is_started = False
    time_needed = 0
    restarts_upon_completion = False
    variable_is_done = False  # Stores if the TimedEvent is done for that cycle since it should be known for at least one cycle

    def __init__(self, time_needed, restarts_upon_completion=False):
        self.time_needed = time_needed
        self.restarts_upon_completion = restarts_upon_completion

    def run(self, should_reset, should_start):
        if should_reset:
            self.reset()

        if should_start and not self.is_started:
            self.start()

        if self.is_started:
            self.current_time += VelocityCalculator.time

        if self.current_time >= self.time_needed:
            self.variable_is_done = True

        if self.current_time >= self.time_needed and self.restarts_upon_completion:
            self.start()
            self.current_time = 0

    def start(self):
        self.current_time = 0
        self.is_started = True
        self.variable_is_done = False

    def reset(self):
        self.current_time = 0
        self.is_started = False
        self.variable_is_done = False

    def is_done(self):
        return self.variable_is_done

    def has_finished(self):
        return not self.is_started or self.is_done()