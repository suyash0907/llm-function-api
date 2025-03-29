import os
import webbrowser
import psutil

def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    os.system("calc")

def open_notepad():
    if os.name == 'nt':  # Check if the OS is Windows
        os.system("notepad.exe")
    else:
        print("Operating system not supported for opening Notepad.")

def get_cpu_usage():
    return psutil.cpu_percent()

def get_ram_usage():
    return psutil.virtual_memory().percent

def run_command(command):
    os.system(command)
