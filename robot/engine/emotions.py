import time
import random
import math


class Emotion:
    def __init__(self, name, height, color, movement=None):
        self.name = name
        self.height = height
        self.color = color
        self.movement = movement


def neutral_move(robot):
    now = time.time()

    if not hasattr(robot, "next_look"):
        robot.next_look = 0

    if now > robot.next_look:
        robot.tx = random.randint(95, 145)
        robot.ty = random.randint(100, 140)
        robot.next_look = now + random.uniform(0.8, 2.0)

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


EMOTIONS = {
    "neutral": Emotion("neutral", 30, "WHITE", neutral_move),
    "happy": Emotion("happy", 35, "MAGENTA", happy_move),
    "angry": Emotion("angry", 20, "RED", angry_move),
    "gold": Emotion("gold", 45, "GOLD", gold_move),
}
