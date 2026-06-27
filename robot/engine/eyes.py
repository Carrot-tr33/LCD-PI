# robot/engine/eyes.py
import time
import random
from PIL import Image, ImageDraw

from robot.core import ST7789
from robot.engine.emotions import EMOTIONS

class RobotEyes:
    def __init__(self):
        self.disp = ST7789.ST7789()
        self.disp.Init()
        self.disp.bl_DutyCycle(100)

        # Gaze coordinates
        self.x, self.y = 120, 120
        self.tx, self.ty = 120, 120

        # Initial baseline emotion state
        self.emotion = EMOTIONS["neutral"]
        self.eye_height = self.emotion.height

        # Blinking mechanics
        self.blink = False 
        self.next_blink = time.time() + random.uniform(1.5, 4.0)

    def set_emotion(self, name):
        """Swaps the active emotion configuration profile."""
        if name in EMOTIONS:
            self.emotion = EMOTIONS[name]

    def update(self):
        """Updates internal position transitions and scaling calculations."""
        if self.emotion.movement:
            self.emotion.movement(self)

        # Smoothly interpolate eyelid scale changes
        self.eye_height += (self.emotion.height - self.eye_height) * 0.25

    def blink_update(self):
        """Tracks the timed state shifts for natural blinking."""
        now = time.time()
        if now > self.next_blink:
            self.blink = not self.blink
            if self.blink:
                self.next_blink = now + 0.08
            else:
                self.next_blink = now + random.uniform(1.5, 4.0)

    def boot_sequence(self):
        """Executes a diagnostic cinematic boot sequence on initialization."""
        print("--> Initiating Robot Boot Sequence...")
        for brightness in [10, 80, 20, 100, 30, 100]:
            self.disp.bl_DutyCycle(brightness)
            time.sleep(0.08)
            
        for color in ["RED", "GREEN", "BLUE"]:
            img = Image.new("RGB", (240, 240), "BLACK")
            d = ImageDraw.Draw(img)
            d.rectangle((110, 110, 130, 130), fill=color)
            self.disp.ShowImage(img.rotate(270))
            time.sleep(0.2)
        print("--> Boot Complete.")

    def draw(self):
        """Generates and displays the graphic frame buffer layer."""
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        # --- NATIVE GLITCH EMOTION DRAWING ---
        if self.emotion.name == "glitch":
            glitch_height_l = self.eye_height + random.randint(-15, 15)
            glitch_height_r = self.eye_height + random.randint(-15, 15)
            glitch_colors = ["CYAN", "RED", "WHITE", "PURPLE", "GREEN"]
            current_color = random.choice(glitch_colors)

            l_offset_x, l_offset_y = random.randint(-10, 10), random.randint(-6, 6)
            r_offset_x, r_offset_y = random.randint(-10, 10), random.randint(-6, 6)

            # Left Eye Scramble
            d.rounded_rectangle(
                (self.x - 55 + l_offset_x, self.y - glitch_height_l + l_offset_y,
                 self.x - 15 + l_offset_x, self.y + glitch_height_l + l_offset_y),
                random.randint(2, 10), current_color
            )
            # Right Eye Scramble
            d.rounded_rectangle(
                (self.x + 15 + r_offset_x, self.y - glitch_height_r + r_offset_y,
                 self.x + 55 + r_offset_x, self.y + glitch_height_r + r_offset_y),
                random.randint(2, 10), current_color
            )
            # Video Artifact Scanlines
            for _ in range(random.randint(1, 3)):
                y_ln = random.randint(0, 240)
                d.line((0, y_ln, 240, y_ln), fill=random.choice(glitch_colors), width=random.randint(1, 2))

        # --- REGULAR CLEAN EMOTION DRAWING ---
        else:
            if self.blink:
                d.line((self.x - 45, self.y, self.x - 15, self.y), fill=self.emotion.color, width=6)
                d.line((self.x + 15, self.y, self.x + 45, self.y), fill=self.emotion.color, width=6)
            else:
                d.rounded_rectangle(
                    (self.x - 55, self.y - self.eye_height, self.x - 15, self.y + self.eye_height),
                    10, self.emotion.color
                )
                d.rounded_rectangle(
                    (self.x + 15, self.y - self.eye_height, self.x + 55, self.y + self.eye_height),
                    10, self.emotion.color
                )

        self.disp.ShowImage(img.rotate(270))