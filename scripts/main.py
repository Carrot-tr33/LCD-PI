# scripts/main.py
import time
from robot.engine.eyes import RobotEyes
from robot.engine.controller import HardwareController

def main():
    eyes = RobotEyes()
    controller = HardwareController(eyes.disp)

    # Launch diagnostic display setup
    eyes.boot_sequence()

    print("System running smoothly. Hardware Listeners Active...")

    try:
        while True:
            # Polling hardware inputs cleanly
            new_emotion = controller.get_target_emotion()
            
            # If a button is pressed and it's a new state, swap it instantly
            if new_emotion and eyes.emotion.name != new_emotion:
                eyes.set_emotion(new_emotion)
                print(f"--> Switched Eye State To: {new_emotion.upper()}")

            # Standard animation ticks
            eyes.update()
            eyes.blink_update()
            eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nSystem closed safely via termination hook.")
    finally:
        eyes.disp.module_exit()

if __name__ == "__main__":
    main()