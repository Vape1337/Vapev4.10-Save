import re
import subprocess
import tkinter as tk
import threading
import time

pause_event = threading.Event()
pause_event.set()

def filter_content():
    with open('settings.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    filtered_content = re.sub(r'[^A-Za-z0-9=]', '', content)
    with open('settings.txt', 'w', encoding='utf-8') as file:
        file.write(filtered_content)

def run_java_command():
    filter_content()
    command = ["java", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "-jar", "vape-loader.jar"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        check_for_616(line.strip())
        handle_stage_output(line.strip())

def check_for_616(output):
    match = re.search(r'616:\s*([A-Za-z0-9=]*)', output)
    if match:
        settings_content = match.group(1).strip()
        with open("settings.txt", "w", encoding="utf-8") as f:
            f.write(settings_content)
        filter_content()

def handle_stage_output(output):
    if "stage: 10" in output:
        pause_program()
    elif "stage: 18" in output:
        resume_program()

def pause_program():
    pause_event.clear()

def resume_program():
    pause_event.set()

def main_loop():
    while True:
        pause_event.wait()
        time.sleep(1)

def on_inject_button_click():
    subprocess.Popen(["load.exe"])
    threading.Thread(target=run_java_command, daemon=True).start()
    threading.Thread(target=main_loop, daemon=True).start()

root = tk.Tk()
root.title("Vape 启动器")

inject_button = tk.Button(root, text="注入", command=on_inject_button_click)
inject_button.pack(pady=20)

root.mainloop()
