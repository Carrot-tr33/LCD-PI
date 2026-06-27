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

# --- NEW CUSTOM DRAWING BEHAVIORS ---

def loading_draw(robot, d):
    """Transforms both eye positions into coordinated spinning loading rings."""
    # Define the centers for both the left and right eyes based on current gaze layout
    left_center_x = robot.x - 35
    right_center_x = robot.x + 35
    center_y = robot.y
    
    radius = 18       # Size of the loading circles
    num_dots = 6      # Number of segments in each ring
    
    # Calculate smooth rotation step over time
    current_step = int(time.time() * 8) % num_dots  

    for i in range(num_dots):
        # Calculate angle positions for the segments
        angle = (i * (2 * math.pi / num_dots))
        offset_x = int(radius * math.cos(angle))
        offset_y = int(radius * math.sin(angle))
        
        # Calculate trailing brightness/fade effect
        diff = (i - current_step) % num_dots
        if diff == 0:
            dot_color = robot.emotion.color  # Lead bright accent color
            dot_radius = 5
        elif diff == 1 or diff == 2:
            dot_color = "GRAY"               # Mid-tone fading trail
            dot_radius = 3.5
        else:
            dot_color = "#222222"            # Dim unlit slots
            dot_radius = 2

        # Draw Left Eye Segment
        d.ellipse(
            (left_center_x + offset_x - dot_radius, center_y + offset_y - dot_radius, 
             left_center_x + offset_x + dot_radius, center_y + offset_y + dot_radius), 
            fill=dot_color
        )
        
        # Draw Right Eye Segment (synchronized spin)
        d.ellipse(
            (right_center_x + offset_x - dot_radius, center_y + offset_y - dot_radius, 
             right_center_x + offset_x + dot_radius, center_y + offset_y + dot_radius), 
            fill=dot_color
        )

def thinking_draw(robot, d):
    """Draws asymmetric eyes: one narrow analyzing eye, and one wider eye that looks around."""
    # Left eye: Narrow, squinted analytic look
    d.rounded_rectangle(
        (robot.x - 55, robot.y - 8, robot.x - 15, robot.y + 8),
        4, robot.emotion.color
    )
    # Right eye: Normal height, looking up/around
    d.rounded_rectangle(
        (robot.x + 15, robot.y - robot.eye_height, robot.x + 55, robot.y + robot.eye_height),
        10, robot.emotion.color
    )


def bored_draw(robot, d):
    """Draws heavily drooped eyelids by cutting off the top half of the rounded rectangles."""
    # Base eye color rectangles
    d.rounded_rectangle(
        (robot.x - 55, robot.y - robot.eye_height, robot.x - 15, robot.y + robot.eye_height),
        10, robot.emotion.color
    )
    d.rounded_rectangle(
        (robot.x + 15, robot.y - robot.eye_height, robot.x + 55, robot.y + robot.eye_height),
        10, robot.emotion.color
    )
    # Draw heavy black 'eyelids' over the top half of the screen to give a half-closed look
    d.rectangle((0, 0, 240, robot.y - 2), fill="BLACK")


def shocked_draw(robot, d):
    """Draws massive, perfectly circular startled eyes."""
    radius = robot.eye_height + 5
    # Left eye ring
    d.ellipse((robot.x - 55, robot.y - radius, robot.x - 15, robot.y + radius), fill=robot.emotion.color)
    # Right eye ring
    d.ellipse((robot.x + 15, robot.y - radius, robot.x + 55, robot.y + radius), fill=robot.emotion.color)


def sleepy_draw(robot, d):
    """Draws soft, upward curved 'sleeping arc' lines (^^) instead of open rectangles."""
    # Left Eye sleeping arc
    d.arc((robot.x - 55, robot.y - 10, robot.x - 15, robot.y + 20), start=180, end=360, fill=robot.emotion.color, width=6)
    # Right Eye sleeping arc
    d.arc((robot.x + 15, robot.y - 10, robot.x + 55, robot.y + 20), start=180, end=360, fill=robot.emotion.color, width=6)

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

# --- NEW MOVEMENT BEHAVIORS ---

def thinking_move(robot):
    """Slowly rolls the gaze in small circles up towards the top-right corner."""
    now = time.time()
    # Lock target look coordinates upward to simulate contemplation
    robot.tx = 140 + int(math.cos(now * 2) * 10)
    robot.ty = 90 + int(math.sin(now * 2) * 10)
    
    # Slow down interpolation to look deliberate
    robot.x += (robot.tx - robot.x) * 0.04
    robot.y += (robot.ty - robot.y) * 0.04


def bored_move(robot):
    """Gaze drifts heavily downwards and barely updates."""
    now = time.time()
    if not hasattr(robot, "next_look"):
        robot.next_look = 0

    if now > robot.next_look:
        # Bored eyes look down and slouch left or right sluggishly
        robot.tx = random.choice([100, 140])
        robot.ty = 155 
        robot.next_look = now + random.uniform(4.0, 7.0) # Changes very infrequently

    robot.x += (robot.tx - robot.x) * 0.03
    robot.y += (robot.ty - robot.y) * 0.03


def sleepy_move(robot):
    """Slowly sways up and down gently, mimicking breathing while sleeping."""
    robot.tx, robot.ty = 120, 120
    robot.x += (robot.tx - robot.x) * 0.05
    robot.y = 120 + math.sin(time.time() * 1.5) * 2.5

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
    "loading":  Emotion("loading", 0, "ORANGE", movement=None, draw_func=loading_draw),
    "thinking": Emotion("thinking", 32, "YELLOW", movement=thinking_move, draw_func=thinking_draw),
    "bored":    Emotion("bored", 22, "BLUE", movement=bored_move, draw_func=bored_draw),
    "shocked":  Emotion("shocked", 35, "ORANGE", movement=angry_move, draw_func=shocked_draw),
    "sleepy":   Emotion("sleepy", 0, "BLUE", movement=sleepy_move, draw_func=sleepy_draw),
}