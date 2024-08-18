import re
import subprocess
import tkinter as tk

# 读取并过滤 settings.txt 文件
def filter_content():
    with open('settings.txt', 'r', encoding='utf-8') as file:
        content = file.read() 

    # 删除所有非字母数字和等号的字符
    filtered_content = re.sub(r'[^A-Za-z0-9=]', '', content)

    # 写回文件
    with open('settings.txt', 'w', encoding='utf-8') as file:
        file.write(filtered_content)

    print("$root@127.0.0.1 Settings >> 已经删除并转码")

# 运行 Java 命令
def run_java_command():
    filter_content()  # 先执行内容过滤

    # Java 命令
    command = ["java", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "-jar", "vape-loader.jar"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # 输出获取和处理
    for line in process.stdout:
        print(line.strip())  # 打印到控制台
        check_for_616(line.strip())

# 检查输出并写入 settings.txt
def check_for_616(output):
    # 检查是否包含 "616:"，并且不含特殊字符
    match = re.search(r'616:\s*([A-Za-z0-9=]*)', output)
    if match:
        # 获取 "616:" 后面的内容
        settings_content = match.group(1).strip()
        # 写入 settings.txt 文件
        with open("settings.txt", "w", encoding="utf-8") as f:
            f.write(settings_content)
        print("已将内容写入 settings.txt:", settings_content)
        filter_content()  # 再次调用过滤函数处理文件内容

# 按钮点击事件
def on_inject_button_click():
    run_java_command()

# 创建 GUI 界面
root = tk.Tk()
root.title("Vape 启动器")

inject_button = tk.Button(root, text="注入", command=on_inject_button_click)
inject_button.pack(pady=20)

root.mainloop()
