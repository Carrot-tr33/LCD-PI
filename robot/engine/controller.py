from robot.core import ST7789

class HardwareController:
    def __init__(self, disp):
        self.disp = disp
        self.target_emotion = None

    def get_target_emotion(self):
        emotion = self.target_emotion
        self.target_emotion = None
        return emotion

    def set_emotion(self, emotion):
        self.target_emotion = emotion