import ctypes
from ctypes import wintypes
import ctypes.wintypes

def set_dpi_aware():
    """设置DPI感知模式"""
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
        return "DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2"
    except:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            return "PROCESS_PER_MONITOR_DPI_AWARE"
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                return "SetProcessDPIAware"
            except:
                return "DPI感知设置失败"

def check_current_dpi_awareness():
    try:
        context = ctypes.windll.user32.GetProcessDpiAwarenessContext()
        print(f"当前进程DPI感知上下文: {context}")
    except:
        pass

# 设置DPI感知
dpi_mode = set_dpi_aware()
# print(f"DPI感知模式: {dpi_mode}")

check_current_dpi_awareness()

def get_monitors_ctypes():
    """使用纯ctypes获取显示器信息"""
    user32 = ctypes.windll.user32
    shcore = ctypes.windll.shcore
    
    monitors = []
    
    # 定义结构体
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long)
        ]
    
    class MONITORINFOEX(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", RECT),
            ("rcWork", RECT),
            ("dwFlags", wintypes.DWORD),
            ("szDevice", wintypes.WCHAR * 32)
        ]
    
    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        try:
            # 获取显示器信息
            monitor_info = MONITORINFOEX()
            monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
            
            result = user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info))
            if not result:
                print(f"GetMonitorInfoW 失败")
                return True
            
            # 获取DPI信息
            dpi_x = ctypes.c_uint()
            dpi_y = ctypes.c_uint()
            
            try:
                result = shcore.GetDpiForMonitor(
                    hMonitor, 
                    0,  # MDT_EFFECTIVE_DPI
                    ctypes.byref(dpi_x), 
                    ctypes.byref(dpi_y)
                )
                if result != 0:  # S_OK = 0
                    # 回退到系统DPI
                    dpi_x.value = 96
                    dpi_y.value = 96
            except:
                dpi_x.value = 96
                dpi_y.value = 96
            
            # 获取显示设置（物理分辨率）
            device_name = monitor_info.szDevice
            
            class DEVMODE(ctypes.Structure):
                _fields_ = [
                    ("dmDeviceName", wintypes.WCHAR * 32),
                    ("dmSpecVersion", wintypes.WORD),
                    ("dmDriverVersion", wintypes.WORD),
                    ("dmSize", wintypes.WORD),
                    ("dmDriverExtra", wintypes.WORD),
                    ("dmFields", wintypes.DWORD),
                    ("dmOrientation", ctypes.c_short),
                    ("dmPaperSize", ctypes.c_short),
                    ("dmPaperLength", ctypes.c_short),
                    ("dmPaperWidth", ctypes.c_short),
                    ("dmScale", ctypes.c_short),
                    ("dmCopies", ctypes.c_short),
                    ("dmDefaultSource", ctypes.c_short),
                    ("dmPrintQuality", ctypes.c_short),
                    ("dmColor", ctypes.c_short),
                    ("dmDuplex", ctypes.c_short),
                    ("dmYResolution", ctypes.c_short),
                    ("dmTTOption", ctypes.c_short),
                    ("dmCollate", ctypes.c_short),
                    ("dmFormName", wintypes.WCHAR * 32),
                    ("dmLogPixels", wintypes.WORD),
                    ("dmBitsPerPel", wintypes.DWORD),
                    ("dmPelsWidth", wintypes.DWORD),
                    ("dmPelsHeight", wintypes.DWORD),
                    ("dmDisplayFlags", wintypes.DWORD),
                    ("dmDisplayFrequency", wintypes.DWORD),
                ]
            
            # 获取物理分辨率
            devmode = DEVMODE()
            devmode.dmSize = ctypes.sizeof(DEVMODE)
            
            physical_width = physical_height = 0
            try:
                result = user32.EnumDisplaySettingsW(device_name, -1, ctypes.byref(devmode))  # ENUM_CURRENT_SETTINGS = -1
                if result:
                    physical_width = devmode.dmPelsWidth
                    physical_height = devmode.dmPelsHeight
            except:
                pass
            
            # 如果无法获取物理分辨率，使用逻辑尺寸计算
            if physical_width == 0 or physical_height == 0:
                scale_x = dpi_x.value / 96.0
                scale_y = dpi_y.value / 96.0
                logical_width = monitor_info.rcMonitor.right - monitor_info.rcMonitor.left
                logical_height = monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top
                physical_width = int(logical_width * scale_x)
                physical_height = int(logical_height * scale_y)
            
            monitor_data = {
                'device_name': device_name,
                'is_primary': (monitor_info.dwFlags & 1) != 0,  # MONITORINFOF_PRIMARY = 1
                'logical_position': {
                    'x': monitor_info.rcMonitor.left,
                    'y': monitor_info.rcMonitor.top
                },
                'logical_size': {
                    'width': monitor_info.rcMonitor.right - monitor_info.rcMonitor.left,
                    'height': monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top
                },
                'physical_size': {
                    'width': physical_width,
                    'height': physical_height
                },
                'work_area': {
                    'x': monitor_info.rcWork.left,
                    'y': monitor_info.rcWork.top,
                    'width': monitor_info.rcWork.right - monitor_info.rcWork.left,
                    'height': monitor_info.rcWork.bottom - monitor_info.rcWork.top
                },
                'dpi': {
                    'x': dpi_x.value,
                    'y': dpi_y.value
                },
                'scale_factor': {
                    'x': dpi_x.value / 96.0,
                    'y': dpi_y.value / 96.0
                },
                'scale_percentage': f"{dpi_x.value / 96.0 * 100:.0f}%"
            }
            
            monitors.append(monitor_data)
            
        except Exception as e:
            print(f"处理显示器时出错: {e}")
            import traceback
            traceback.print_exc()
        
        return True  # 继续枚举
    
    # 定义回调函数类型
    MonitorEnumProc = ctypes.WINFUNCTYPE(
        wintypes.BOOL,          # 返回值类型
        wintypes.HMONITOR,      # hMonitor
        wintypes.HDC,           # hdcMonitor  
        ctypes.POINTER(RECT),   # lprcMonitor
        wintypes.LPARAM         # dwData
    )
    
    # 枚举显示器
    try:
        result = user32.EnumDisplayMonitors(
            None,                           # hdc
            None,                           # lprcClip
            MonitorEnumProc(monitor_enum_proc),  # lpfnEnum
            0                               # dwData
        )
        if not result:
            print("EnumDisplayMonitors 失败")
    except Exception as e:
        print(f"调用 EnumDisplayMonitors 时出错: {e}")
        import traceback
        traceback.print_exc()
    
    return monitors

def check_system_info():
    """检查系统信息"""
    try:
        # 检查系统DPI
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        
        hdc = user32.GetDC(0)
        if hdc:
            dpi_x = gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            dpi_y = gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
            user32.ReleaseDC(0, hdc)
            print(f"系统 DPI: {dpi_x}x{dpi_y}")
            print(f"系统缩放: {dpi_x/96*100:.0f}%")
        
        # 检查虚拟屏幕大小
        virtual_width = user32.GetSystemMetrics(78)    # SM_CXVIRTUALSCREEN
        virtual_height = user32.GetSystemMetrics(79)   # SM_CYVIRTUALSCREEN
        virtual_left = user32.GetSystemMetrics(76)     # SM_XVIRTUALSCREEN  
        virtual_top = user32.GetSystemMetrics(77)      # SM_YVIRTUALSCREEN
        
        print(f"虚拟屏幕: {virtual_width}x{virtual_height} at ({virtual_left}, {virtual_top})")
        
        # 检查显示器数量
        monitor_count = user32.GetSystemMetrics(80)    # SM_CMONITORS
        print(f"显示器数量: {monitor_count}")
        
    except Exception as e:
        print(f"获取系统信息时出错: {e}")

monitors = get_monitors_ctypes()

def print_info():
    print("=== 系统信息 ===")
    check_system_info()
    print()
    
    print("=== 显示器信息 ===")
    
    if not monitors:
        print("未能获取显示器信息")
        return
    
    for i, monitor in enumerate(monitors):
        print(f"显示器 {i+1}:")
        print(f"  设备名: {monitor['device_name']}")
        print(f"  主显示器: {'是' if monitor['is_primary'] else '否'}")
        print(f"  逻辑位置: ({monitor['logical_position']['x']}, {monitor['logical_position']['y']})")
        print(f"  逻辑大小: {monitor['logical_size']['width']} x {monitor['logical_size']['height']}")
        print(f"  物理大小: {monitor['physical_size']['width']} x {monitor['physical_size']['height']}")
        print(f"  工作区域: {monitor['work_area']['width']} x {monitor['work_area']['height']} at ({monitor['work_area']['x']}, {monitor['work_area']['y']})")
        print(f"  DPI: {monitor['dpi']['x']} x {monitor['dpi']['y']}")
        print(f"  缩放比例: {monitor['scale_factor']['x']:.2f} x {monitor['scale_factor']['y']:.2f}")
        print(f"  缩放百分比: {monitor['scale_percentage']}")
        print()

import os
import cv2
import tqdm
import math
import time
import random
import keyboard
import pyautogui
import subprocess
import numpy as np
from PIL import Image, ImageGrab, ImageDraw

from Locator import ColorLocator

def get_img_from_clipboard():
    clipboard_content = ImageGrab.grabclipboard()
    if clipboard_content is None:
        print("错误：剪贴板中没有内容或不是图片格式")
        return None
    if not isinstance(clipboard_content, Image.Image):
        print("错误：剪贴板中的内容不是图片")
        return None
    
    return clipboard_content

def greedy_sort_cells(cells):
    """
    贪心排序函数：保持第一个元素不变，从第二个元素开始按距离排序
    
    Args:
        cells: 单元格列表，每个元素包含 'center' 字段 (cx, cy)
    
    Returns:
        排序后的单元格列表
    """
    if len(cells) <= 1:
        return cells
    
    # 复制原列表，避免修改原数据
    sorted_cells = [cells[0]]  # 保持第一个元素不变
    remaining_cells = cells[1:].copy()  # 剩余待排序的元素
    
    current_center = cells[0]['center']
    
    while remaining_cells:
        # 计算当前位置到所有剩余元素的距离
        min_distance = float('inf')
        closest_idx = 0
        
        for i, cell in enumerate(remaining_cells):
            # 计算欧几里得距离
            dx = cell['center'][0] - current_center[0]
            dy = cell['center'][1] - current_center[1]
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
        
        # 将最近的元素添加到结果中
        closest_cell = remaining_cells.pop(closest_idx)
        sorted_cells.append(closest_cell)
        current_center = closest_cell['center']
    
    return sorted_cells


should_exit = False
loc = ColorLocator()

def opt_func_1():
    img = get_img_from_clipboard()
    if img is None: return
    try: dimming = max(0, int(input("Dimming (default 20): ")))
    except: dimming = 20
    loc.set_dimming(dimming)
    ret = loc.filter_cell_img(img, 0 if dimming == 0 else 2)
    if ret:
        print(f"位置: {ret['loc']}\n面积: {ret['area']}\n颜色: {ret['color']}")
    else:
        print("获取失败")
        
def opt_func_2():
    # img = ImageGrab.grabclipboard()
    img_raw = ImageGrab.grab(all_screens=True)
    mx, my = 0, 0
    ox, oy = 0, 0
    if len(monitors) != 1:
        for i, m in enumerate(monitors):
            print(f"{i+1}. {m['device_name']}: Coord ({m['logical_position']['x']}, {m['logical_position']['y']}) | Size {m['physical_size']['width']}x{m['physical_size']['height']} | Primary {m['is_primary']}")
            mx, my = m['logical_position']['x'], m['logical_position']['y']
            mw, mh = m['physical_size']['width'], m['physical_size']['height']
            ox = min(ox, mx)
            oy = min(oy, my)
        try: 
            idx_m = int(input("输入显示器编号: ")) - 1
            m = monitors[idx_m]
            mx, my = m['logical_position']['x'], m['logical_position']['y']
            mw, mh = m['physical_size']['width'], m['physical_size']['height']
            img = img_raw.crop((mx-ox, my-oy, mx-ox+mw, my-oy+mh))
        except Exception as e: 
            print((mx-ox, my-oy, mx-ox+mw, my-oy+mh))
            print(e)
            return
    
    if img is None or not isinstance(img, Image.Image):
        return
    if loc.cell_data is None:
        return
    draw = ImageDraw.Draw(img)
    ret  = loc.locate_cells(img, single_color=True, tol=2 if loc.dimming else 0)
    if ret is None: 
        print("未找到单元格")
        cv2.namedWindow('Image Filter', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('Image Filter', np.array(img.convert("RGB"))[:, :, ::-1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return
    
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    for cell in ret['cells'][ret['color_index'][0]]:
        x, y, w, h = cell['rect']
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x+w)
        max_y = max(max_y, y+h)
        draw.rectangle((x, y, x+w, y+h), outline='red', width=2)
        draw.rectangle((x-2, y-2, x+w+2, y+h+2), outline='green', width=2)
    
    margin = 3 * max(w, h)
    crop_box = (
        max(0, min_x - margin),
        max(0, min_y - margin),
        min(img.size[0], max_x + margin),
        min(img.size[1], max_y + margin)
    )
    cropped_img = img.crop(crop_box)
    
    cv2.namedWindow('Image Filter', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Image Filter', np.array(cropped_img.convert("RGB"))[:, :, ::-1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def opt_func_3():
    global should_exit
    img_raw = ImageGrab.grab(all_screens=True)
    mx, my = 0, 0
    ox, oy = 0, 0
    if len(monitors) != 1:
        for i, m in enumerate(monitors):
            print(f"{i+1}. {m['device_name']}: Coord ({m['logical_position']['x']}, {m['logical_position']['y']}) | Size {m['physical_size']['width']}x{m['physical_size']['height']} | Primary {m['is_primary']}")
            mx, my = m['logical_position']['x'], m['logical_position']['y']
            mw, mh = m['physical_size']['width'], m['physical_size']['height']
            ox = min(ox, mx)
            oy = min(oy, my)
        try: 
            idx_m = int(input("输入显示器编号: ")) - 1
            m = monitors[idx_m]
            mx, my = m['logical_position']['x'], m['logical_position']['y']
            mw, mh = m['physical_size']['width'], m['physical_size']['height']
            print(mx, my, mw, mh)
            print((mx-ox, my-oy, mx-ox+mw, my-oy+mh))
            img = img_raw.crop((mx-ox, my-oy, mx-ox+mw, my-oy+mh))
        except Exception as e: 
            print((mx-ox, my-oy, mx-ox+mw, my-oy+mh))
            print(e)
            return
        
    if img is None or not isinstance(img, Image.Image):
        return
    if loc.cell_data is None:
        return
    
    ret = loc.locate_cells(img, single_color=True, tol=2 if loc.dimming else 0)
    if ret is None: 
        print("未找到单元格")
        return
    
    cells = ret['cells'][ret['color_index'][0]]
    print(f"共找到{len(cells)}个点位")
    if len(cells) == 0: return
    
    try:
        current_charge = int(input("Charges: "))
    except:
        current_charge = len(cells)
        
    current_charge = min(len(cells), current_charge)
    sorted_cells = greedy_sort_cells(cells[:current_charge])
    
    avg_area = sum(c['area'] for c in cells) / len(cells)
    avg_length = math.sqrt(avg_area) * 3
    upper_len = int(math.ceil(avg_length * 1.25))
    lower_len = int(math.floor(avg_length * 0.75))
    
    in_range = lambda x, y, z: x >= min(y, z) and x <= max(y, z)
    
    dist = 100
    count = 0
    should_exit = False
    pressed_down = False
    with tqdm.trange(min(len(sorted_cells), current_charge)) as t:
        for i in t:
            if should_exit: 
                print("检测到按键中断操作")
                break
            cell = sorted_cells[i]
            t.set_description_str(f"Cell {i}")
            t.set_postfix_str(f"{cell['center']}|{cell['rect']}|{pressed_down}")
            x, y = cell['center']
            x = x + mx
            y = y + my
            duration = min(random.randint(80, 300)/1000, dist/1000*random.randint(8, 12)/10)
            if i == 0: pyautogui.moveTo(x, y)
            pyautogui.moveTo(x, y, duration=duration)
            if i == 0:
                time.sleep(random.randint(30, 80)/1000)
                pyautogui.click(x, y)
                time.sleep(random.randint(30, 80)/1000)
                
            if not pressed_down:
                pressed_down = True
                keyboard.press('space')
                
            count += 1
            if count >= current_charge or i >= len(sorted_cells) - 1:
                pressed_down = False
                time.sleep(random.randint(10, 50)/1000)
                keyboard.release('space')
                break
            
            next_square = sorted_cells[i+1]
            x1, y1 = cell['center']
            x2, y2 = next_square['center']
            dist = abs(x1-x2) + abs(y1-y2)
            if not in_range(dist, upper_len, lower_len):
                pressed_down = False
                time.sleep(random.randint(10, 50)/1000)
                keyboard.release('space')

def opt_func_4():
    cmds = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'D:\Software\OperaGX\opera.exe'
    ]

    for cmd in cmds:
        if os.path.exists(cmd):
            try:
                subprocess.Popen([cmd, 'wplace.live'])
                print(f'已启动浏览器: {os.path.basename(cmd)}')
            except Exception as e:
                print(f'启动失败: {e}')

def opt_func_5():
    quit()

def on_f2_press():
    global should_exit
    should_exit = True
    
if __name__ == "__main__":
    # 注册F2键监听
    keyboard.on_press_key('f2', lambda _: on_f2_press())
    print_info()
    while True:
        print("""
-------------------------
1. 读取剪贴板生成识别模板
2. 显示识别结果
3. 绘图
4. 一键启动浏览器
5. 退出
-------------------------
        """)
        try:
            option = int(input("输入选项："))
        except: 
            continue
        
        if option == 1:
            opt_func_1()
        elif option == 2:
            opt_func_2()
        elif option == 3:
            opt_func_3()
        elif option == 4:
            opt_func_4()
        elif option == 5:
            opt_func_5()
