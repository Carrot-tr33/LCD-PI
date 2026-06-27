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


    def draw(self):
        # Creates a completely blank, black 240x240 pixel canvas
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

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
