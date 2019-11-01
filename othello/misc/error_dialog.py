# Internal
import sys
import platform


def tkinter_error(msg: str) -> None:
    from tkinter import messagebox

    messagebox.showerror("Error", msg)


def windows_error(msg: str) -> None:
    import ctypes

    ctypes.windll.user32.MessageBoxW(None, msg, "Error", 0x10)


def zenity_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        ("zenity", "--error", "--no-wrap", "--text", msg),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def kdialog_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        ("kdialog", "--error", msg),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def applescript_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        ("osascript", "-e", f'display alert "{msg}" as critical buttons {{"ok"}}'),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def gui_error(msg: str) -> None:
    attempts = [tkinter_error]

    os = platform.system()

    if os == "Windows":
        attempts += [windows_error]
    elif os == "Linux":
        attempts += [kdialog_error, zenity_error]
    elif os == "Darwin":
        attempts += [applescript_error]

    for attempt in attempts:
        try:
            attempt(msg)
        except Exception:
            pass
        else:
            break
