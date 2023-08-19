import time
from tkinter import Tk
import cv2
import pyautogui
import os
import subprocess
import win32com.client
import numpy as np
from PIL import ImageGrab

# 创建白屏窗口
root = Tk()
# 隐藏外部窗口
root.overrideredirect(True)
# 设置为全屏
root.state('zoomed')
# 置顶
root.attributes("-topmost", 1)

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 获取快捷方式路径
shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'

# 解析快捷方式获取安装路径
shell = win32com.client.Dispatch("WScript.Shell")
install_dir = shell.CreateShortCut(shortcut)
install_dir = install_dir.TargetPath.replace('launcher.exe', '')
# 拼接游戏exe路径
game_exe = os.path.join(install_dir, 'Genshin Impact Game', 'YuanShen.exe')
# print(game_exe)

def main(game_path):
    try:
        # 将游戏置顶启动
        subprocess.Popen(game_path)
        # 检查原神是否已经启动
        # >nul 屏蔽执行后的输出,但是错误不会   2>nul  不管命令是否正确,都屏蔽输出
        while 1:
            if os.system('tasklist /FI "IMAGENAME eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0:
                time.sleep(6)
                # 枚举窗口,找到名称包含"原神"的窗口
                window = pyautogui.getWindowsWithTitle("原神")[0]
                # 将目标窗口置顶
                pyautogui.moveTo(window.left, window.top)
                # 关闭白屏窗口
                root.destroy()

                print("原神 启动!")
                break

    except:
        root.destroy()
        print("未获取到原神安装路径!或权限不够!")


while True:

    # 截图
    print("正在检测屏幕...")
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)
    # 计算屏幕白色像素比例
    white_pixels = np.count_nonzero(screenshot == [255, 255, 255])
    total_pixels = screenshot.shape[0] * screenshot.shape[1]
    white_percentage = white_pixels / total_pixels * 100

    # 判断是否满足启动条件
    if white_percentage >= 94:
        # 先显示白屏
        root.update()
        # 启动原神
        main(game_exe)
        break
