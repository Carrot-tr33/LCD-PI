from robot.core import ST7789

class HardwareController:
    def __init__(self, disp):
        self.disp = disp
        self.target_emotion = None

    def get_target_emotion(self):
        """
        Polls the physical buttons on the LCD hat.
        Returns the corresponding emotion string if pressed, otherwise None.
        """
        # Active-low buttons: 0 means the button is physically pressed down
        if self.disp.digital_read(self.disp.GPIO_KEY1_PIN) == 0:        # KEY1 / Button A
            return "happy"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY2_PIN) == 0:      # KEY2 / Button B
            return "angry"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY3_PIN) == 0:      # KEY3 / Button C
            return "gold"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY_PRESS_PIN) == 0: # Joystick Center Press
            return "neutral"
            
        return None