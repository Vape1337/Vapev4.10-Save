import os
import subprocess
from datetime import datetime

def disable_auto_time_sync():
    try:
        # 禁用Windows自动时间同步
        subprocess.run(["w32tm", "/config", "/manualpeerlist:", "/syncfromflags:manual", "/reliable:NO", "/update"], check=True)
        subprocess.run(["net", "stop", "w32time"], check=True)
        print("已关闭自动时间同步")
    except Exception as e:
        print(f"关闭自动时间同步失败: {e}")

def enable_auto_time_sync():
    try:
        # 启用Windows自动时间同步
        subprocess.run(["net", "start", "w32time"], check=True)
        subprocess.run(["w32tm", "/resync"], check=True)
        print("已启用自动时间同步")
    except Exception as e:
        print(f"启用自动时间同步失败: {e}")

def set_system_time(date_str):
    try:
        # 设置系统时间，针对Windows系统
        os.system(f'date {date_str}')
        print(f"系统时间已设置为: {date_str}")
    except Exception as e:
        print(f"设置系统时间失败: {e}")

def restore_system_time():
    try:
        # 恢复到当前的系统时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.system(f'date {current_time.split()[0]}')
        os.system(f'time {current_time.split()[1]}')
        print(f"系统时间已恢复为: {current_time}")
    except Exception as e:
        print(f"恢复系统时间失败: {e}")

if __name__ == "__main__":
    # 禁用自动时间同步
    disable_auto_time_sync()

    # 设置时间为2012年2月1日
    set_system_time('02-01-2012')

    while True:
        user_input = input("输入1恢复正常时间并重新开启自动同步，输入其他任意键退出: ")
        if user_input == "1":
            restore_system_time()
            enable_auto_time_sync()  # 恢复时间后启用自动时间同步
            break
        else:
            break
