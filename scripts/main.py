# scripts/main.py
import time
import psutil
from robot.engine.eyes import RobotEyes
from robot.engine.controller import HardwareController

def main():
    eyes = RobotEyes()
    controller = HardwareController(eyes.disp)

    eyes.boot_sequence()

    # UI State management variables
    current_mode = "EYES" # Modes available: "EYES", "MENU", "STATS"
    menu_options = ["1. Animated Eyes", "2. System Stats", "3. Matrix Glitch"]
    selected_row = 0

    try:
        while True:
            # --- STATE 1: SELECTION MENU MODE ---
            if current_mode == "MENU":
                # Read structural layout tracking directions
                nav = controller.get_menu_navigation()
                if nav == "UP":
                    selected_row = (selected_row - 1) % len(menu_options)
                elif nav == "DOWN":
                    selected_row = (selected_row + 1) % len(menu_options)

                # Render menu graphic array
                eyes.draw_menu(menu_options, selected_row)

                # If selected button clicked down, switch core engine operational runtime mode
                if controller.is_joystick_pressed():
                    if selected_row == 0:
                        eyes.is_glitching = False
                        current_mode = "EYES"
                    elif selected_row == 1:
                        current_mode = "STATS"
                    elif selected_row == 2:
                        eyes.is_glitching = True
                        current_mode = "EYES"

            # --- STATE 2: HARDWARE STATS DISPLAY MODE ---
            elif current_mode == "STATS":
                # Gather actual real-time OS load details
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                eyes.draw_stats_page(cpu, ram)

                # Return safely to UI navigation panel if clicked again
                if controller.is_joystick_pressed():
                    current_mode = "MENU"

            # --- STATE 3: STANDARD RUNTIME SYSTEM (EYES / GLITCH) ---
            elif current_mode == "EYES":
                # Open menu layer overlay immediately if joystick clicked down
                if controller.is_joystick_pressed():
                    current_mode = "MENU"
                else:
                    # Keep checking physical emotional buttons only when eyes are active
                    if not eyes.is_glitching:
                        new_emotion = controller.get_target_emotion()
                        if new_emotion and eyes.emotion.name != new_emotion:
                            eyes.set_emotion(new_emotion)

                    # Update internal visual frameworks
                    eyes.update()
                    eyes.blink_update()
                    eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nExiting system loop cleanly...")
    finally:
        eyes.disp.module_exit()

if __name__ == "__main__":
    main()