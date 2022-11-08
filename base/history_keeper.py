from copy import deepcopy

from base.dimensions import Dimensions
from base.velocity_calculator import VelocityCalculator


class HistoryKeeper:
    last_objects = {}
    times = []
    last_time = 0

    @staticmethod
    def add(history_keeper_object, name, needs_dimensions_only=False, needs_deepcopy=False):
        """ summary: adds the object to the HistoryKeeper; IMPORTANT: make sure to provide a unique name for each unique object!
            params:
                object: Object; the object that is going to be added to the HistoryKeeper
                name: String; the unique name (identifier) for the object
                is_game_object: boolean; the object provided is an instance of GameObject
                needs_deepcopy: boolean; if all the data in the object must be kept (usually only the dimensions are kept)
            returns: None
        """
        if needs_deepcopy:
            history_keeper_object = deepcopy(history_keeper_object)
            history_keeper_object.name = name

        if needs_dimensions_only:
            history_keeper_object = Dimensions(history_keeper_object.left_edge, history_keeper_object.top_edge, history_keeper_object.length, history_keeper_object.height)
            history_keeper_object.name = name

        HistoryKeeper.last_objects[f"{name}{VelocityCalculator.time}"] = history_keeper_object

    @staticmethod
    def get_last(name):
        """ summary: gets the version of that object from the last cycle
            params:
                name: String; the unique name (identifier) given for the object in HistoryKeeper.add() that is used to retrieve the previous version of the object
            returns: Object; the version of the object from the last cycle
        """

        return HistoryKeeper.get_last_using_time(name, HistoryKeeper.last_time)

    @staticmethod
    def get_last_using_time(name, time):
        """returns: Object; the version of the object from the cycle with that time"""

        return HistoryKeeper.last_objects.get(f"{name}{time}")

    @staticmethod
    def reset():
        """Makes the objects the HistoryKeeper keeps track of back down to 0"""

        HistoryKeeper.last_objects = {}
        HistoryKeeper.last_time = 0



