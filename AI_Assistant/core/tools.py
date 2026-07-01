import os
import subprocess
import webbrowser


def open_windows_app(app_name):

    common_apps = {

        "vscode":
        r"C:\Users\Ol'sola\AppData\Local\Programs\Microsoft VS Code\Code.exe",

        "notepad":
        "notepad.exe",

        "calculator":
        "calc.exe",

        "paint":
        "mspaint.exe",

        "powershell":
        "powershell.exe",

        "terminal":
        "wt.exe",

        "task manager":
        "taskmgr.exe",

        "file explorer":
        "explorer.exe",

        "edge":
        "msedge.exe"

    }

    if app_name in common_apps:

        subprocess.Popen(common_apps[app_name])

        return True

    return False


def handle_command(command):

    command = command.lower().strip()

    if command.startswith("open "):

        target = command.replace("open ", "")

        special = {

            "settings":
            "ms-settings:",

            "microsoft store":
            "ms-windows-store:",

            "xbox":
            "xbox:",

            "camera":
            "microsoft.windows.camera:",

            "photos":
            "ms-photos:"
        }

        if target in special:

            os.startfile(special[target])

            return f"Opening {target}"

        if open_windows_app(target):

            return f"Opening {target}"

        try:

            os.system(f'start "" "{target}"')

            return f"Trying to open {target}"

        except Exception:

            return f"Could not open {target}"

    if "youtube" in command:

        webbrowser.open("https://youtube.com")

        return "Opening YouTube"

    if "google" in command:

        webbrowser.open("https://google.com")

        return "Opening Google"

    return None