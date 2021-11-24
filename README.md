# LeagueStop
Disables the chat in League of Legends for Windows. If you simply can't stop yourself from typing LeagueStop will play KEKW.mp3 each time you try. The sound will stack & becomes horribly annoying.

![KEKW.png](KEKW.png)

## Download
1. Download LeagueStop [here](https://github.com/Wans1e/LeagueStop/releases/download/Release/LeagueStop.exe)
2. Double-click LeagueStop
3. Play League of Legends

## Features
* Disables the chat in League of Legends
  * Plays KEKW.mp3 if you try
* Disables the Task Manager
* Runs upon login

---

## Requirements
* Windows 10
* Python 3.6+

## Installation
* **Installing packages:** pip install playsound==1.2.2 keyboard pywin32 pyinstaller
* **Building executable:** pyinstaller -F -w -i KEKW.ico --add-data KEKW.mp3;. LeagueStop.py
* **Run using Python:** python LeagueStop.py

## Remove Autostart
1. **Start:** Command Prompt with administrator privileges
2. **Paste:** reg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /f
