import time
from robot.engine.eyes import RobotEyes
from robot.engine import sound

SOUND_ENABLED = False

def apply_emotion(eyes, name):
    eyes.set_emotion(name)

    if not SOUND_ENABLED:
        return

    if name == "happy":
        sound.happy()

    elif name == "angry":
        sound.warning()

    elif name == "neutral":
        sound.neutral()

    elif name == "gold":
        sound.chime_up()


def main():
    eyes = RobotEyes()

    try:
        while True:
            eyes.update()
            eyes.blink_update()
            eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        eyes.disp.module_exit()


if __name__ == "__main__":
    main()
