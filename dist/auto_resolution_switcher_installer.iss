[Setup]
AppName=Auto Resolution Switcher
AppVersion=1.0.0
AppPublisher=Cpt Kincaid
DefaultDirName={autopf}\Auto Resolution Switcher
DefaultGroupName=Auto Resolution Switcher
UninstallDisplayIcon={app}\auto_resolution_switcher.exe
OutputBaseFilename=Auto_Resolution_Switcher_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
PrivilegesRequired=admin

[Files]
Source: "auto_resolution_switcher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Auto Resolution Switcher"; Filename: "{app}\auto_resolution_switcher.exe"
Name: "{group}\Uninstall Auto Resolution Switcher"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Auto Resolution Switcher"; Filename: "{app}\auto_resolution_switcher.exe"; Tasks: desktopicon
Name: "{userstartup}\Auto Resolution Switcher"; Filename: "{app}\auto_resolution_switcher.exe"; Tasks: autostart

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop Shortcut"; GroupDescription: "Additional Icons"
Name: "autostart"; Description: "Start automatically with Windows"; GroupDescription: "Startup"
