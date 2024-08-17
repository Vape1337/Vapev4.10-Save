import subprocess
import tkinter as tk
import re
import os
os.system('del.exe') #运行del.exe文件
def run_java_command():
    # 更改时间
    spoof = r'RunAsDate.exe 19\09\2015 13:37:37 Attach:cmd.exe & RunAsDate.exe 19\09\2015 13:37:37 Attach:cmdjavaw.exe'
    # 启动指令
    os.system('del.exe') #运行del.exe文件
    command = ["./jdk-17/bin/java", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "-jar", "vape-loader.jar"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # 输出获取
    for line in process.stdout:
        print(line.strip())  # 打印到控制台
        check_for_616(line.strip())

def check_for_616(output):
    # 检查是否包含 "616:"，没有特殊字符
    match = re.search(r'616:\s*([^!\@\#\$\%\^\&\*\(\)\[\]\{\};:\'",\/\\]*)', output)
    if match:
        # 获取 "616:" 后面的内容
        settings_content = match.group(1).strip()
        # 写入 settings.txt 文件
        with open("settings.txt", "w", encoding="utf-8") as f:  # 添加 encoding="utf-8"
            f.write(settings_content) 
        print("已将内容写入 settings.txt:", settings_content)

def on_inject_button_click():
    run_java_command()

# 创建 GUI 界面
root = tk.Tk()
root.title("Vape启动器")

inject_button = tk.Button(root, text="注入", command=on_inject_button_click)
inject_button.pack(pady=20)

root.mainloop()

