import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # 用于调整关闭按钮的位置

# 初始化窗口
root = tk.Tk()
root.geometry("444x324")
root.configure(bg="#202020")

# 移除窗口边框
root.overrideredirect(True)

# 设置图片的函数
def place_image(path, x, y, anchor):
    image = Image.open(path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, bg="#202020")
    label.image = photo  # 防止图片被垃圾回收
    label.place(x=x, y=y, anchor=anchor)

# 将图片放置在左下角和右下角
place_image("newassets/mask_l_1.png", 0, 324, anchor="sw")
place_image("newassets/mask_r_1.png", 444, 324, anchor="se")

# 设置右上角的关闭按钮
off_image = Image.open("newassets/off.png")
off_photo = ImageTk.PhotoImage(off_image)
close_button = tk.Button(root, image=off_photo, bg="#202020", bd=0, command=root.quit)
close_button.image = off_photo
# 关闭按钮偏移
close_button.place(x=444 - 20*10, y=0 + 20*10, anchor="ne")

# 使窗口可拖动
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

root.bind('<B1-Motion>', move_window)

root.mainloop()
