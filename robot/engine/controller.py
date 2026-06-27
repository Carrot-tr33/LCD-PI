import time
from robot.engine.emotions import EMOTIONS

class HardwareController:
    def __init__(self, disp):
        self.disp = disp
        
        # 1. Store a clean, indexable list of all available emotion names
        self.emotion_pool = list(EMOTIONS.keys())
        self.current_index = 0
        
        # 2. Map physical pins to cycle direction commands
        # Assumes GPIO_KEY_LEFT_PIN and GPIO_KEY_RIGHT_PIN exist on your ST7789 board object
        self.LEFT_PIN = self.disp.GPIO_KEY_LEFT_PIN
        self.RIGHT_PIN = self.disp.GPIO_KEY_RIGHT_PIN

        # 3. Track the previous button state to prevent rapid machine-gun scrolling
        self.last_left_state = 0
        self.last_right_state = 0

    def get_target_emotion(self):
        """
        Polls the left/right pins, detects single directional clicks, 
        and calculates the next or previous emotion profile in line.
        """
        # Read raw current physical states
        current_left = self.disp.digital_read(self.LEFT_PIN)
        current_right = self.disp.digital_read(self.RIGHT_PIN)
        
        target_emotion = None

        # --- CYCLE LEFT (Previous Emotion) ---
        # Triggers ONLY on transition: was 0 (centered), now is 1 (tilted left)
        if current_left == 1 and self.last_left_state == 0:
            self.current_index = (self.current_index - 1) % len(self.emotion_pool)
            target_emotion = self.emotion_pool[self.current_index]
            time.sleep(0.05)  # Quick software debounce micro-delay

        # --- CYCLE RIGHT (Next Emotion) ---
        # Triggers ONLY on transition: was 0 (centered), now is 1 (tilted right)
        elif current_right == 1 and self.last_right_state == 0:
            self.current_index = (self.current_index + 1) % len(self.emotion_pool)
            target_emotion = self.emotion_pool[self.current_index]
            time.sleep(0.05)  # Quick software debounce micro-delay

        # Save states for the next execution loop cycle comparison
        self.last_left_state = current_left
        self.last_right_state = current_right

        return target_emotion