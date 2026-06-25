import subprocess
import threading

BLINK_SOUND = "/home/carrot/Robot/blink_sound.mp3"

def play_blink():
    threading.Thread(
        target=lambda: subprocess.run(
            [
                "mpg123",
                "-q",
                "-a",
                "bluealsa",
                BLINK_SOUND
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ),
        daemon=True
    ).start()
