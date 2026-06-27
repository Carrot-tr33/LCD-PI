import ST7789

class HardwareController:
    def __init__(self, display_instance):
        """
        Pass the existing display instance from RobotEyes 
        to avoid resource conflicts on the SPI bus.
        """
        self.disp = display_instance
        self.last_emotion = "neutral"

    def get_target_emotion(self):
        """
        Polls the hardware buttons. 
        Returns the new emotion string if a button is pressed, otherwise None.
        """
        # Active-low buttons: 0 means pressed
        if self.disp.digital_read(self.disp.GPIO_KEY1_PIN) == 0:
            return "happy"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY2_PIN) == 0:
            return "angry"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY3_PIN) == 0:
            return "gold"
            
        elif self.disp.digital_read(self.disp.GPIO_KEY_PRESS_PIN) == 0: # Center joystick press
            return "neutral"
            
        return None