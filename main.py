import os
import subprocess
import time

import cv2
import numpy as np
import pyautogui
import win32com.client
import win32con
import win32gui
from PIL import ImageGrab

while True:
    # 检查原神是否已经启动
    if os.system('tasklist /FI "IMAGENAME eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0:
        print("原神 已在运行!")
        break

    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 截图
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)

    # 计算屏幕白色像素比例
    white_pixels = np.count_nonzero(screenshot >= [250, 250, 250])
    total_pixels = screenshot.shape[0] * screenshot.shape[1]
    white_percentage = white_pixels / total_pixels * 100
    print(f"屏幕含原量{white_percentage}%")

    # 判断是否满足启动条件
    if white_percentage >= 90:
        try:
            # 获取快捷方式路径
            shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'

            # 解析快捷方式获取安装路径
            shell = win32com.client.Dispatch("WScript.Shell")
            install_dir = shell.CreateShortCut(shortcut)
            install_dir = install_dir.TargetPath.replace('launcher.exe', '')

            # 拼接游戏exe路径
            game_exe = os.path.join(install_dir, 'Genshin Impact Game', 'YuanShen.exe')

            # 创建过渡用的白色图片
            transition_steps = 35
            white_image = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)

            # 创建过渡窗口并置顶
            cv2.namedWindow('Transition', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Transition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            transition_window = pyautogui.getWindowsWithTitle("Transition")[0]
            pyautogui.moveTo(transition_window.left, transition_window.top)
            cv2.imshow('Transition', screenshot)
            hwnd = win32gui.FindWindow(None, "Transition")
            CVRECT = cv2.getWindowImageRect("Transition")
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height,
                                  win32con.SWP_SHOWWINDOW)

            # 原神，启动！
            subprocess.Popen(game_exe)

            # 进行过渡并在过渡窗口上显示
            for step in range(transition_steps):
                alpha = (step + 1) / transition_steps
                blended_image = cv2.addWeighted(screenshot, 1 - alpha, white_image, alpha, 0)
                cv2.imshow('Transition', blended_image)
                cv2.waitKey(10)

            # 枚举窗口,找到名称包含"原神"的窗口
            while True:
                windows = pyautogui.getWindowsWithTitle("原神")
                if windows:
                    # 将过渡窗口置于非最高层
                    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, screen_width, screen_height,
                                          win32con.SWP_SHOWWINDOW)

                    # 将原神置于最高层
                    hwnd = win32gui.FindWindow(None, "原神")
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height,
                                          win32con.SWP_SHOWWINDOW)
                    genshin_window = windows[0]
                    pyautogui.moveTo(genshin_window.left, genshin_window.top)
                    pyautogui.click(genshin_window.left, genshin_window.top)
                    print("原神 启动!")

                    # 过渡完毕，偷偷删除过渡窗口
                    time.sleep(5)
                    cv2.destroyAllWindows()
                    break

                time.sleep(1)
            break

        except:
            print("未获取到原神安装路径!或权限不够!")
            break
