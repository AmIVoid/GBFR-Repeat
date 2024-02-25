import sys
import struct
import threading
from pymem import Pymem
from pymem.process import module_from_name
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

# Function to apply a dark theme to the app
def apply_dark_theme(app):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

# Global flag to control the memory writing loop
running = False

# Function to toggle memory write
def toggle_memory_write():
    global running
    running = not running
    if running:
        thread = threading.Thread(target=write_memory, daemon=True)
        thread.start()
        button.setText("Stop")
    else:
        button.setText("Start")

# Memory writing function with your logic
def write_memory():
    global running
    while running:
        try:
            target_addr = get_pointer_addr(module_base, pointer_offset)
            if target_addr > 0:
                mem.write_int(target_addr, 0)
        except Exception as e:
            print(f"Error occurred: {e}")
            running = False

# Function to calculate the pointer address
def get_pointer_addr(base_address, offset):
    bytes_read = mem.read_bytes(base_address + offset, 8)
    intermediate_addr, = struct.unpack('<Q', bytes_read)
    final_addr = intermediate_addr + final_offset
    return final_addr

# Initialize Pymem
mem = Pymem("granblue_fantasy_relink.exe")
module_base = module_from_name(mem.process_handle, "granblue_fantasy_relink.exe").lpBaseOfDll
pointer_offset = 0x06772160
final_offset = 0x4A0

# PyQt5 App
app = QApplication(sys.argv)

# Apply dark theme
apply_dark_theme(app)

window = QWidget()
window.setWindowTitle("GBFR Repeat")
window.setWindowIcon(QIcon(r'icon.ico'))
window.setFixedSize(250, 100)  # Set a fixed size for the window

layout = QVBoxLayout()

# Title Label
title_label = QLabel("Granblue Fantasy: Relink - Auto Repeat")
title_label.setAlignment(Qt.AlignCenter)  # Center-align the title
layout.addWidget(title_label)

# Toggle Button
button = QPushButton("Start")
button.clicked.connect(toggle_memory_write)
layout.addWidget(button)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
