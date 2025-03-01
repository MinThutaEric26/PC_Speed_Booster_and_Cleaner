import os
import shutil
import subprocess
import ctypes
import sys
import psutil
import platform
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QProgressBar

# Function to request administrator privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    if not is_admin():
        # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

# Function to get system health (CPU, memory, and disk health)
def get_memory_health():
    memory = psutil.virtual_memory()
    if memory.percent > 90:
        return f"Warning: High memory usage ({memory.percent}%)"
    return f"Memory Usage: {memory.percent}%"

def get_cpu_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    try:
        cpu_temp = psutil.sensors_temperatures().get('cpu_thermal', None)
        if cpu_temp:
            temp = cpu_temp[0].current
            if temp > 80:
                return f"Warning: High CPU Temperature ({temp}°C)"
    except AttributeError:
        pass
    return f"CPU Usage: {cpu_usage}%"

def get_disk_health():
    disk_usage = psutil.disk_usage('/')
    free_space = disk_usage.free / (1024 ** 3)  # GB
    total_space = disk_usage.total / (1024 ** 3)  # GB
    if free_space < 10:
        return f"Warning: Low Disk Space ({free_space:.2f}GB free of {total_space:.2f}GB)"
    return f"Disk Space: {free_space:.2f}GB free of {total_space:.2f}GB"

def get_system_info():
    os_info = platform.uname()
    os_version = os_info.system + " " + os_info.release
    cpu_count = psutil.cpu_count(logical=False)
    cpu_model = platform.processor()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 ** 3)  # GB
    used_memory = memory.used / (1024 ** 3)    # GB
    free_memory = memory.free / (1024 ** 3)    # GB
    disk_usage = psutil.disk_usage('/')
    total_disk = disk_usage.total / (1024 ** 3)  # GB
    free_disk = disk_usage.free / (1024 ** 3)    # GB
    system_info = {
        "OS": os_version,
        "CPU": f"{cpu_model} ({cpu_count} cores)",
        "CPU Usage": f"{cpu_usage}%",
        "Memory": f"{used_memory:.2f}GB / {total_memory:.2f}GB",
        "Disk": f"{free_disk:.2f}GB free of {total_disk:.2f}GB"
    }
    return system_info

# SciFi Cleanup Tool class
class SciFiCleanupTool(QWidget):
    def __init__(self):
        super().__init__()

        # Request admin privileges before starting the app
        run_as_admin()

        # Set up the window
        self.setWindowTitle("Cleanup & Boost Tool")
        self.setFixedSize(900, 400)

        # Set a modern and professional theme
        self.set_theme()

        # Create layout and widgets
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Windows 10/11 Cleanup & Performance Boost Tool Developed by Min Thuta Saw Naing", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: yellow; font-size: 18px; font-family: 'Arial'; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Status label
        self.status_label = QLabel("System ready for cleanup...", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: yellow; font-size: 14px; font-family: 'Arial';")
        layout.addWidget(self.status_label)

        # Log box
        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("""
            background-color: #1e1e1e;
            color: #00FF00;
            border: 2px solid yellow;
            font-size: 12px;
            font-family: 'Arial';
        """)
        layout.addWidget(self.log_box)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 4px solid yellow;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00FF00;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Start button
        self.start_button = QPushButton("Start Cleanup", self)
        self.start_button.setStyleSheet("""
            background-color: #1e1e1e;
            color: white;
            border: 2px solid yellow;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
        """)
        self.start_button.setFont(QFont('Arial', 14))
        self.start_button.clicked.connect(self.start_cleanup)
        layout.addWidget(self.start_button)

        # Add widgets to the layout
        self.setLayout(layout)

        # Automatically display system information when the app starts
        self.display_system_info()

    def set_theme(self):
        # Set a dark, sleek sci-fi palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Dark background
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 0))  # Green text
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))  # Button background
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 255, 0))  # Button text color
        self.setPalette(palette)

    def start_cleanup(self):
        self.status_label.setText("Activating system cleanup...")
        self.start_button.setDisabled(True)

        # Reset progress bar
        self.progress_bar.setValue(0)

        # Adding a delay to simulate a sci-fi "processing" effect
        QTimer.singleShot(1000, self.clean_temp_files)
        QTimer.singleShot(2000, self.clean_system_logs)
        QTimer.singleShot(3000, self.clear_recycle_bin)
        QTimer.singleShot(4000, self.run_disk_cleanup)
        QTimer.singleShot(5000, self.defrag_disk)

    def log_message(self, message):
        self.log_box.append(message)

    def clean_temp_files(self):
        self.status_label.setText("Cleaning temporary files...")
        self.log_message("Cleaning temporary files...")
        self.progress_bar.setValue(20)

        temp_paths = [os.getenv("TEMP"), "C:\\Windows\\Temp"]
        for path in temp_paths:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.log_message(f"Error cleaning {file_path}: {e}")

        self.log_message("Temporary files cleaned.")
        self.progress_bar.setValue(40)

    def clean_system_logs(self):
        self.status_label.setText("Cleaning system logs...")
        self.log_message("Cleaning system logs...")
        self.progress_bar.setValue(60)

        log_path = "C:\\Windows\\System32\\winevt\\Logs"
        if os.path.exists(log_path):
            for log_file in os.listdir(log_path):
                try:
                    os.remove(os.path.join(log_path, log_file))
                except Exception as e:
                    self.log_message(f"Error cleaning system log {log_file}: {e}")
        self.log_message("System logs cleaned.")
        self.progress_bar.setValue(80)

    def clear_recycle_bin(self):
        self.status_label.setText("Emptying the Recycle Bin...")
        self.log_message("Emptying the Recycle Bin...")
        recycle_bin_path = "C:\\$Recycle.Bin"
        try:
            shutil.rmtree(recycle_bin_path)
        except Exception as e:
            self.log_message(f"Error clearing Recycle Bin: {e}")
        self.log_message("Recycle Bin emptied.")
        self.progress_bar.setValue(100)

    def run_disk_cleanup(self):
        self.status_label.setText("Running Disk Cleanup...")
        self.log_message("Running Disk Cleanup...")
        try:
            subprocess.run("cleanmgr /sagerun:1", check=True)
        except Exception as e:
            self.log_message(f"Error running Disk Cleanup: {e}")
        self.log_message("Disk Cleanup completed.")

    def defrag_disk(self):
        self.status_label.setText("Defragmenting Disk...")
        self.log_message("Defragmenting Disk...")
        try:
            subprocess.run("defrag C: /O", check=True)
        except Exception as e:
            self.log_message(f"Error defragmenting disk: {e}")
        self.log_message("Disk defragmentation completed.")

        # Add "Clean Up Done" message at the end
        self.log_message("Clean Up Done.")
        

    def display_system_info(self):
        system_info = get_system_info()
        self.log_message("\nSystem Information:")
        for key, value in system_info.items():
            self.log_message(f"{key}: {value}")

        self.log_message("\nSystem Health:")
        self.log_message(get_memory_health())
        self.log_message(get_cpu_health())
        self.log_message(get_disk_health())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SciFiCleanupTool()
    window.show()
    sys.exit(app.exec())
