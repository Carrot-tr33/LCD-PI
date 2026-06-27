import time
from robot.engine import controller
from robot.engine.eyes import RobotEyes
from robot.engine import sound
from robot.engine.controller import HardwareController



def apply_emotion(eyes, name):
    eyes.set_emotion(name)

    controller.set_emotion(name)

    print("System running. Use KEY1, KEY2, KEY3, or Joystick Press to change emotions.")

def main():
    eyes = RobotEyes()
    controller = HardwareController(eyes.disp)

    print("System running. Control Layout Configuration:")
    print(" [KEY1] -> Happy  |  [KEY2] -> Angry  |  [KEY3] -> Gold  |  [JOYSTICK] -> Neutral")

    try:
        while True:

            # 1. Check for button inputs via our external module
            new_emotion = controller.get_target_emotion()

            # 2. If a new emotion is detected, apply it to the eyes
            if new_emotion and eyes.emotion.name != new_emotion:
                apply_emotion(eyes, new_emotion)

            eyes.update()
            eyes.blink_update()
            eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        eyes.disp.module_exit()
    finally:
        eyes.disp.module_exit()


if __name__ == "__main__":
    main()
