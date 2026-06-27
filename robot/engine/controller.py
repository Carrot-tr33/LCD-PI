from robot.core import ST7789
import time

class HardwareController:
    def __init__(self, disp):
        self.disp = disp
        self.target_emotion = None

    def is_joystick_pressed(self):
        """Returns True if the center joystick is currently held down, else False."""
        return self.disp.digital_read(self.disp.GPIO_KEY_PRESS_PIN) == 1

    def get_target_emotion(self):

        # Active-high buttons (== 1 means pressed down)
        if self.disp.digital_read(self.disp.GPIO_KEY1_PIN) == 1:       # KEY1 / Button A
            time.sleep(0.15)        
            return "happy"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY2_PIN) == 1:      # KEY2 / Button B
            time.sleep(0.15)
            return "angry"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY3_PIN) == 1:      # KEY3 / Button C
            time.sleep(0.15)
            return "gold"
            
            
        return None