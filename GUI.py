import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
import subprocess

# 获取当前脚本的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 初始化窗口
root = tk.Tk()
window_width = 694
window_height = 417

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口居中时左上角的坐标
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口大小并居中
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#1a1a1a")

# 移除窗口边框
root.overrideredirect(True)

# 设置图片的函数
def place_image(path, x, y, anchor):
    image = Image.open(path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, bg="#1a1a1a")
    label.image = photo
    label.place(x=x, y=y, anchor=anchor)
    return label

# 将背景图片放置在窗口的最左上角
background_label = place_image(os.path.join(script_dir, "newassets/mask_l_1.png"), 0, 0, anchor="nw")

# 将另一张图片放置在右下角
place_image(os.path.join(script_dir, "newassets/mask_r_1.png"), window_width, window_height, anchor="se")

# 设置关闭按钮，并偏移2cm
off_image_path = os.path.join(script_dir, "newassets/off.png")

# 加载常规图像
off_image = Image.open(off_image_path)
off_photo = ImageTk.PhotoImage(off_image)

# 创建亮度增强图像
enhancer = ImageEnhance.Brightness(off_image)
off_hover_image = enhancer.enhance(1.5)  # 增加亮度
off_hover_photo = ImageTk.PhotoImage(off_hover_image)

# 设置关闭按钮高亮效果
def on_enter(event):
    close_button.config(image=off_hover_photo)  # 更换为高亮图片

def on_leave(event):
    close_button.config(image=off_photo)  # 恢复原始图片

# 创建关闭按钮
close_button = tk.Button(root, image=off_photo, bg="#1a1a1a", bd=0, activebackground="#1a1a1a", command=root.destroy)
close_button.image = off_photo

# 绑定鼠标进入和离开事件来实现高亮效果
close_button.bind("<Enter>", on_enter)
close_button.bind("<Leave>", on_leave)

# 关闭按钮位置向左偏2cm（20px），向下偏2cm（20px）
button_x_offset = 20  # 偏移量
button_y_offset = 20  # 偏移量
close_button.place(x=window_width - button_x_offset, y=button_y_offset, anchor="ne")

# 将关闭按钮置于最顶层，以确保不会被其他元素遮挡
close_button.lift()

# 允许在窗口的任意区域拖动窗口
def start_move(event):
    root._drag_data = {'x': event.x_root - root.winfo_rootx(), 'y': event.y_root - root.winfo_rooty()}

def do_move(event):
    x = event.x_root - root._drag_data['x']
    y = event.y_root - root._drag_data['y']
    root.geometry(f'+{x}+{y}')

# 绑定拖动事件到整个窗口
root.bind('<ButtonPress-1>', start_move)
root.bind('<B1-Motion>', do_move)

# 定义按钮点击事件
def run_vape(version):
    exe_path = os.path.join(script_dir, f"Vape{version}/norename.exe")
    subprocess.run(exe_path)

# 添加左侧按钮
button_names = ["点击注入VapeV4.04", "点击注入VapeV4.09", "点击注入VapeV4.10", "点击注入VapeV4.11", "点击注入VapeLite"]
versions = ["V4.04", "V4.09", "V4.10", "V4.11", "Lite"]

for i, (name, version) in enumerate(zip(button_names, versions)):
    button = tk.Button(root, text=name, command=lambda v=version: run_vape(v), bg="#333333", fg="#FFFFFF", bd=0, activebackground="#444444", activeforeground="#FFFFFF")
    button.place(x=20, y=40 + i*40, anchor="nw", width=160, height=30)

root.mainloop()
