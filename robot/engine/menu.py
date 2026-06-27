# robot/engine/menu.py
import psutil
from PIL import Image, ImageDraw

class RobotMenu:
    def __init__(self, disp):
        self.disp = disp
        self.options = ["1. Animated Eyes", "2. System Stats", "3. Matrix Glitch"]
        self.selected_row = 0

    def navigate(self, direction):
        """Adjusts the highlighted menu row index safely."""
        if direction == "UP":
            self.selected_row = (self.selected_row - 1) % len(self.options)
        elif direction == "DOWN":
            self.selected_row = (self.selected_row + 1) % len(self.options)

    def draw_main_menu(self):
        """Renders the main choice selection screen."""
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        # Draw Header Bar
        d.rectangle((0, 0, 240, 35), fill="BLUE")
        d.text((10, 10), "SYSTEM MAIN MENU", fill="WHITE")
        d.line((0, 35, 240, 35), fill="WHITE", width=2)

        # Render rows dynamically
        start_y = 60
        for index, option in enumerate(self.options):
            y_pos = start_y + (index * 40)
            if index == self.selected_row:
                d.rectangle((10, y_pos - 5, 230, y_pos + 25), outline="CYAN", fill="#112233")
                d.text((25, y_pos), f"> {option}", fill="CYAN")
            else:
                d.text((25, y_pos), f"  {option}", fill="LIGHTGRAY")

        self.disp.ShowImage(img.rotate(270))

    def draw_stats_page(self):
        """Queries hardware variables and renders a dashboard panel."""
        img = Image.new("RGB", (240, 240), "BLACK")
        d = ImageDraw.Draw(img)

        # Query metrics via OS bindings
        cpu_pct = psutil.cpu_percent()
        ram_pct = psutil.virtual_memory().percent

        d.rectangle((0, 0, 240, 35), fill="DARKGRAY")
        d.text((10, 10), "RASPBERRY PI HARDWARE STATS", fill="BLACK")

        # CPU load progress bar
        d.text((20, 60), f"CPU Usage: {cpu_pct}%", fill="WHITE")
        d.rectangle((20, 80, 220, 95), outline="WHITE", fill="BLACK")
        d.rectangle((20, 80, 20 + int(cpu_pct * 2), 95), fill="GREEN")

        # RAM allocation progress bar
        d.text((20, 130), f"RAM Usage: {ram_pct}%", fill="WHITE")
        d.rectangle((20, 150, 220, 165), outline="WHITE", fill="BLACK")
        d.rectangle((20, 150, 20 + int(ram_pct * 2), 165), fill="MAGENTA")

        d.text((20, 200), "[Press Joystick to Return]", fill="CYAN")
        self.disp.ShowImage(img.rotate(270))