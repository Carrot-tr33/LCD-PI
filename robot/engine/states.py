# robot/engine/states.py
class SystemState:
    EYES = 0
    MENU = 1
    STATS = 2

    def __init__(self):
        self.current = SystemState.EYES

    def set_state(self, new_state):
        self.current = new_state