import time
import random
from PIL import Image, ImageDraw

from robot.core import ST7789
from robot.engine.emotions import EMOTIONS
from robot.engine import sound


class RobotEyes:
    def __init__(self):
        # Initializes the screen display controller
        self.disp = ST7789.ST7789()
        self.disp.Init()
        self.disp.bl_DutyCycle(100)

        # Centers the starting positions and targets of the eyes directly in the middle
        self.x = 120
        self.y = 120
        self.tx = 120
        self.ty = 120

        # Sets the default starting state to "neutral" and sets the current eye frame height.
        self.emotion = EMOTIONS["neutral"]
        self.eye_height = self.emotion.height

        self.blink = False # Sets the initial state of the eyes to not blinking
        self.next_blink = time.time() + random.uniform(1.5, 4.0) # Sets the next time to blink at a random interval between 1.5 and 4 seconds

        self.is_glitching = False


    def set_emotion(self, name):
        self.emotion = EMOTIONS[name]

    def update(self):
        # Updates the movement of the eyes based on the current emotional state
        if self.emotion.movement:
            self.emotion.movement(self)

        # Smoothly transitions the eye height to match the current emotional state
        self.eye_height += (self.emotion.height - self.eye_height) * 0.25


    def blink_update(self):
        now = time.time()

        # Checks if it is time to perform a blink change state
        if now > self.next_blink:
            self.blink = not self.blink

            if self.blink:
                sound.play_blink()
                self.next_blink = now + 0.08
            else:
                self.next_blink = now + random.uniform(1.5, 4.0)

    def boot_sequence(self):
        """Executes a diagnostic and cinematic hardware boot sequence."""
        print("--> Initiating Robot Boot Sequence...")
        
        # 1. Screen Power Flickering (Simulating power stabilizing)
        for brightness in [10, 80, 20, 100, 30, 100]:
            self.disp.bl_DutyCycle(brightness)
            time.sleep(0.08)
            
        # 2. RGB Hardware Color Diagnostics
        diagnostic_colors = ["RED", "GREEN", "BLUE"]
        for color in diagnostic_colors:
            img = Image.new("RGB", (240, 240), "BLACK")
            d = ImageDraw.Draw(img)
            # Draw tiny diagnostic indicator blocks in the center
            d.rectangle((110, 110, 130, 130), fill=color)
            self.disp.ShowImage(img.rotate(270))
            time.sleep(0.3)
            
        # 3. Eyelid Fluttering (Waking up)
        # We simulate heavy, tired eyelids trying to open by forcing blink states
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)
        
        # Micro-flutter 1: Quick slit open and shut
        d.line((self.x-45, self.y, self.x-15, self.y), fill="WHITE", width=2)
        d.line((self.x+15, self.y, self.x+45, self.y), fill="WHITE", width=2)
        self.disp.ShowImage(img.rotate(270))
        time.sleep(0.15)
        
        # Clear screen to black
        self.disp.ShowImage(Image.new("RGB", (240, 240), "BLACK").rotate(270))
        time.sleep(0.4)
        
        # Micro-flutter 2: Opening slightly wider
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((self.x-55, self.y-5, self.x-15, self.y+5), 2, "WHITE")
        d.rounded_rectangle((self.x+15, self.y-5, self.x+55, self.y+5), 2, "WHITE")
        self.disp.ShowImage(img.rotate(270))
        time.sleep(0.2)
        
        # Fall back asleep for a brief second
        self.disp.ShowImage(Image.new("RGB", (240, 240), "BLACK").rotate(270))
        time.sleep(0.6)
        
        print("--> Boot Sequence Complete. Consciousness active.")            


    def draw(self):
        # Creates a completely blank, black 240x240 pixel canvas
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        if self.is_glitching:
            # 1. Randomly scramble heights and color palettes every frame
            glitch_height_left = self.eye_height + random.randint(-15, 15)
            glitch_height_right = self.eye_height + random.randint(-15, 15)
            glitch_colors = [self.emotion.color, "CYAN", "RED", "DARKGRAY", "PURPLE"]
            current_color = random.choice(glitch_colors)

            # 2. Desynchronize left and right eye coordinates (horizontal/vertical tearing)
            left_x_offset = random.randint(-12, 12)
            left_y_offset = random.randint(-8, 8)
            right_x_offset = random.randint(-12, 12)
            right_y_offset = random.randint(-8, 8)

            # Draw scrambled Left Eye
            d.rounded_rectangle(
                (self.x - 55 + left_x_offset, self.y - glitch_height_left + left_y_offset,
                 self.x - 15 + left_x_offset, self.y + glitch_height_left + left_y_offset),
                random.randint(2, 12), current_color
            )
            # Draw scrambled Right Eye
            d.rounded_rectangle(
                (self.x + 15 + right_x_offset, self.y - glitch_height_right + right_y_offset,
                 self.x + 55 + right_x_offset, self.y + glitch_height_right + right_y_offset),
                random.randint(2, 12), current_color
            )

            # 3. Render random "GPU interference" lines across the screen matrix
            for _ in range(random.randint(1, 4)):
                y_line = random.randint(0, 240)
                d.line((0, y_line, 240, y_line), fill=random.choice(glitch_colors), width=random.randint(1, 3))
                
        else:
            # Draw the eyes based on the current emotional state and blink status
            # If the robot is blinking, draw two horizontal lines to represent the closed eyes.
            if self.blink:
                d.line((self.x-45, self.y, self.x-15, self.y),
                    fill=self.emotion.color, width=6)
                d.line((self.x+15, self.y, self.x+45, self.y),
                    fill=self.emotion.color, width=6)
            else: # Draws two rounded rectangles to represent the open eyes
                d.rounded_rectangle(
                    (self.x-55, self.y-self.eye_height,
                    self.x-15, self.y+self.eye_height),
                    10, self.emotion.color
                )
                d.rounded_rectangle(
                    (self.x+15, self.y-self.eye_height,
                    self.x+55, self.y+self.eye_height),
                    10, self.emotion.color
                )

        self.disp.ShowImage(img.rotate(270))
