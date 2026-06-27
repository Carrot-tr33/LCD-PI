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

    def draw_menu(self, menu_options, selected_index):
        """Renders a text-based UI selection menu over the image canvas."""
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        # Draw Title bar
        d.rectangle((0, 0, 240, 35), fill="BLUE")
        d.text((10, 10), "SYSTEM MAIN MENU", fill="WHITE")
        d.line((0, 35, 240, 35), fill="WHITE", width=2)

        # Draw Menu list options
        start_y = 60
        for index, option in enumerate(menu_options):
            y_pos = start_y + (index * 40)
            
            if index == selected_index:
                # Draw a highlight box around the active selected row
                d.rectangle((10, y_pos - 5, 230, y_pos + 25), outline="CYAN", fill="#112233")
                d.text((25, y_pos), f"> {option}", fill="CYAN")
            else:
                d.text((25, y_pos), f"  {option}", fill="LIGHTGRAY")

        self.disp.ShowImage(img.rotate(270))

    def draw_stats_page(self, cpu_pct, ram_pct):
        """Renders a live system dashboard reading Pi parameters."""
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        d.rectangle((0, 0, 240, 35), fill="DARKGRAY")
        d.text((10, 10), "RASPBERRY PI HARDWARE STATS", fill="BLACK")

        # CPU Status Bar
        d.text((20, 60), f"CPU Usage: {cpu_pct}%", fill="WHITE")
        d.rectangle((20, 80, 220, 95), outline="WHITE", fill="BLACK")
        d.rectangle((20, 80, 20 + int(cpu_pct * 2), 95), fill="GREEN")

        # RAM Status Bar
        d.text((20, 130), f"RAM Usage: {ram_pct}%", fill="WHITE")
        d.rectangle((20, 150, 220, 165), outline="WHITE", fill="BLACK")
        d.rectangle((20, 150, 20 + int(ram_pct * 2), 165), fill="MAGENTA")

        d.text((20, 200), "[Press Joystick to Return]", fill="CYAN")

        self.disp.ShowImage(img.rotate(270))
