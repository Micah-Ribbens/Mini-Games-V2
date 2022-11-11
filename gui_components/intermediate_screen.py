from base.colors import white
from base.dimensions import Dimensions
from base.events import TimedEvent
from base.important_variables import background_color, screen_length, screen_height
from gui_components.screen import Screen
from gui_components.text_box import TextBox


class IntermediateScreen(Screen):
    text_box = None
    timed_event = None

    def __init__(self):
        """Initializes the object"""

        self.text_box = TextBox("", 30, background_color, white, True)
        self.timed_event = TimedEvent(0)

        Dimensions.__init__(self, 0, 0, screen_length, screen_height)
        self.components = [self.text_box]
        self.text_box.number_set_dimensions(0, 0, screen_length, screen_height)

    def display(self, message, time_displayed):
        """Displays the 'message' on the screen for the amount 'time_displayed'"""

        self.text_box.text = message
        self.timed_event.time_needed = time_displayed
        self.timed_event.start()

    def run(self):
        """Runs the timed event, so the intermediate only displays for a certain period of time"""

        self.timed_event.run(self.timed_event.current_time >= self.timed_event.time_needed, False)

    def has_finished(self):
        """returns: boolean; if the intermediate screen should be displayed (message displayed time event has finished)"""

        return self.timed_event.has_finished()
