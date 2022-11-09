from base.fraction import Fraction
from base.important_variables import *
from base.lines import Point
from base.paths import SimplePath
from base.velocity_calculator import VelocityCalculator

## Player
### Dimensions
PLAYER_HEIGHT = VelocityCalculator.get_measurement(screen_height, 15)
PLAYER_LENGTH = VelocityCalculator.get_measurement(screen_length, 5)

### Movement
PLAYER_JUMP_DISPLACEMENT = screen_height * .3
PLAYER_TIME_TO_JUMP_VERTEX = .55
PLAYER_RUNNING_DECELERATION_TIME = .3
PLAYER_INVINCIBILITY_TOTAL_TIME = 1
PLAYER_TIME_TO_GET_MAX_VELOCITY = .2
PLAYER_MAX_HORIZONTAL_VELOCITY = VelocityCalculator.get_velocity(screen_length, 450)

### Other
PLAYER_OBJECT_TYPE = "Player"
PLAYER_TOTAL_HIT_POINTS = 60
PLAYER_BASE_LEFT_EDGE = 100
PLAYER_BASE_TOP_EDGE = 0

## Generator

### Miscellaneous
MAX_VERTICAL_CHANGE = VelocityCalculator.get_measurement(screen_height, 25)
SIDE_SCROLLING_START_DISTANCE = VelocityCalculator.get_measurement(screen_length, 33)
# The minimum amount of the next platform that has to be visible when the player gets to the end of the previous platform
MINIMUM_PLATFORM_LENGTH_VISIBLE = VelocityCalculator.get_measurement(screen_length, 20)
MINIMUM_GENERATOR_ACCURACY_DECREASE = .05
MARGINS_OF_ERROR = SimplePath(Point(0, 35), [Point(20, 30), Point(40, 25), Point(60, 20), Point(70, 15),
                                             Point(80, 10), Point(90, 6), Point(100, 0)])


### Platform Dimensions
MINIMUM_PLATFORM_HEIGHT = int(VelocityCalculator.get_measurement(screen_height, 10))
MAXIMUM_PLATFORM_HEIGHT = int(VelocityCalculator.get_measurement(screen_height, 20))
MINIMUM_PLATFORM_LENGTH = int(VelocityCalculator.get_measurement(screen_length, 45))
MAXIMUM_PLATFORM_LENGTH = int(VelocityCalculator.get_measurement(screen_length, 55))

## Scoring
SCORE_FROM_PASSING_PLATFORM = 100
SCORE_FROM_KILLING_ENEMY = 250
SCORE_TO_GAME_DIFFICULTY = SimplePath(Point(0, 50), [Point(1000, 70), Point(2500, 90), Point(5000, 100),
                                                     Point(float("inf"), 100)])

## Weapons
BASE_WEAPON_AMMO = 10
WEAPON_BASE_DAMAGE = 10

### Bouncy Thrower
BOUNCY_PROJECTILE_SIZE = VelocityCalculator.get_measurement(screen_length, 2.5)
TIME_TO_BOUNCY_PROJECTILE_VERTEX = .2
BOUNCY_PROJECTILE_WEAPON_NAME = "bouncy thrower"
BOUNCY_THROWER_DAMAGE = 15
BOUNCY_THROWER_HIT_POINTS = 10
BOUNCY_THROWER_COOL_DOWN_TIME = .15

### Straight Thrower
STRAIGHT_PROJECTILE_LENGTH = VelocityCalculator.get_measurement(screen_length, 3)
STRAIGHT_PROJECTILE_HEIGHT = VelocityCalculator.get_measurement(screen_height, 4)
STRAIGHT_THROWER_WEAPON_NAME = "straight thrower"
STRAIGHT_THROWER_WEAPON_DAMAGE = 10
STRAIGHT_THROWER_WEAPON_HIT_POINTS = 10
STRAIGHT_THROWER_COOL_DOWN_TIME = .15


## Powerups
POWERUP_LENGTH = VelocityCalculator.get_measurement(screen_length, 3)
POWERUP_HEIGHT = VelocityCalculator.get_measurement(screen_height, 3)
AMMO_INCREASE_FROM_POWERUP = 5
HEALTH_INCREASE_FROM_HEART = 5
PROBABILITY_OF_GETTING_POWERUP_GENERATED = Fraction(2, 7)
# If the player has a weapon and they pick up the powerup of the same weapon that weapon should be upgraded
DAMAGE_INCREASE_FROM_DUPLICATE_WEAPON_PICKUP = 5
# Probabilities of a powerup being a specific type
PROBABILITY_OF_POWERUP_BEING_A_WEAPON = Fraction(30, 100)
PROBABILITY_OF_POWERUP_NOT_BEING_A_WEAPON = PROBABILITY_OF_POWERUP_BEING_A_WEAPON.get_fraction_to_become_one()

## Wall of Death
TIME_BEFORE_WALL_OF_DEATH_STARTS_MOVING = 2
WALL_OF_DEATH_TIME_INCREASE_AFTER_PLAYER_DEATH = 1
TIME_GAME_HAS_RUN_TO_WALL_OF_DEATH_VELOCITY = SimplePath(Point(0, PLAYER_MAX_HORIZONTAL_VELOCITY * .3),
                                                         [Point(5, PLAYER_MAX_HORIZONTAL_VELOCITY * .5),
                                                          Point(30, PLAYER_MAX_HORIZONTAL_VELOCITY * .6),
                                                          Point(60, PLAYER_MAX_HORIZONTAL_VELOCITY * .7),
                                                          Point(120, PLAYER_MAX_HORIZONTAL_VELOCITY * .75),
                                                          Point(float("inf"), PLAYER_MAX_HORIZONTAL_VELOCITY * .75)])
