import tkinter as tk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk
import time

# 更新 GUI 背景和进度条
class ProgressBar:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bar = canvas.create_rectangle(x, y, x, y + height, fill='green', outline='green')
        self.update_progress(0)

    def update_progress(self, progress):
        # 更新进度条长度
        self.canvas.coords(self.bar, self.x, self.y, self.x + progress * self.width, self.y + self.height)

def update_gui_progress(canvas, progress_bar):
    progress = (time.time() - start_time) / 10  # 10秒完成
    if progress > 1:
        progress = 1
    progress_bar.update_progress(progress * canvas.winfo_width())
    if progress < 1:
        canvas.after(50, update_gui_progress, canvas, progress_bar)
    
def create_gui():
    root = tk.Tk()
    root.title("Vape 启动器")
    root.geometry("530x324")
    root.configure(bg='#202020')  # 设置背景颜色为 rgb(32,32,32)

    canvas = Canvas(root, width=530, height=324, bg='#202020', bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 加载并显示背景图
    bg1 = Image.open('newassets/mask_l_1.png')
    bg1 = bg1.resize((265, 324))  # 确保图像适配窗口
    bg1 = ImageTk.PhotoImage(bg1)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg1)

    bg2 = Image.open('newassets/mask_r_1.png')
    bg2 = bg2.resize((265, 324))  # 确保图像适配窗口
    bg2 = ImageTk.PhotoImage(bg2)
    canvas.create_image(265, 0, anchor=tk.NW, image=bg2)

    # 加载并显示中间图像
    logo = Image.open('newassets/load-logo.png')
    logo = logo.resize((200, 200))  # 调整 logo 大小
    logo = ImageTk.PhotoImage(logo)
    canvas.create_image(265, 162, anchor=tk.CENTER, image=logo)

    # 创建进度条
    progress_bar = ProgressBar(canvas, 20, 290, 490, 20)
    
    # 开始更新进度条
    global start_time
    start_time = time.time()
    update_gui_progress(canvas, progress_bar)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
