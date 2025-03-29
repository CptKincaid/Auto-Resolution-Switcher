
Auto Resolution Switcher Tray App (Python Source Version v2)

Run Instructions:
1. Make sure you have Python 3.9+ installed.
2. Install dependencies:
   pip install pywin32 pystray pillow screeninfo keyboard
3. Run the script:
   python auto_resolution_switcher.py

Features:
- Auto detection only on OMEN 27K monitor
- Manual override hotkeys:
  Ctrl+F1 → Force 4K + disables auto
  Ctrl+F2 → Force 1080p + disables auto
  Ctrl+F3 → Re-enable auto mode
  Ctrl+F4 → Emergency Kill Switch
- Tray icon toggle & exit
- Cooldown & debounce protection
- Real-time logs and debugging output in terminal

How to install: 
1. Go to dist -> Output -> Double click Auto_Resolution_Installer
2. Double-click
3. Enjoy!

Things that need to be tweaked for better Plug And Play:
1. Currently hard wired for my monitor 3 (center montior) but your 4k monitor not be considered Display 3 so the code needs to be tweaked to recognize 4k capable monitors
2. Sometimes get errors that require you to Ctrl F3 to reenable auto mode.
Mode Ok...
[QRes] Switched to 1920x1080 using subprocess.
[Retry 1] Could not get window rect: (1400, 'GetWindowRect', 'Invalid window handle.')
[Retry 2] Could not get window rect: (1400, 'GetWindowRect', 'Invalid window handle.')
[Error] Skipping fullscreen check after multiple failures


