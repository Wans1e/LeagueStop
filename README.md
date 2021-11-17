# LeagueStop
Disables the chat in League of Legends for Windows, no setup needed.

![KEKW.png](KEKW.png)

### Install
1. Download LeagueStop __[here](...)__
2. Right-click LeagueStop and click "Run as administrator"
3. Play League of Legends

### Features
* Disables the chat in League of Legends
* Disables the Task Manager
* Runs upon login

#### Requirements
* Windows 10
* Python 3.6+

#### Usage
* Installing packages: pip install pywin32 keyboard playsound pyinstaller
* Building executable: pyinstaller -F -w -i KEKW.ico --add-data "KEKW.mp3;." LeagueStop.py
* Run using Python: python LeagueStop.py

#### Remove Autostart
1. Start: Command Prompt with administrator privileges
2. Paste: reg.exe delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /f
