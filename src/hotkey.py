import keyboard
import yaml

config = yaml.safe_load(open('config.yaml'))['autoclicker']

class HotkeyManager:
    def __init__(self, toggle_callback):
        self.hotkey = config['hotkey_toggle']
        self.toggle_callback = toggle_callback

    def listen(self):
        keyboard.add_hotkey(self.hotkey, self.toggle_callback)