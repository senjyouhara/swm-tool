import win32api, win32con, win32gui, win32com, win32process
import psutil

import config


def __get_window_handles(pid, pidName):
    def callback(hwnd, all_windows):
        _,PID = win32process.GetWindowThreadProcessId(hwnd)
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and PID == pid and win32gui.IsWindowVisible(hwnd):
            txt = win32gui.GetWindowText(hwnd)
            if txt != "":
                all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    all_windows = []
    win32gui.EnumWindows(callback, all_windows)

    return all_windows

def get_window_pwd(processName: str):

    print(f"正在查找该进程： {processName}")

    processes = psutil.process_iter()
    process = None
    for process in processes:
        # print(f"Process ID: {process.pid}, Name: {process.name()}")
        if process.name() == processName and process.parent() == None:
            process = process
            break

    if process is None:
        print("未找到对应的进程！")
    else:
        print(f"进程已找到！")
        windows = __get_window_handles(process.pid, process.exe())
        if len(windows) > 0:
            for hwnd, title in windows:
                print(f'Window Title: "{title}"')
                # 获取窗口句柄
                if hwnd == 0:
                    return (), None
                else:
                    # 返回坐标值和handle
                    return win32gui.GetWindowRect(hwnd), hwnd

    return (), None


def is_window_active(hwnd):
    # 获取窗口的可见状态（1表示可见）
    visible = win32gui.IsWindowVisible(hwnd)

    # 判断窗口是否有焦点（1表示有焦点）
    focused = win32gui.GetForegroundWindow() == hwnd

    return visible and focused


def get_window_position(processName: str):
    _, handle = get_window_pwd(processName)
    if handle != None:

        if is_window_active(handle):
            return _, handle

        win32gui.ShowWindow(handle, win32con.SW_SHOWMAXIMIZED)
        # win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        # 设为高亮
        win32gui.SetForegroundWindow(handle)
        #最小化
        if _[0] < -1000:
            # 最小化时是获取不到窗口坐标的，需要重新获取一次
            position = win32gui.GetWindowRect(handle)
            return position, handle

    return (), None
