from base.important_variables import *
from base.velocity_calculator import VelocityCalculator

jump_displacement = screen_height * .3
time_to_vertex_of_jump = .55
player_height = VelocityCalculator.get_measurement(screen_height, 15)