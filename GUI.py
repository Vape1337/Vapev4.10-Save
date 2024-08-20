import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
import subprocess
import sys

# 判断当前运行的文件路径
if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
window_width = 694
window_height = 417

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#1a1a1a")
root.overrideredirect(True)

def place_image(path, x, y, anchor):
    image = Image.open(os.path.join(script_dir, path))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, bg="#1a1a1a")
    label.image = photo
    label.place(x=x, y=y, anchor=anchor)
    return label

background_label = place_image("assets/mask_l_1.png", 0, 0, anchor="nw")
place_image("assets/mask_r_1.png", window_width, window_height, anchor="se")

# 缩小比例
scale = 0.6

def load_image(path, scale):
    image = Image.open(os.path.join(script_dir, path))
    width, height = image.size
    resized_image = image.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    enhancer = ImageEnhance.Brightness(resized_image)
    hover_image = enhancer.enhance(1.5)  # 提高伽马值
    hover_photo = ImageTk.PhotoImage(hover_image)
    return photo, hover_photo

def on_click(bat_path):
    full_path = os.path.join(script_dir, bat_path)
    print(f"Attempting to run: {full_path}")  # 打印尝试运行的路径
    try:
        subprocess.Popen(f'"{full_path}"', shell=True)
        print(f"Successfully started: {full_path}")  # 打印成功启动信息
    except Exception as e:
        print(f"Failed to start {full_path}: {e}")  # 打印错误信息

# 按钮路径与执行的程序映射
buttons_info = [
    ("assets/4.04.png", "VapeV4.04/run.bat"),
    ("assets/4.09.png", "VapeV4.09/run.bat"),
    ("assets/4.10.png", "VapeV4.10/run.bat"),
    ("assets/4.11.png", "VapeV4.11/run.bat"),
    ("assets/lite.png", "VapeLite/run.bat")
]

button_x_position = 20
button_spacing = 60  # 调整间距

# 最下方按钮的位置
bottom_button_y_position = window_height - 100

# 从下往上排列按钮
for i, (img_path, bat_path) in enumerate(reversed(buttons_info)):
    photo, hover_photo = load_image(img_path, scale)
    button = tk.Button(root, image=photo, bg="#1a1a1a", bd=0, activebackground="#1a1a1a",
                       command=lambda path=bat_path: on_click(path))
    button.image = photo
    button.bind("<Enter>", lambda event, hp=hover_photo: event.widget.config(image=hp))
    button.bind("<Leave>", lambda event, p=photo: event.widget.config(image=p))
    button.place(x=button_x_position, y=bottom_button_y_position - i * button_spacing, anchor="nw")

# 关闭按钮设置
close_button_path = "assets/off.png"
off_image_path = os.path.join(script_dir, close_button_path)
off_image = Image.open(off_image_path)
off_photo = ImageTk.PhotoImage(off_image)
enhancer = ImageEnhance.Brightness(off_image)
off_hover_image = enhancer.enhance(1.5)
off_hover_photo = ImageTk.PhotoImage(off_hover_image)

def on_enter(event):
    close_button.config(image=off_hover_photo)

def on_leave(event):
    close_button.config(image=off_photo)

close_button = tk.Button(root, image=off_photo, bg="#1a1a1a", bd=0, activebackground="#1a1a1a", command=root.destroy)
close_button.image = off_photo

button_x_offset = 20
button_y_offset = 20
close_button.place(x=window_width - button_x_offset, y=button_y_offset, anchor="ne")
close_button.lift()

# 窗口拖动功能
def start_move(event):
    root._drag_data = {'x': event.x_root - root.winfo_rootx(), 'y': event.y_root - root.winfo_rooty()}

def do_move(event):
    x = event.x_root - root._drag_data['x']
    y = event.y_root - root._drag_data['y']
    root.geometry(f'+{x}+{y}')

root.bind('<ButtonPress-1>', start_move)
root.bind('<B1-Motion>', do_move)

root.mainloop()
