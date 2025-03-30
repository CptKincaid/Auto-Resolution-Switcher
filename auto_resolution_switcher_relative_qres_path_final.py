import time
import threading
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image
import win32gui
import win32api
import keyboard
import ctypes
import sys
import os

# --- Configuration ---
AUTO_MODE = True
print("[Init] Auto Mode forced ON at startup")
IS_4K = False
COOLDOWN = 5  # seconds
QRES_PATH = os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "QRes.exe")
RES_4K = ["3840", "2160"]
RES_1080P = ["1920", "1080"]
# ----------------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_qres(resolution):
    try:
        print(f"[QRes] Attempting resolution switch to {resolution[0]}x{resolution[1]}")
        subprocess.run([QRES_PATH, "/x", resolution[0], "/y", resolution[1]], check=True)
        print(f"[QRes] Switched to {resolution[0]}x{resolution[1]} using subprocess.")
    except Exception as e:
        print(f"[Error] Subprocess QRes failed: {e}")
        print("[QRes] Trying fallback PowerShell method...")
        try:
            ps_cmd = f'Start-Process -FilePath "{os.path.abspath(QRES_PATH)}" -ArgumentList "/x {resolution[0]} /y {resolution[1]}"'
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            print(f"[QRes] Switched to {resolution[0]}x{resolution[1]} using PowerShell fallback.")
        except Exception as e2:
            print(f"[Fatal] Both QRes methods failed: {e2}")

def switch_to_4k():
    global IS_4K
    IS_4K = True
    run_qres(RES_4K)

def switch_to_1080p():
    global IS_4K
    IS_4K = False
    run_qres(RES_1080P)

def check_fullscreen():
    global AUTO_MODE, IS_4K
    while True:
        if AUTO_MODE:
            fg_window = win32gui.GetForegroundWindow()
            retry_attempts = 5
            for attempt in range(retry_attempts):
                try:
                    rect = win32gui.GetWindowRect(fg_window)
                    break
                except win32gui.error as e:
                    print(f"[Retry {attempt+1}] Could not get window rect: {e}")
                    time.sleep(0.3)
            else:
                print("[Warning] Skipping fullscreen check after multiple failures")
                time.sleep(COOLDOWN)
                continue


            monitor = win32api.MonitorFromWindow(fg_window)
            monitor_info = win32api.GetMonitorInfo(monitor)
            device_name = monitor_info['Device']
            if device_name != '\\\\.\\DISPLAY3':
                print(f"[Skip] Fullscreen window is not on middle (4K) monitor: {device_name}")
                time.sleep(COOLDOWN)
                continue

            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            if rect[2] == screen_width and rect[3] == screen_height:
                if not IS_4K:
                    print("[Auto] Fullscreen detected - Switching to 4K")
                    switch_to_4k()
            else:
                if IS_4K:
                    print("[Auto] Fullscreen exited - Switching to 1080p")
                    switch_to_1080p()
        time.sleep(COOLDOWN)

def toggle_auto(icon, item):
    global AUTO_MODE
    AUTO_MODE = not AUTO_MODE
    source = "[Tray]" if icon else "[Hotkey]"
    print(f"{source} Ctrl+F3 - Toggled Auto Mode: {'ON' if AUTO_MODE else 'OFF'}")


def exit_app(icon, item):
    print("[Exit] App is closing.")
    icon.stop()
    sys.exit()

def start_tray():
    image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    menu = Menu(
        MenuItem('Force 4K', lambda: (disable_auto(), print('[Tray] Force 4K Selected'), switch_to_4k())),
        MenuItem('Force 1080p', lambda: (disable_auto(), print('[Tray] Force 1080p Selected'), switch_to_1080p())),
        MenuItem('Toggle Auto Mode', toggle_auto),
        MenuItem('Exit', exit_app)
    )
    icon = Icon("Resolution Switcher", image, "Res Switcher", menu)
    icon.run()

def start_hotkeys():
    keyboard.add_hotkey('ctrl+f1', lambda: (disable_auto(), print("[Hotkey] Ctrl+F1 - Force 4K"), switch_to_4k()))
    keyboard.add_hotkey('ctrl+f2', lambda: (disable_auto(), print("[Hotkey] Ctrl+F2 - Force 1080p"), switch_to_1080p()))
    keyboard.add_hotkey('ctrl+f3', lambda: (toggle_auto(None, None), print(f"[Hotkey] Ctrl+F3 - Toggled Auto Mode: {'ON' if AUTO_MODE else 'OFF'}")))
    keyboard.add_hotkey('ctrl+f4', lambda: (print("[Hotkey] Ctrl+F4 - Emergency Kill"), sys.exit()))
    keyboard.wait()

def disable_auto():
    global AUTO_MODE
    AUTO_MODE = False
    print("[Toggle] Auto Mode: OFF")

def enable_auto():
    global AUTO_MODE
    AUTO_MODE = True
    print("[Toggle] Auto Mode: ON")

if __name__ == "__main__":
    if not is_admin():
        print("[Warning] Script is NOT running as Administrator. Hotkeys may not work.")

    # Auto Mode always ON at startup
    AUTO_MODE = True

    # Detect current resolution
    displays = win32api.EnumDisplaySettings("\\\\.\\DISPLAY3", -1)
    current_width = displays.PelsWidth
    current_height = displays.PelsHeight
    IS_4K = (current_width == 3840 and current_height == 2160)
    print(f"[Init] Auto Mode: ON | Current Resolution: {current_width}x{current_height} | IS_4K = {IS_4K}")

    print("[Start] Auto Resolution Switcher running...")
    threading.Thread(target=check_fullscreen, daemon=True).start()
    threading.Thread(target=start_hotkeys, daemon=True).start()
    start_tray()
