import time
import random
import math

class Emotion:
    def __init__(self, name, height, color, movement=None, draw_func=None):
        self.name = name          
        self.height = height      
        self.color = color        
        self.movement = movement  
        self.draw_func = draw_func if draw_func else default_draw # Fallback to default rendering


# --- DRAWING BEHAVIORS ---

def default_draw(robot, d):
    """The standard rendering style for regular clean emotions."""
    if robot.blink:
        d.line((robot.x - 45, robot.y, robot.x - 15, robot.y), fill=robot.emotion.color, width=6)
        d.line((robot.x + 15, robot.y, robot.x + 45, robot.y), fill=robot.emotion.color, width=6)
    else:
        d.rounded_rectangle(
            (robot.x - 55, robot.y - robot.eye_height, robot.x - 15, robot.y + robot.eye_height),
            10, robot.emotion.color
        )
        d.rounded_rectangle(
            (robot.x + 15, robot.y - robot.eye_height, robot.x + 55, robot.y + robot.eye_height),
            10, robot.emotion.color
        )


def glitch_draw(robot, d):
    """The specialized frantic rendering style for the glitch state."""
    glitch_height_l = robot.eye_height + random.randint(-15, 15)
    glitch_height_r = robot.eye_height + random.randint(-15, 15)
    glitch_colors = ["CYAN", "RED", "WHITE", "PURPLE", "GREEN"]
    current_color = random.choice(glitch_colors)

    l_offset_x, l_offset_y = random.randint(-10, 10), random.randint(-6, 6)
    r_offset_x, r_offset_y = random.randint(-10, 10), random.randint(-6, 6)

    # Left Eye Scramble
    d.rounded_rectangle(
        (robot.x - 55 + l_offset_x, robot.y - glitch_height_l + l_offset_y,
         robot.x - 15 + l_offset_x, robot.y + glitch_height_l + l_offset_y),
        random.randint(2, 10), current_color
    )
    # Right Eye Scramble
    d.rounded_rectangle(
        (robot.x + 15 + r_offset_x, robot.y - glitch_height_r + r_offset_y,
         robot.x + 55 + r_offset_x, robot.y + glitch_height_r + r_offset_y),
        random.randint(2, 10), current_color
    )
    # Video Artifact Scanlines
    for _ in range(random.randint(1, 3)):
        y_ln = random.randint(0, 240)
        d.line((0, y_ln, 240, y_ln), fill=random.choice(glitch_colors), width=random.randint(1, 2))


# --- MOVEMENT BEHAVIORS ---

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


# --- EMOTION REGISTRY ---

EMOTIONS = {
    "neutral": Emotion("neutral", 30, "WHITE", movement=neutral_move),
    "happy":   Emotion("happy", 35, "MAGENTA", movement=happy_move),
    "angry":   Emotion("angry", 20, "RED", movement=angry_move),
    "gold":    Emotion("gold", 45, "GOLD", movement=gold_move),
    "glitch":  Emotion("glitch", 35, "CYAN", movement=None, draw_func=glitch_draw),
}