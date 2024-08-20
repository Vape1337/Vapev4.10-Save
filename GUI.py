import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import webbrowser
import os
import sys
import subprocess

def create_rounded_rectangle_image(width, height, radius, color):
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return image

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
root.overrideredirect(True)

bg_image = create_rounded_rectangle_image(window_width, window_height, 20, "#1a1a1a")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo, bg="#1a1a1a")
bg_label.place(x=0, y=0)

root.iconbitmap(default=os.path.join(script_dir, "assets/icon.ico"))

def place_image(path, x, y, anchor):
    image = Image.open(os.path.join(script_dir, path)).convert('RGBA')
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, bg="#1a1a1a")
    label.image = photo
    label.place(x=x, y=y, anchor=anchor)
    return label

background_label = place_image("assets/mask_l_1.png", 0, 0, anchor="nw")
place_image("assets/mask_r_1.png", window_width, window_height, anchor="se")

def load_image(path, scale):
    image = Image.open(os.path.join(script_dir, path)).convert('RGBA')
    width, height = image.size
    resized_image = image.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
    
    enhancer = ImageEnhance.Brightness(resized_image)
    hover_image = enhancer.enhance(1.5)
    
    photo = ImageTk.PhotoImage(resized_image)
    hover_photo = ImageTk.PhotoImage(hover_image)
    return photo, hover_photo

clicked_any_button = False

def on_click(bat_path):
    global clicked_any_button
    if not clicked_any_button:
        full_path = os.path.join(script_dir, bat_path)
        
        try:
            subprocess.Popen(f'"{full_path}"', shell=True)
            clicked_any_button = True
        except Exception as e:
            print(f"Failed to start {full_path}: {e}")
    else:
        messagebox.showwarning("警告", "请不要多次点击！")

close_button_path = "assets/off.png"
off_image_path = os.path.join(script_dir, close_button_path)
off_image = Image.open(off_image_path).convert('RGBA')
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

def start_move(event):
    root._drag_data = {'x': event.x_root - root.winfo_rootx(), 'y': event.y_root - root.winfo_rooty()}

def do_move(event):
    x = event.x_root - root._drag_data['x']
    y = event.y_root - root._drag_data['y']
    root.geometry(f'+{x}+{y}')

root.bind('<ButtonPress-1>', start_move)
root.bind('<B1-Motion>', do_move)

def create_button(button_image, bat_path, y_position):
    button_photo, button_hover = load_image(button_image, 0.8)
    button = tk.Button(root, image=button_photo, bg="#1a1a1a", bd=0, activebackground="#1a1a1a")
    button.image = button_photo
    button.place(x=50, y=y_position, anchor="nw")

    button.config(command=lambda: on_click(bat_path))

buttons_info = [
    ("assets/4.04.png", "VapeV4.04/run.bat"),
    ("assets/4.09.png", "VapeV4.09/run.bat"),
    ("assets/4.10.png", "VapeV4.10/run.bat"),
    ("assets/4.11.png", "VapeV4.11/run.bat"),
    ("assets/lite.png", "VapeLite/run.bat")
]

button_y = 50
for button_image, bat_path in buttons_info:
    create_button(button_image, bat_path, button_y)
    button_y += 60

def animate_image():
    logo1_image = Image.open(os.path.join(script_dir, "assets/logo1.png")).resize((117, 35), Image.LANCZOS).convert('RGBA')
    logo1_photo = ImageTk.PhotoImage(logo1_image)
    
    logo_image = Image.open(os.path.join(script_dir, "assets/logo.png")).resize((123, 22), Image.LANCZOS).convert('RGBA')
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    logo_x = window_width * 0.5
    logo_y = window_height // 2

    logo_label = tk.Label(root, image=logo_photo, bg="#1a1a1a")
    logo_label.image = logo_photo
    logo_label.place(x=logo_x, y=logo_y, anchor="center")
    
    logo1_label = tk.Label(root, image=logo1_photo, bg="#1a1a1a")
    logo1_label.image = logo1_photo
    logo1_label.place(x=logo_x, y=logo_y, anchor="center")

    for i in range(13):
        new_x = logo_x + i * 10
        logo1_label.place_configure(x=new_x)
        root.update_idletasks()
        root.after(3)

    logo1_label.lift()

root.after(500, animate_image)


# 图标悬停变色和点击事件
def on_enter_icon(event, hover_photo):
    event.widget.config(image=hover_photo)
    event.widget.image = hover_photo

def on_leave_icon(event, photo):
    event.widget.config(image=photo)
    event.widget.image = photo

def open_link(url):
    webbrowser.open(url)

# 添加中间下部的图标和点击事件
def create_icon(path, hover_path, x, y, url):
    photo, hover_photo = load_image(path, 0.5)
    icon_label = tk.Label(root, image=photo, bg="#1a1a1a", cursor="hand2")
    icon_label.image = photo
    icon_label.place(x=x, y=y, anchor="center")
    icon_label.bind("<Button-1>", lambda e: open_link(url))
    icon_label.bind("<Enter>", lambda e: on_enter_icon(e, hover_photo))
    icon_label.bind("<Leave>", lambda e: on_leave_icon(e, photo))

# 更新后的icon_info
icon_info = [
    ("assets/bilibili.png", "assets/bilibili.png", window_width // 2 - 40, window_height - 30, "https://space.bilibili.com/486637407"),
    ("assets/github.png", "assets/github.png", window_width // 2 + 40, window_height - 30, "https://github.com/Vape1337/Vapev4.10-Save"),
]

for icon in icon_info:
    create_icon(*icon)

root.mainloop()
