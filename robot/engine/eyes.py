import time
import random
from PIL import Image, ImageDraw

from robot.core import ST7789
from robot.engine.emotions import EMOTIONS
from robot.engine import sound


class RobotEyes:
    def __init__(self):
        self.disp = ST7789.ST7789()
        self.disp.Init()
        self.disp.bl_DutyCycle(100)

        self.x = 120
        self.y = 120
        self.tx = 120
        self.ty = 120

        self.emotion = EMOTIONS["neutral"]
        self.eye_height = self.emotion.height

        self.blink = False
        self.next_blink = time.time() + random.uniform(1.5, 4.0)

    def set_emotion(self, name):
        self.emotion = EMOTIONS[name]

    def update(self):
        if self.emotion.movement:
            self.emotion.movement(self)

        self.eye_height += (self.emotion.height - self.eye_height) * 0.25

    def blink_update(self):
        now = time.time()

        if now > self.next_blink:
            self.blink = not self.blink

            if self.blink:
                sound.play_blink()
                self.next_blink = now + 0.08
            else:
                self.next_blink = now + random.uniform(1.5, 4.0)

    def draw(self):
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        if self.blink:
            d.line((self.x-45, self.y, self.x-15, self.y),
                   fill=self.emotion.color, width=6)
            d.line((self.x+15, self.y, self.x+45, self.y),
                   fill=self.emotion.color, width=6)
        else:
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
