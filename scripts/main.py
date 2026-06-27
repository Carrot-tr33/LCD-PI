# scripts/main.py
import time
from robot.engine.eyes import RobotEyes
from robot.engine.controller import HardwareController
from robot.engine.menu import RobotMenu
from robot.engine.states import SystemState

def main():
    # Instantiate standalone layout pieces
    eyes = RobotEyes()
    controller = HardwareController(eyes.disp)
    menu = RobotMenu(eyes.disp)
    state = SystemState()

    # Hardware wake-up run-through
    eyes.boot_sequence()

    try:
        while True:
            # Check if joystick core button clicked down
            joystick_click = controller.is_joystick_pressed()

            # --- SYSTEM ROUTING MATRIX BASED ON STATE ---
            
            if state.current == SystemState.MENU:
                # Read directional inputs
                nav = controller.get_menu_navigation()
                if nav:
                    menu.navigate(nav)
                
                menu.draw_main_menu()

                if joystick_click:
                    if menu.selected_row == 0:
                        eyes.is_glitching = False
                        state.set_state(SystemState.EYES)
                    elif menu.selected_row == 1:
                        state.set_state(SystemState.STATS)
                    elif menu.selected_row == 2:
                        eyes.is_glitching = True
                        state.set_state(SystemState.EYES)

            elif state.current == SystemState.STATS:
                menu.draw_stats_page()
                if joystick_click:
                    state.set_state(SystemState.MENU)

            elif state.current == SystemState.EYES:
                if joystick_click:
                    state.set_state(SystemState.MENU)
                else:
                    # Update background quick-keys if not locked into hardware glitch mode
                    if not eyes.is_glitching:
                        new_emotion = controller.get_target_emotion()
                        if new_emotion and eyes.emotion.name != new_emotion:
                            eyes.set_emotion(new_emotion)

                    eyes.update()
                    eyes.blink_update()
                    eyes.draw()

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nShutdown hook caught.")
    finally:
        eyes.disp.module_exit()

if __name__ == "__main__":
    main()