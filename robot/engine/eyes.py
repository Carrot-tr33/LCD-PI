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
        self.eye_vel = 0

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

        # Spring physics calculation
        k = 0.15  # Spring stiffness
        damp = 0.80  # Friction/damping to stop perpetual bouncing
        
        acceleration = (self.emotion.height - self.eye_height) * k
        self.eye_vel = (self.eye_vel + acceleration) * damp
        # Smoothly interpolate eyelid scale changes
        self.eye_height += (self.emotion.height - self.eye_height) * 0.25

    def blink_update(self):
        """Tracks the timed state shifts for natural blinking."""
        # Disable natural blinking for non-standard eye patterns
        if self.emotion.name in ["loading", "sleepy"]:
            self.blink = False
            return
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

        # Delegate drawing to whatever specific behavior the current emotion holds
        self.emotion.draw_func(self, d)

        self.disp.ShowImage(img.rotate(270))