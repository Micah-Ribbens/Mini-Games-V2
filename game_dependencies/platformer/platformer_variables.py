from base.important_variables import *
from base.velocity_calculator import VelocityCalculator

jump_displacement = screen_height * .3
time_to_vertex_of_jump = .55
player_height = VelocityCalculator.get_measurement(screen_height, 15)
side_scrolling_start_distance = VelocityCalculator.get_measurement(screen_length, 33)
# The minimum amount of the next platform that has to be visible when the player gets to the end of the previous platform
min_platform_length_visible = VelocityCalculator.get_measurement(screen_length, 20)