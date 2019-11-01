# Internal
import sys
import platform


def tkinter_error(msg: str) -> None:
    from tkinter import messagebox, Tk

    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showerror("Error", msg)


def windows_error(msg: str) -> None:
    import ctypes

    ctypes.windll.user32.MessageBoxW(None, msg, "Error", 0x10)


def yad_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        (
            "yad",
            f"--text={msg}",
            "--title=Error",
            "--image=gtk-dialog-error",
            "--center",
            "--on-top",
            "--border=15",
            "--escape-ok",
            "--button=OK:0",
            "--window-icon=gtk-execute",
        ),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


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


def xmessage_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        ("xmessage", "-xrm", "*international: true", "-title", "Error", "-center", msg,),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def applescript_error(msg: str) -> None:
    import subprocess

    subprocess.run(
        ("osascript", "-e", f'display alert "Error" message "{msg}" as critical buttons {{"ok"}}'),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def gui_error(msg: str) -> None:
    os = platform.system()

    if os == "Windows":
        attempts = [windows_error]
    elif os == "Linux":
        attempts = [kdialog_error, zenity_error, yad_error, xmessage_error]
    elif os == "Darwin":
        attempts = [applescript_error]
    else:
        attempts = []

    attempts.append(tkinter_error)

    for attempt in attempts:
        try:
            attempt(msg)
        except Exception:
            pass
        else:
            break
