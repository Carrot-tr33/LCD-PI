# robot/engine/controller.py
import time

class HardwareController:
    def __init__(self, disp):
        self.disp = disp
        
        # Map physical pins directly to emotion string profiles
        self.EMOTION_MAP = {
            self.disp.GPIO_KEY1_PIN: "happy",
            self.disp.GPIO_KEY2_PIN: "angry",
            self.disp.GPIO_KEY3_PIN: "gold",
            self.disp.GPIO_KEY_PRESS_PIN: "glitch" # Joystick press now triggers glitch emotion!
        }

    def is_pressed(self, pin):
        """Standardized helper to read active-high physical pins."""
        return self.disp.digital_read(pin) == 1

    def get_target_emotion(self):
        """Iterates through mapped pins to return the triggered emotion string."""
        for pin, emotion_name in self.EMOTION_MAP.items():
            if self.is_pressed(pin):
                time.sleep(0.15) # Universal debounce delay
                return emotion_name
        return None