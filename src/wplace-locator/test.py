# imports
import sys, time, random
import tqdm
import cv2
import screeninfo
import keyboard
import pyautogui
import numpy as np
from PIL import Image, ImageGrab
from typing import List, Dict, Optional, Tuple, Union

class ColorLocator():
    
    def __init__(self):
        self.colors_ref = [
            (0, 0, 0), (60, 60, 60), (120, 120, 120), (170, 170, 170), (210, 210, 210), (255, 255, 255), (96, 0, 24), (165, 14, 30), 
            (237, 28, 36), (250, 128, 114), (228, 92, 26), (255, 127, 39), (246, 170, 9), (249, 221, 59), (255, 250, 188), (156, 132, 49), 
            (197, 173, 49), (232, 212, 95), (74, 107, 58), (90, 148, 74), (132, 197, 115), (14, 185, 104), (19, 230, 123), (135, 255, 94), 
            (12, 129, 110), (16, 174, 166), (19, 225, 190), (15, 121, 159), (96, 247, 242), (187, 250, 242), (40, 80, 158), (64, 147, 228), 
            (125, 199, 255), (77, 49, 184), (107, 80, 246), (153, 177, 251), (74, 66, 132), (122, 113, 196), (181, 174, 241), (120, 12, 153), 
            (170, 56, 185), (224, 159, 249), (203, 0, 122), (236, 31, 128), (243, 141, 169), (155, 82, 73), (209, 128, 120), (250, 182, 164), 
            (104, 70, 52), (149, 104, 42), (219, 164, 99), (123, 99, 82), (156, 132, 107), (214, 181, 148), (209, 128, 81), (248, 178, 119), 
            (255, 197, 165), (109, 100, 63), (148, 140, 107), (205, 197, 158), (51, 57, 65), (109, 117, 141), (179, 185, 209)
        ]
        self.dimming = 0
        self.dimming_cache = 0
        self.set_dimming(0, True)
        self.cell_data  = None
        self.grid_data  = None
        self.loc_data   = None
        self.color_data = None
        self.cell_area_multiplier = (0.5, 2)
    
    def set_dimming(self, val: int, update: bool = True):
        self.dimming = self._cap(val, 0, 90)
        if not update: return
        self.colors = []
        for c in self.colors_ref:
            self.colors.append(
                tuple(
                    self._cap(int(x*(100-self.dimming)/100), 0, 255) for x in c
                )
            )
        self.dimming_cache = self.dimming
    
    def update_dimming(self):
        if self.dimming_cache == self.dimming: return
        self.set_dimming(self.dimming, True)
        
    def filter_cell_img(self, img: Image.Image, tol = 0, method = 'contours', specify_colors: list | None = None, exclude_colors: list = []):
        # 获取边框
        mask = self._mask_img(img, tol, specify_colors, exclude_colors)
        if method == 'contours':
            ret = self._get_rectangle_by_contours(mask)
            if ret != None:
                x, y, w, h, area = ret
            else: return None
        elif method == 'bounds':
            ret = self._get_rectangle_by_bounds(mask)
            if ret != None:
                x, y, w, h, area = ret
            else: return None
        else:
            raise ValueError("method 参数必须是 'contours' 或 'bounds'")
        
        # 读取中心像素
        center = (int(x) + int(w/2), int(y) + int(h/2))
        pixel = img.getpixel(center)
        return {
            'loc': (x, y, w, h),
            'area': area,
            'color': pixel
        }
        
    # 内部函数
    
    def _in_range(self, val, min_val, max_val):
        return val == self._cap(val, min_val, max_val)
        
    def _cap(self, val, min_val, max_val):
        return max(min(val, max_val), min_val)
    
    def _contours(self, mask):
        _, binary = cv2.threshold(mask, 240, 255, cv2.THRESH_BINARY)
        return cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    def _get_rectangle_by_contours(self, mask):
        """使用轮廓检测方法"""
        contours, _ = self._contours(mask)
        if not contours:
            return None
        # 找到最大的轮廓（假设白色长方形是最大的白色区域）
        largest_contour = max(contours, key=cv2.contourArea)
        # 获取边界矩形
        x, y, w, h = cv2.boundingRect(largest_contour)
        area = cv2.contourArea(largest_contour)
        return x, y, w, h, area
    
    def _get_rectangle_by_bounds(self, mask):
        """使用边界检测方法"""
        # 二值化处理
        _, binary = cv2.threshold(mask, 240, 255, cv2.THRESH_BINARY)
        # 找到所有白色像素的位置
        white_pixels = np.where(binary == 255)
        if len(white_pixels[0]) == 0:
            return None
        # 计算边界
        min_y, max_y = np.min(white_pixels[0]), np.max(white_pixels[0])
        min_x, max_x = np.min(white_pixels[1]), np.max(white_pixels[1])
        x, y = min_x, min_y
        w    = max_x - min_x + 1
        h    = max_y - min_y + 1
        area = len(white_pixels[0])
        return x, y, w, h, area
    
    def _mask_img(self, img: Image.Image, tol = 0, specify_colors: list | None = None, exclude_colors: list = []):
        if len(exclude_colors) > 0 and specify_colors is not None:
            for c in exclude_colors:
                specify_colors.remove(c)
        
        color_list = specify_colors if specify_colors is not None else self.colors
        
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        # 获取掩码图像
        img_array = np.array(img)
        # 创建掩码
        mask = np.zeros(img_array.shape[:2], dtype=bool)
        # 遍历
        for color in color_list:
            if tol == 0:
                color_mask = np.all(img_array == color, axis=2)
            else:
                diff = np.abs(img_array.astype(int) - np.array(color).astype(int))
                color_mask = np.all(diff <= tol, axis=2)
            mask |= color_mask

        result = np.zeros(img_array.shape[:2], dtype=np.uint8)
        result[mask] = 255
        return result.astype(np.uint8)
        # return Image.fromarray(result.astype(np.uint8))

# 边框定位类
class MultiMonitorSquareDetector:
    def __init__(self):
        self.monitors = self.get_monitor_info()
        self.primary_monitor = self.get_primary_monitor()
    
    def get_monitor_info(self) -> List[Dict]:
        """获取所有显示器信息"""
        monitors = []
        try:
            for i, monitor in enumerate(screeninfo.get_monitors()):
                monitors.append({
                    'index': i,
                    'name': monitor.name if hasattr(monitor, 'name') else f"Monitor {i+1}",
                    'x': monitor.x,
                    'y': monitor.y,
                    'width': monitor.width,
                    'height': monitor.height,
                    'is_primary': monitor.is_primary if hasattr(monitor, 'is_primary') else (i == 0)
                })
        except Exception as e:
            print(f"警告：无法获取显示器信息，使用默认配置: {e}")
            # 如果screeninfo失败，使用pyautogui获取主显示器信息
            screen_size = pyautogui.size()
            monitors.append({
                'index': 0,
                'name': "Primary Monitor",
                'x': 0,
                'y': 0,
                'width': screen_size.width,
                'height': screen_size.height,
                'is_primary': True
            })
        return monitors
    
    def get_primary_monitor(self):
        """获取主显示器信息"""
        for monitor in self.monitors:
            if monitor['is_primary']:
                return monitor
        return self.monitors[0] if self.monitors else None
    
    def list_monitors(self) -> None:
        """列出所有显示器信息"""
        print("可用显示器:")
        for monitor in self.monitors:
            primary_tag = " [主显示器]" if monitor['is_primary'] else ""
            print(f"  {monitor['index']}: {monitor['name']}{primary_tag}")
            print(f"    位置: ({monitor['x']}, {monitor['y']})")
            print(f"    分辨率: {monitor['width']} x {monitor['height']}")
            print()
    
    def capture_monitor(self, monitor_index: Optional[int] = None) -> np.ndarray:
        """
        截取指定显示器的屏幕
        monitor_index: 显示器索引，None表示截取所有显示器
        """
        if monitor_index is None:
            # 截取所有显示器
            screenshot = ImageGrab.grab()
        else:
            if monitor_index < 0 or monitor_index >= len(self.monitors):
                raise ValueError(f"显示器索引 {monitor_index} 无效，可用范围: 0-{len(self.monitors)-1}")
            
            monitor = self.monitors[monitor_index]
            # 截取指定显示器区域
            bbox = (
                monitor['x'], 
                monitor['y'], 
                monitor['x'] + monitor['width'], 
                monitor['y'] + monitor['height']
            )
            screenshot = ImageGrab.grab(bbox)
        
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_colored_squares(self, 
                           color_bgr: Tuple[int, int, int],
                           min_area: int = 100,
                           max_area: int = 10000,
                           monitor_index: Optional[int] = None,
                           color_tolerance: int = 10,
                           aspect_ratio_tolerance: float = 0.2) -> List[Dict]:
        """
        在指定显示器上寻找指定颜色的正方形
        
        Args:
            color_bgr: BGR格式的颜色值
            min_area: 最小面积
            max_area: 最大面积
            monitor_index: 显示器索引，None表示搜索所有显示器
            color_tolerance: 颜色容差
            aspect_ratio_tolerance: 长宽比容差
        
        Returns:
            包含正方形信息的字典列表
        """
        if monitor_index is not None:
            return self._find_squares_single_monitor(
                color_bgr, min_area, max_area, monitor_index, 
                color_tolerance, aspect_ratio_tolerance
            )
        else:
            # 在所有显示器上搜索
            all_squares = []
            for i in range(len(self.monitors)):
                squares = self._find_squares_single_monitor(
                    color_bgr, min_area, max_area, i, 
                    color_tolerance, aspect_ratio_tolerance
                )
                all_squares.extend(squares)
            return all_squares
    
    def _find_squares_single_monitor(self, 
                                   color_bgr: Tuple[int, int, int],
                                   min_area: int,
                                   max_area: int,
                                   monitor_index: int,
                                   color_tolerance: int,
                                   aspect_ratio_tolerance: float) -> List[Dict]:
        """在单个显示器上寻找正方形"""
        
        if monitor_index < 0 or monitor_index >= len(self.monitors):
            raise ValueError(f"显示器索引 {monitor_index} 无效")
        
        monitor = self.monitors[monitor_index]
        screenshot = self.capture_monitor(monitor_index)
        
        # 创建颜色掩码
        lower_bound = np.array([max(0, c - color_tolerance) for c in color_bgr])
        upper_bound = np.array([min(255, c + color_tolerance) for c in color_bgr])
        mask = cv2.inRange(screenshot, lower_bound, upper_bound)
        
        # 形态学操作，清理噪声
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        squares = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area <= area <= max_area:
                # 近似轮廓为多边形
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # 检查是否为4边形
                if len(approx) == 4:
                    # 获取边界框
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # 检查长宽比
                    aspect_ratio = float(w) / h
                    if abs(aspect_ratio - 1.0) <= aspect_ratio_tolerance:
                        # 转换为全局坐标
                        global_x = monitor['x'] + x
                        global_y = monitor['y'] + y
                        global_center_x = monitor['x'] + x + w // 2
                        global_center_y = monitor['y'] + y + h // 2
                        
                        squares.append({
                            'monitor_index': monitor_index,
                            'monitor_name': monitor['name'],
                            'center': (global_center_x, global_center_y),
                            'center_relative': (x + w//2, y + h//2),  # 相对于显示器的坐标
                            'top_left': (global_x, global_y),
                            'top_left_relative': (x, y),  # 相对于显示器的坐标
                            'width': w,
                            'height': h,
                            'area': area,
                            'aspect_ratio': aspect_ratio
                        })
        
        return squares
    
    def find_squares_by_size(self,
                           color_bgr: Tuple[int, int, int],
                           target_size: int,
                           monitor_index: Optional[int] = None,
                           size_tolerance: int = 5,
                           color_tolerance: int = 10) -> List[Dict]:
        """
        根据指定大小寻找正方形
        
        Args:
            color_bgr: BGR格式的颜色值
            target_size: 目标边长
            monitor_index: 显示器索引
            size_tolerance: 大小容差
            color_tolerance: 颜色容差
        """
        min_area = (target_size - size_tolerance) ** 2
        max_area = (target_size + size_tolerance) ** 2
        
        return self.find_colored_squares(
            color_bgr, min_area, max_area, monitor_index, color_tolerance
        )
    
    def visualize_results(self, squares: List[Dict], save_path: Optional[str] = None) -> None:
        """
        可视化检测结果
        
        Args:
            squares: 检测到的正方形列表
            save_path: 保存路径，None表示不保存
        """
        if not squares:
            print("没有找到正方形")
            return
        
        # 按显示器分组
        monitor_squares = {}
        for square in squares:
            monitor_idx = square['monitor_index']
            if monitor_idx not in monitor_squares:
                monitor_squares[monitor_idx] = []
            monitor_squares[monitor_idx].append(square)
        
        # 为每个有检测结果的显示器创建可视化
        for monitor_idx, monitor_square_list in monitor_squares.items():
            screenshot = self.capture_monitor(monitor_idx)
            
            # 在图像上标记正方形
            for i, square in enumerate(monitor_square_list):
                x, y = square['top_left_relative']
                w, h = square['width'], square['height']
                
                # 绘制边界框
                cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 1)
                
                # 标记中心点
                center = square['center_relative']
                cx, cy = center
                cv2.circle(screenshot, center, 1, (0, 0, 255), -1)
                cv2.line(screenshot, (cx - 3, cy), (cx + 3, cy), (0, 0, 255), 1)
                cv2.line(screenshot, (cx, cy - 3), (cx, cy + 3), (0, 0, 255), 1)
                
                # 添加文本标签
                # label = f"#{i+1} ({w}x{h})"
                # cv2.putText(screenshot, label, (x, y - 10), 
                #           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # 显示结果
            window_name = f"Monitor {monitor_idx} - Found {len(monitor_square_list)} squares"
            cv2.imshow(window_name, screenshot)
            
            # 保存结果
            if save_path:
                save_filename = f"{save_path}_monitor_{monitor_idx}.png"
                cv2.imwrite(save_filename, screenshot)
                print(f"结果已保存到: {save_filename}")
        
        print("按任意键关闭窗口...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# 图片读取函数

def get_image_info_from_clipboard():
    """
    从剪贴板读取图片并返回长、宽和中心像素颜色信息
    
    Returns:
        tuple: (width, height, center_color_bgr) 或 None（如果失败）
    """
    try:
        # 从剪贴板获取内容
        clipboard_content = ImageGrab.grabclipboard()
        
        # 检查剪贴板内容是否为图片
        if clipboard_content is None:
            print("错误：剪贴板中没有内容或不是图片格式")
            return None
        
        if not isinstance(clipboard_content, Image.Image):
            print("错误：剪贴板中的内容不是图片")
            return None
        
        # 将PIL图片转换为OpenCV格式（BGR）
        # PIL使用RGB格式，需要转换为BGR
        image_rgb = np.array(clipboard_content)
        
        # 检查图片是否有效
        if image_rgb.size == 0:
            print("错误：图片为空")
            return None
        
        # 如果是RGBA格式，转换为RGB
        if len(image_rgb.shape) == 3 and image_rgb.shape[2] == 4:
            # 处理透明通道，将透明部分设为白色背景
            image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGBA2RGB)
        
        # 转换为BGR格式（OpenCV标准格式）
        if len(image_rgb.shape) == 3:
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        else:
            # 灰度图转换为BGR
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_GRAY2BGR)
        
        # 获取图片尺寸
        height, width = image_bgr.shape[:2]
        
        # 计算中心位置
        center_x = width // 2
        center_y = height // 2
        
        # 获取中心像素的BGR颜色值
        center_color_bgr = image_bgr[center_y, center_x]
        
        # 转换为Python原生int类型（避免numpy类型）
        center_color_bgr = tuple(int(color) for color in center_color_bgr)
        
        return width, height, center_color_bgr
        
    except Exception as e:
        print(f"错误：处理剪贴板图片时发生异常 - {e}")
        return None

def show_image_with_center_mark(width, height, center_color):
    """
    可选功能：显示图片并在中心位置标记
    """
    try:
        # 重新从剪贴板获取图片用于显示
        clipboard_image = ImageGrab.grabclipboard()
        if clipboard_image is None:
            return
        
        # 转换为OpenCV格式
        image_array = np.array(clipboard_image)
        if len(image_array.shape) == 3 and image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        if len(image_array.shape) == 3:
            image_display = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        else:
            image_display = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
        
        # 在中心位置画一个十字标记
        center_x, center_y = width // 2, height // 2
        
        # 画十字线（白色，带黑色边框以确保可见性）
        cv2.line(image_display, (center_x-10, center_y), (center_x+10, center_y), (0, 0, 0), 3)
        cv2.line(image_display, (center_x, center_y-10), (center_x, center_y+10), (0, 0, 0), 3)
        cv2.line(image_display, (center_x-10, center_y), (center_x+10, center_y), (255, 255, 255), 1)
        cv2.line(image_display, (center_x, center_y-10), (center_x, center_y+10), (255, 255, 255), 1)
        
        # 画中心点
        cv2.circle(image_display, (center_x, center_y), 1, (0, 0, 255), -1)  # 红色圆点
        
        # 添加颜色信息文本
        text = f"Center: {center_color} (BGR)"
        cv2.putText(image_display, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(image_display, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        
        # 显示图片
        cv2.imshow('Clipboard Image - Center Marked', image_display)
        print(f"\n图片已显示，按任意键关闭窗口...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"显示图片时出错: {e}")

# 简化版本（只返回核心信息）
def get_clipboard_image_info_simple():
    """简化版本：只返回核心信息，无额外输出"""
    try:
        clipboard_content = ImageGrab.grabclipboard()
        
        if clipboard_content is None or not isinstance(clipboard_content, Image.Image):
            return None
        
        image_array = np.array(clipboard_content)
        if len(image_array.shape) == 3 and image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        if len(image_array.shape) == 3:
            image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        else:
            image_bgr = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
        
        height, width = image_bgr.shape[:2]
        center_color = tuple(int(c) for c in image_bgr[height//2, width//2])
        
        return width, height, center_color
    except:
        return None

def greedy_sort_by_center(data_list):
    """
    贪心排序函数：第一个元素不变，其余元素按照与上一个元素center距离最近的原则排序
    
    Args:
        data_list: 包含字典的列表，每个字典有'center'属性（二元组）
    
    Returns:
        排序后的列表
    """
    if len(data_list) <= 1:
        return data_list.copy()
    
    # 复制列表避免修改原列表
    remaining = data_list[1:].copy()  # 除第一个元素外的所有元素
    result = [data_list[0]]  # 结果列表，第一个元素不变
    
    # 计算两点间的欧几里得距离
    def distance(center1, center2):
        return ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5
    
    # 贪心选择：每次选择与当前最后一个元素center距离最近的
    while remaining:
        current_center = result[-1]['center']
        
        # 找到距离最近的元素
        min_distance = float('inf')
        closest_index = 0
        
        for i, item in enumerate(remaining):
            dist = distance(current_center, item['center'])
            if dist < min_distance:
                min_distance = dist
                closest_index = i
        
        # 将最近的元素添加到结果中，并从剩余列表中移除
        result.append(remaining.pop(closest_index))
    
    return result

should_exit    = False
color          = None
area           = 0
min_multiplier = 0.5
max_multiplier = 2
square_tol     = 0.2

def opt_func_1():
    try:
        global color, area
        # ret = get_clipboard_image_info_simple()
        # if ret is None: return
        # w, h, color = ret
        # area = w*h
        clipboard_content = ImageGrab.grabclipboard()
        print(clipboard_content)
        loc = ColorLocator()
        try: 
            dimming = int(input("输入dimming值(默认25): "))
        except: 
            dimming = 25
            
        loc.set_dimming(dimming)
        ret = loc.filter_cell_img(clipboard_content, 0 if dimming == 0 else 2)
        print(ret)
        area = ret['area']
        color = list(ret['color'])[::-1]
        
        min_area = int(area * min_multiplier)
        max_area = int(area * max_multiplier)

        print(area, color)

        detector = MultiMonitorSquareDetector()
        # 列出所有显示器
        detector.list_monitors()

        # 在所有显示器上寻找正方形
        print("在所有显示器上寻找正方形...")
        red_squares = detector.find_colored_squares(
            color_bgr=color,
            min_area=min_area,
            max_area=max_area
        )
        print(f"找到 {len(red_squares)} 个正方形")
        
    except Exception as e:
        print("读取失败，剪贴板可能不是图片")
        print(e)
        
def opt_func_2():
    global color, area
    min_area = int(area * min_multiplier)
    max_area = int(area * max_multiplier)
    detector = MultiMonitorSquareDetector()
    squares = detector.find_colored_squares(
        # monitor_index=0,
        color_bgr=color,
        min_area=min_area,
        max_area=max_area
    )
    if squares:
        detector.visualize_results(squares)
    
def opt_func_3():
    global should_exit, color, area
    min_area = int(area * min_multiplier)
    max_area = int(area * max_multiplier)
    should_exit = False
    
    detector = MultiMonitorSquareDetector()
    # 列出所有显示器
    detector.list_monitors()

    # 在所有显示器上寻找正方形
    print("在所有显示器上寻找正方形...")
    squares = detector.find_colored_squares(
        color_bgr=color,
        min_area=min_area,
        max_area=max_area
    )
    
    count = 0
    print(f"找到 {len(squares)} 个正方形")
    if len(squares) == 0: return
    try:
        input_str = input("Charges：")
        current_charge = int(input_str) if len(input_str) > 0 and not (input_str is None) else len(squares)
    except:
        current_charge = len(squares)
        
    sorted_squares = greedy_sort_by_center(squares[:min(len(squares), current_charge)])
    with tqdm.trange(min(len(sorted_squares), current_charge)) as t:
        for i in t:
            if should_exit: break
            square = sorted_squares[i]
            t.set_description_str(f"Square {i}")
            t.set_postfix_str(f"Cord: {square['center']} Size: {square['width']}x{square['height']}={square['area']}")
            # print(f"  显示器: {square['monitor_name']} (索引: {square['monitor_index']})")
            # print(f"  全局坐标 - 中心: {square['center']}, 左上角: {square['top_left']}")
            # print(f"  相对坐标 - 中心: {square['center_relative']}, 左上角: {square['top_left_relative']}")
            x, y = square['center']
            pyautogui.moveTo(x, y, duration=random.randint(80, 150) / 1000)
            time.sleep(random.randint(10, 20) / 1000)
            pyautogui.click(x, y)
            count += 1
            time.sleep(random.randint(10, 30) / 1000)
            if count >= current_charge:
                break


def opt_func_4():
    pass

def on_f2_press():
    global should_exit
    should_exit = True
    print("\n检测到F2键，准备退出...")
# 注册F2键监听
keyboard.on_press_key('f2', lambda _: on_f2_press())

while True:
    print("""
        ---------------------------------
            1. 读取剪贴板生成识别模板
            2. 显示识别结果
            3. 绘图
        ---------------------------------
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
