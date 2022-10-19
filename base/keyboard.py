from base.events import Event, TimedEvent
from pygame_library.keys import keys
from pygame_library.utility_functions import mouse_was_pressed, key_is_pressed


class Keyboard:
    key_events = []
    key_timed_events = []
    mouse_clicked_event = Event()

    def __init__(self):
        for x in range(len(keys)):
            self.key_events.append(Event())
            self.key_timed_events.append(TimedEvent(0))
    
    def get_key_timed_event(self, key):
        return self.key_timed_events[key]

    def get_key_event(self, key):
        return self.key_events[key]

    def run(self):
        self.mouse_clicked_event.run(mouse_was_pressed())

        for key in keys:
            key_was_pressed = key_is_pressed(key)

            self.get_key_event(key).run(key_was_pressed)

            should_reset = not self.get_key_event(key).happened_last_cycle() and not key_was_pressed

            self.get_key_timed_event(key).run(should_reset, key_was_pressed)


