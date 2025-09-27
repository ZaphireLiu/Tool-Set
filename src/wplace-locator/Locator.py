import cv2
import numpy as np
from PIL import Image

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
        # self.grid_data  = None
        # self.loc_data   = None
        # self.color_data = None
        self.cell_area_multiplier = (0.5, 2)
        self.cell_filter_config = {
            'min_mul': 0.6,
            'max_mul': 3,
            'square_tol': 0.3
        }
        
    def set_cell_filter_config(self, min_mul, max_mul, square_tol):
        self.cell_filter_config = {
            'min_mul': self._cap(min_mul, 0, 1),
            'max_mul': self._cap(max_mul, 1, 9),
            'square_tol': self._cap(square_tol, 0, 1)
        }
    
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
        img = img.convert('RGB')
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
        
        self.cell_data = {
            'loc': (x, y, w, h),
            'area': area,
            'color': pixel
        }
        
        return self.cell_data
    
    def locate_cells(self, 
        img: Image.Image, 
        tol: int = 0, 
        single_color: bool = True, 
        specify_area: tuple[int] | None = None,
        specify_colors: list | None = None, 
        exclude_colors: list = []
    ):
        if self.cell_data is None:
            raise RuntimeError("未指定单元数据")
        if specify_area is not None and len(specify_area) != 4:
            raise AssertionError("specify_area 需要为(x, y, w, h)的格式")
        
        self.update_dimming()
        if specify_area:
            ax, ay, aw, ah = specify_area
            for check in [aw, ah]:
                if check < 0: raise AssertionError(
                    "specify_area 需要为(x, y, w, h)的格式"
                )
        
        img = img.convert('RGB')
        if not single_color:
            mask = self._mask_img(img, tol, specify_colors, exclude_colors)
        else:
            mask = self._mask_img(img, tol, specify_colors=[self.cell_data['color']])
            
        countours, _ = self._contours(mask)
        
        ret = dict()
        ret['color_index'] = []
        ret['cells'] = dict()
        for c in countours:
            x, y, w, h = cv2.boundingRect(c)
            area_flag = self._in_range(
                w * h,
                int(self.cell_data['area'] * self.cell_filter_config['min_mul']), 
                int(self.cell_data['area'] * self.cell_filter_config['max_mul'])
            )
            square_flag = (min(w, h) / max(w, h)) >= (1.0 - self.cell_filter_config['square_tol'])
            if (not area_flag) or (not square_flag): continue
            cx, cy =  int(x+w/2), int(y+h/2)
            if specify_area:
                if (not self._in_range(cx, ax, ax + aw)) or (not self._in_range(cy, ay, ay + ah)): continue
            color = img.getpixel((cx, cy))
            color_idx = self.color_idx(color, tol)
            if color_idx is None: continue
            
            if color_idx not in ret['color_index']:
                ret['color_index'].append(color_idx)
            if ret['cells'].get(color_idx) is None:
                ret['cells'][color_idx] = []
            
            ret['cells'][color_idx].append({
                'index': color_idx,
                'color': color,
                'original_color': self.colors_ref[color_idx],
                'center': (cx, cy),
                'rect': (x, y, w, h),
                'area': w * h
            })
            
        return ret if len(ret['color_index']) != 0 else None
        
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
        
    def color_idx(self, color, tol = 0, use_ref_color = False):
        if use_ref_color: tol = 0
        for i in range(len(self.colors_ref)):
            color_comp = self.colors[i] if not use_ref_color else self.colors_ref[i]
            diff_max = 0
            for j in range(3):
                diff = abs(color[j] - color_comp[j])
                diff_max = max(diff_max, diff)
                
            if diff_max < tol: return i
            
        return None