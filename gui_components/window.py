from pygame_library.utility_functions import set_up_window


class Window:
    screens = []

    def __init__(self, length, height, background_color, title):
        set_up_window(length, height, background_color, title)

    def add_screen(self, screen):
        self.screens.append(screen)

    def display_screen(self, screen):
        for other_screen in self.screens:
            other_screen.is_visible = False

        screen.is_visible = True

    def run(self):
        for screen in self.screens:
            if screen.is_visible:
                screen.run()
                screen.render_background()

            else:
                continue

            for component in screen.get_components():

                if component.is_runnable:
                    component.run()

                component.render()

    def run_on_close(self):
        """Runs what should happen when the application is closed"""

        for screen in self.screens:
            screen.run_on_close()
