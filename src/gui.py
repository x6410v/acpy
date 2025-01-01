from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QApplication)
from PyQt6.QtCore import Qt, QTimer  # Fixed import for QTimer
import yaml
import threading

# Load Configuration
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

class ControlPanel(QWidget):
    def __init__(self, autoclicker):
        super().__init__()
        self.setWindowTitle("Autoclicker Control Panel")
        self.autoclicker = autoclicker
        self.cps_counter = 0

        # Layout Setup
        layout = QVBoxLayout()

        # CPS Display
        self.cps_label = QLabel("CPS: 0")
        layout.addWidget(self.cps_label)

        # Sliders for Click Intervals
        self.interval_slider = self.create_slider("Click Interval (ms)", 1, 100, autoclicker.click_interval_min * 1000)
        self.jitter_slider = self.create_slider("Jitter Amount (px)", 0, 50, autoclicker.jitter_amount)
        self.speed_slider = self.create_slider("Cursor Speed (s)", 0, 50, autoclicker.cursor_speed * 1000)

        # Mode Toggle Button
        self.toggle_button = QPushButton("Switch Mode (Current: Manual)")
        self.toggle_button.clicked.connect(self.toggle_mode)

        # Stop Button
        stop_button = QPushButton("Stop Autoclicker")
        stop_button.clicked.connect(self.stop_autoclicker)

        # Add Widgets to Layout
        layout.addWidget(self.interval_slider['label'])
        layout.addWidget(self.interval_slider['slider'])
        layout.addWidget(self.jitter_slider['label'])
        layout.addWidget(self.jitter_slider['slider'])
        layout.addWidget(self.speed_slider['label'])
        layout.addWidget(self.speed_slider['slider'])
        layout.addWidget(self.toggle_button)
        layout.addWidget(stop_button)

        self.setLayout(layout)
        self.update_button_text()

        # Timer for Live CPS Monitoring
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cps)
        self.timer.start(1000)  # Update CPS every second

    # Slider Factory
    def create_slider(self, text, min_val, max_val, initial_value):
        label = QLabel(f"{text}: {initial_value}")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(lambda: self.slider_changed(label, slider, text))
        return {"label": label, "slider": slider}

    # Update Slider Values
    def slider_changed(self, label, slider, text):
        label.setText(f"{text}: {slider.value()}")
        if "Interval" in text:
            self.autoclicker.click_interval_min = slider.value() / 1000
            self.autoclicker.click_interval_max = slider.value() / 1000
        elif "Jitter" in text:
            self.autoclicker.jitter_amount = slider.value()
        elif "Speed" in text:
            self.autoclicker.cursor_speed = slider.value() / 1000

    # Toggle Autoclicker Mode
    def toggle_mode(self):
        self.autoclicker.toggle_mode()
        self.update_button_text()

    def update_button_text(self):
        current_mode = self.autoclicker.mode.capitalize()
        self.toggle_button.setText(f"Switch Mode (Current: {current_mode})")

    # Stop Autoclicker
    def stop_autoclicker(self):
        self.autoclicker.running = False
        self.close()

    # CPS Monitoring - Update Label
    def update_cps(self):
        self.cps_label.setText(f"CPS: {self.autoclicker.cps}")
        self.autoclicker.cps = 0  # Reset CPS every second

# Launch GUI
def run_gui(autoclicker):
    app = QApplication([])
    control_panel = ControlPanel(autoclicker)
    control_panel.show()
    app.exec()