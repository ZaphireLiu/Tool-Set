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
    except Exception as e:
        print(e)
        pass

# 设置DPI感知
dpi_mode = set_dpi_aware()
print(f"DPI感知模式: {dpi_mode}")

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

def main():
    print("=== 系统信息 ===")
    check_system_info()
    print()
    
    print("=== 显示器信息 ===")
    monitors = get_monitors_ctypes()
    
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

if __name__ == "__main__":
    main()
