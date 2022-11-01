from base.history_keeper import HistoryKeeper
from base.velocity_calculator import VelocityCalculator


class CollisionsEngine:

    @staticmethod
    def is_horizontal_collision(object1, object2):        
        return object1.left_edge <= object2.right_edge and object1.right_edge >= object2.left_edge

    @staticmethod
    def is_vertical_collision(object1, object2):
        return object1.top_edge <= object2.bottom_edge and object1.bottom_edge >= object2.top_edge

    @staticmethod
    def is_collision(object1, object2):
        return CollisionsEngine.is_horizontal_collision(object1, object2) and CollisionsEngine.is_vertical_collision(object1, object2)

    # VERY IMPORTANT NOTE: is moving left and right collisions count it if the object was not outside of the other last cycle
    # Meaning that if the object were to come down onto the end of the other object it would count; whereas left and right
    # Collisions it has to be on the outside last cycle in order for it to count
    @staticmethod
    def is_left_collision(object1, object2, is_collision=None, last_time=None):
        """returns: boolean; if object1 has collided with object2's left edge (movement does not matter)"""

        objects_are_touching = object1.right_edge == object2.left_edge and CollisionsEngine.is_vertical_collision(object1, object2)
        is_moving_left_collision = CollisionsEngine.is_moving_left_collision(object1, object2, is_collision, last_time)

        return is_moving_left_collision or objects_are_touching

    @staticmethod
    def is_right_collision(object1, object2, is_collision=None, last_time=None):
        """returns: boolean; if object1 has collided with object2's right_edge (movement does not matter)"""

        is_moving_right_collision = CollisionsEngine.is_moving_right_collision(object1, object2, is_collision, last_time)
        objects_are_touching = object1.left_edge == object2.right_edge and CollisionsEngine.is_vertical_collision(object1, object2)

        return is_moving_right_collision or objects_are_touching

    @staticmethod
    def is_moving_right_collision(object1, object2, is_collision=None, last_time=None):
        """returns: boolean; if object1 has collided with object2's right_edge because one of the objects has moved"""
        
        last_time = last_time if last_time is not None else HistoryKeeper.last_time

        # TODO change both to HistoryKeeper.get_last_using_time?
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)
        object1_has_moved_into_object2 = (
                    prev_object1.left_edge > prev_object2.right_edge and object1.left_edge < object2.right_edge)

        return is_collision and object1_has_moved_into_object2

    @staticmethod
    def is_moving_left_collision(object1, object2, is_collision=None, last_time=None):
        """ returns: boolean; if object1 has hit object2's left_edge because one of the objects has moved"""

        last_time = last_time if last_time is not None else HistoryKeeper.last_time

        # TODO change both to HistoryKeeper.get_last_using_time?
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        object1_has_moved_into_object2 = prev_object1.right_edge < prev_object2.left_edge and object1.right_edge > object2.left_edge
        return is_collision and object1_has_moved_into_object2


    def is_bottom_collision(object1, object2, is_collision=None, time=None):
        """ summary: finds out if the object's collided from the bottom

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object's collided from the bottom
        """
        last_time = time if time is not None else HistoryKeeper.last_time

        # TODO change both to HistoryKeeper.get_last_using_time?
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        objects_are_touching = object1.top_edge == object2.bottom_edge and CollisionsEngine.is_horizontal_collision(object1,
                                                                                                               object2)
        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.top_edge > prev_object2.bottom_edge and
                object1.top_edge < object2.bottom_edge) or objects_are_touching

    @staticmethod
    def is_top_collision(object1, object2, is_collision=None, time=None):
        """ summary: finds out if the object's collided from the bottom

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object's collided from the bottom
        """

        last_time = time if time is not None else HistoryKeeper.last_time

        # TODO change both to HistoryKeeper.get_last_using_time?
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        # So rounding doesn't cause any issues
        objects_are_touching = int(object1.bottom_edge) == int(object2.top_edge) and CollisionsEngine.is_horizontal_collision(object1,
                                                                                                               object2)
        is_collision = is_collision if is_collision is not None else CollisionsEngine.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.bottom_edge < prev_object2.top_edge
                and object1.bottom_edge > object2.top_edge) or objects_are_touching


