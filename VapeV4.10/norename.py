import re
import subprocess
import threading
import os
from time import sleep

load_process = None

def filter_content():
    try:
        with open('settings.txt', 'r', encoding='utf-8') as file:
            content = file.read()

        filtered_content = re.sub(r'[^A-Za-z0-9=]', '', content)

        with open('settings.txt', 'w', encoding='utf-8') as file:
            file.write(filtered_content)
    except Exception as e:
        pass

def run_java_command():
    filter_content()

    command = ["java", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "-jar", "vape-loader.jar"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                check_for_616(line)
                check_for_stage(line)
    finally:
        process.stdout.close()

def check_for_616(output):
    match = re.search(r'616:\s*([A-Za-z0-9=]*)', output)
    if match:
        settings_content = match.group(1).strip()
        try:
            with open("settings.txt", "w", encoding="utf-8") as f:
                f.write(settings_content)
            filter_content()
        except Exception as e:
            pass

def check_for_stage(output):
    global load_process
    if load_process is None:
        return

def start_load_exe():
    global load_process
    sleep(7)
    load_path = "load.exe"
    if os.path.exists(load_path):
        load_process = subprocess.Popen([load_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_injection():
    global load_process
    if load_process is None:
        threading.Thread(target=start_load_exe).start()
    threading.Thread(target=run_java_command).start()

# 开始注入过程
start_injection()
