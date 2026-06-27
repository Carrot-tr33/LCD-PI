import time
import random
import math

# Defines a blueprint data class to store the physical attributes and behavior of each emotional state.
class Emotion:
    def __init__(self, name, height, color, movement=None):
        self.name = name          # String identifier
        self.height = height      # Vertical size of the eyes
        self.color = color        # Color of the eyes
        self.movement = movement  # Function that defines how the robot moves when in this emotional state


# Defines the movement behavior 
def neutral_move(robot):
    now = time.time()

    # Initialize the target position for the robot's eyes if it hasn't been set yet
    if not hasattr(robot, "next_look"):
        robot.next_look = 0

    # Update the target position for the robot's eyes at random intervals
    if now > robot.next_look:
        robot.tx = random.randint(95, 145)
        robot.ty = random.randint(100, 140)
        robot.next_look = now + random.uniform(0.8, 2.0) # Set the next time to update the target position

    robot.x += (robot.tx - robot.x) * 0.08
    robot.y += (robot.ty - robot.y) * 0.08


def happy_move(robot):
    neutral_move(robot)

    robot.y += math.sin(time.time() * 6) * 0.5


def angry_move(robot):
    neutral_move(robot)

    robot.x += random.uniform(-1.5, 1.5)
    robot.y += random.uniform(-1.5, 1.5)


def gold_move(robot):
    neutral_move(robot)

    robot.y += math.sin(time.time() * 2) * 1.2

# A dictionary mapping string keys to configured Emotion objects
EMOTIONS = {
    "neutral": Emotion("neutral", 30, "WHITE", neutral_move),
    "happy": Emotion("happy", 35, "MAGENTA", happy_move),
    "angry": Emotion("angry", 20, "RED", angry_move),
    "gold": Emotion("gold", 45, "GOLD", gold_move),
    "glitch":  Emotion("glitch", 35, "CYAN", None),
}
