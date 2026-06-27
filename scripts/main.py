# scripts/main.py
import time
from robot.engine.eyes import RobotEyes
from robot.engine.controller import HardwareController

def apply_emotion(eyes, name):
    """Updates the internal visual emotion profile state cleanly."""
    eyes.set_emotion(name)
    print(f"--> Switched Eye State To: {name.upper()}")


def main():
    eyes = RobotEyes()
    controller = HardwareController(eyes.disp)

    eyes.boot_sequence()

    print("System running. Control Layout Configuration:")
    print(" [KEY1] -> Happy  |  [KEY2] -> Angry  |  [KEY3] -> Gold  |  [JOYSTICK] -> Neutral")

    try:
        while True:
            # 1. Check if the user is forcing a system glitch
            if controller.is_joystick_pressed():
                eyes.is_glitching = True
            else:
                eyes.is_glitching = False

            # 2. Process other emotional state key presses if not glitching
            if not eyes.is_glitching:
                new_emotion = controller.get_target_emotion()
                if new_emotion and eyes.emotion.name != new_emotion:
                    apply_emotion(eyes, new_emotion)

            # 3. Standard screen refresh and interpolation step
            eyes.update()
            eyes.blink_update()
            eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Exiting cleanly...")
    finally:
        eyes.disp.module_exit()


if __name__ == "__main__":
    main()