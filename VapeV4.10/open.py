import re
import subprocess
import tkinter as tk
import threading
import os
import psutil
import time

load_process = None
paused_event = threading.Event()

def filter_content():
    try:
        with open('settings.txt', 'r', encoding='utf-8') as file:
            content = file.read()

        filtered_content = re.sub(r'[^A-Za-z0-9=]', '', content)

        with open('settings.txt', 'w', encoding='utf-8') as file:
            file.write(filtered_content)

        print("$root@127.0.0.1 Settings >> 已经删除并转码")
    
    except FileNotFoundError:
        print("Error: settings.txt 文件未找到。请确保文件存在并重试。")

def run_java_command():
    filter_content()

    command = ["java", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "-jar", "vape-loader.jar"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        print(line.strip())
        check_for_616(line.strip())
        check_for_stage(line.strip())

def check_for_616(output):
    match = re.search(r'616:\s*([A-Za-z0-9=]*)', output)
    if match:
        settings_content = match.group(1).strip()
        with open("settings.txt", "w", encoding="utf-8") as f:
            f.write(settings_content)
        print("已将内容写入 settings.txt:", settings_content)
        filter_content()

def check_for_stage(output):
    global load_process
    if load_process is None:
        return
    
    pid = load_process.pid
    
    if "stage: 21" in output:
        print("检测到 stage: 21，程序将进入未响应状态")
        suspend_process(pid)
        paused_event.clear()  # 设置阻塞
        paused_event.wait()    # 程序挂起，等待信号解除
    elif "stage: 28" in output:
        print("检测到 stage: 28，程序将恢复响应")
        resume_process(pid)
        paused_event.set()     # 恢复响应

def suspend_process(pid):
    process = psutil.Process(pid)
    for thread in process.threads():
        thread_handle = ctypes.windll.kernel32.OpenThread(0x2, False, thread.id)
        if thread_handle:
            ctypes.windll.kernel32.SuspendThread(thread_handle)
            ctypes.windll.kernel32.CloseHandle(thread_handle)
    print(f"已暂停进程 {pid} 的所有线程")

def resume_process(pid):
    process = psutil.Process(pid)
    for thread in process.threads():
        thread_handle = ctypes.windll.kernel32.OpenThread(0x2, False, thread.id)
        if thread_handle:
            ctypes.windll.kernel32.ResumeThread(thread_handle)
            ctypes.windll.kernel32.CloseHandle(thread_handle)
    print(f"已恢复进程 {pid} 的所有线程")

def start_load_exe():
    global load_process
    load_path = "load.exe"
    if os.path.exists(load_path):
        load_process = subprocess.Popen([load_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("已启动 load.exe")
    else:
        print("未找到 load.exe 文件")

def on_inject_button_click():
    global load_process
    if load_process is None:
        threading.Thread(target=start_load_exe).start()
    threading.Thread(target=run_java_command).start()

root = tk.Tk()
root.title("Vape 启动器")

inject_button = tk.Button(root, text="注入", command=on_inject_button_click)
inject_button.pack(pady=20)

root.mainloop()
