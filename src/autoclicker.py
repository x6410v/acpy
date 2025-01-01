import time
import threading
import random
import yaml
import pyautogui
from logger import log_info, log_error
from bezier import bezier_curve
from hotkey import HotkeyManager

# Load Configuration from YAML
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()['autoclicker']

# Autoclicker Class
class AutoClicker:
    def __init__(self):
        self.mode = config['mode']
        self.click_interval_min = config['click_interval_min']
        self.click_interval_max = config['click_interval_max']
        self.jitter_amount = config['jitter_amount']
        self.bezier_points = config['bezier_points']
        self.cursor_speed = config['cursor_speed']
        self.click_burst_count = config['click_burst_count']
        self.burst_delay_min = config['burst_delay_min']
        self.burst_delay_max = config['burst_delay_max']
        self.movement_cooldown = config['movement_cooldown']
        self.manual_tracking_interval = config['manual_tracking_interval']
        self.running = True
        self.hotkey_manager = HotkeyManager(self.toggle_mode)
        self.cps = 0

    def perform_click(self):
        for _ in range(self.click_burst_count):
            x, y = self.jitter_position(*pyautogui.position())
            pyautogui.click(x, y)
            self.cps += 1  # Increment CPS on each click
            time.sleep(random.uniform(self.burst_delay_min, self.burst_delay_max))

    def random_delay(self):
        return random.uniform(self.click_interval_min, self.click_interval_max)

    def jitter_position(self, x, y):
        return x + random.randint(-self.jitter_amount, self.jitter_amount), y + random.randint(-self.jitter_amount, self.jitter_amount)

    def move_cursor_automatically(self):
        try:
            start_pos = pyautogui.position()  # Initialize start_pos
            end_pos = (start_pos[0] + random.randint(-300, 300), start_pos[1] + random.randint(-300, 300))
            curve = bezier_curve(start_pos, end_pos, self.bezier_points)

            for point in curve:
                pyautogui.moveTo(point[0], point[1], duration=self.cursor_speed)
                self.cursor_overlay.update_cursor_asset(point[0], point[1])
                time.sleep(self.cursor_speed)
            time.sleep(self.movement_cooldown)
        except Exception as e:
            log_error(f"Error in move_cursor_automatically: {e}")

    def follow_user_cursor(self):
        while self.running:
            time.sleep(self.manual_tracking_interval)

    def perform_click(self):
        for _ in range(self.click_burst_count):
            x, y = self.jitter_position(*pyautogui.position())
            pyautogui.click(x, y)
            time.sleep(random.uniform(self.burst_delay_min, self.burst_delay_max))

    def run(self):
        log_info("Autoclicker started...")
        self.hotkey_manager.listen()

        if self.mode == "manual":
            threading.Thread(target=self.follow_user_cursor, daemon=True).start()

        try:
            while True:
                if self.mode == "automatic":
                    self.move_cursor_automatically()
                self.perform_click()
                time.sleep(self.random_delay())
        except KeyboardInterrupt:
            self.running = False
            log_error("Autoclicker stopped.")

    def toggle_mode(self):
        self.mode = "manual" if self.mode == "automatic" else "automatic"
        log_info(f"Mode switched to: {self.mode}")

if __name__ == "__main__":
    clicker = AutoClicker()
    clicker.run()