import sys
import re
from typing import List, Tuple
from PIL import Image
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                               QHBoxLayout, QWidget, QPushButton, QLineEdit, 
                               QLabel, QScrollArea, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QPalette, QClipboard, QPixmap

class ColorMatchWorker(QThread):
    """颜色匹配工作线程"""
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, target_color, color_palette):
        super().__init__()
        self.target_color = target_color
        self.color_palette = color_palette
    
    def run(self):
        try:
            matches = self.find_closest_colors(self.target_color, self.color_palette, 8)
            self.finished.emit(matches)
        except Exception as e:
            self.error.emit(str(e))
    
    def find_closest_colors(self, target_color: Tuple[int, int, int], 
                           palette: List[Tuple[str, str]], 
                           count: int) -> List[Tuple[str, str, Tuple[int, int, int], float]]:
        """找到最接近的颜色"""
        distances = []
        target_r, target_g, target_b = target_color
        
        for name, hex_color in palette:
            # 将十六进制颜色转换为RGB
            r, g, b = self.hex_to_rgb(hex_color)
            
            # 计算欧几里得距离
            distance = np.sqrt((target_r - r)**2 + (target_g - g)**2 + (target_b - b)**2)
            distances.append((name, hex_color, (r, g, b), distance))
        
        # 按距离排序并返回前count个
        distances.sort(key=lambda x: x[3])
        return distances[:count]
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class ColorListItem(QFrame):
    """颜色列表项组件"""
    def __init__(self, rank: int, name: str, hex_color: str, rgb_color: Tuple[int, int, int], similarity: float):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedHeight(80)
        self.setStyleSheet("QFrame { margin: 2px; }")
        
        # 主布局
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 8, 10, 8)
        
        # 排名标签
        rank_label = QLabel(f"#{rank}")
        rank_label.setFixedSize(30, 60)
        rank_label.setAlignment(Qt.AlignCenter)
        rank_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(rank_label)
        
        # 颜色块
        color_block = QLabel()
        color_block.setFixedSize(60, 60)
        # 根据颜色亮度选择边框颜色
        brightness = sum(rgb_color) / 3
        border_color = "#ffffff" if brightness < 100 else "#000000"
        color_block.setStyleSheet(f"""
            QLabel {{
                background-color: {hex_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(color_block)
        
        # 信息区域
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # 颜色名称
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        # 十六进制值
        hex_label = QLabel(hex_color.upper())
        hex_label.setStyleSheet("font-size: 14px; font-family: 'Consolas', 'Monaco', monospace;")
        info_layout.addWidget(hex_label)
        
        # RGB值
        rgb_label = QLabel(f"RGB({rgb_color[0]}, {rgb_color[1]}, {rgb_color[2]})")
        rgb_label.setStyleSheet("font-size: 12px;")
        info_layout.addWidget(rgb_label)
        
        main_layout.addLayout(info_layout)
        
        # 弹性空间
        main_layout.addStretch()
        
        # 相似度信息
        similarity_layout = QVBoxLayout()
        similarity_layout.setAlignment(Qt.AlignCenter)
        
        similarity_percent = 100 - similarity
        similarity_label = QLabel(f"{similarity_percent:.1f}%")
        similarity_label.setAlignment(Qt.AlignCenter)
        similarity_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
        """)
        similarity_layout.addWidget(similarity_label)
        
        similarity_text = QLabel("相似度")
        similarity_text.setAlignment(Qt.AlignCenter)
        similarity_text.setStyleSheet("font-size: 10px;")
        similarity_layout.addWidget(similarity_text)
        
        # 距离信息（用于调试）
        distance_label = QLabel(f"距离: {similarity:.1f}")
        distance_label.setAlignment(Qt.AlignCenter)
        distance_label.setStyleSheet("font-size: 9px;")
        similarity_layout.addWidget(distance_label)
        
        main_layout.addLayout(similarity_layout)
        
        self.setLayout(main_layout)

class ColorMatcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.color_palette = self.create_color_palette()
        self.init_ui()
        
    def create_color_palette(self) -> List[Tuple[str, str]]:
        """创建颜色调色板 - 使用十六进制格式存储"""
        return [
            ("Black", "#000000"),
            ("Dark Gray", "#3c3c3c"),
            ("Gray", "#787878"),
            ("Medium Gray", "#aaaaaa"),
            ("Light Gray", "#d2d2d2"),
            ("White", "#ffffff"),
            ("Deep Red", "#600018"),
            ("Dark Red", "#a50e1e"),
            ("Red", "#ed1c24"),
            ("Light Red", "#fa8072"),
            ("Dark Orange", "#e45c1a"),
            ("Orange", "#ff7f27"),
            ("Gold", "#f6aa09"),
            ("Yellow", "#f9dd3b"),
            ("Light Yellow", "#fffabc"),
            ("Dark Goldenrod", "#9c8431"),
            ("Goldenrod", "#c5ad31"),
            ("Light Goldenrod", "#e8d45f"),
            ("Dark Olive", "#4a6b3a"),
            ("Olive", "#5a944a"),
            ("Light Olive", "#84c573"),
            ("Dark Green", "#0eb968"),
            ("Green", "#13e67b"),
            ("Light Green", "#87ff5e"),
            ("Dark Teal", "#0c816e"),
            ("Teal", "#10aea6"),
            ("Light Teal", "#13e1be"),
            ("Dark Cyan", "#0f799f"),
            ("Cyan", "#60f7f2"),
            ("Light Cyan", "#bbfaf2"),
            ("Dark Blue", "#28509e"),
            ("Blue", "#4093e4"),
            ("Light Blue", "#7dc7ff"),
            ("Dark Indigo", "#4d31b8"),
            ("Indigo", "#6b50f6"),
            ("Light Indigo", "#99b1fb"),
            ("Dark Slate Blue", "#4a4284"),
            ("Slate Blue", "#7a71c4"),
            ("Light Slate Blue", "#b5aef1"),
            ("Dark Purple", "#780c99"),
            ("Purple", "#aa38b9"),
            ("Light Purple", "#e09ff9"),
            ("Dark Pink", "#cb007a"),
            ("Pink", "#ec1f80"),
            ("Light Pink", "#f38da9"),
            ("Dark Peach", "#9b5249"),
            ("Peach", "#d18078"),
            ("Light Peach", "#fab6a4"),
            ("Dark Brown", "#684634"),
            ("Brown", "#95682a"),
            ("Light Brown", "#dba463"),
            ("Dark Tan", "#7b6352"),
            ("Tan", "#9c846b"),
            ("Light Tan", "#d6b594"),
            ("Dark Beige", "#d18051"),
            ("Beige", "#f8b277"),
            ("Light Beige", "#ffc5a5"),
            ("Dark Stone", "#6d643f"),
            ("Stone", "#948c6b"),
            ("Light Stone", "#cdc59e"),
            ("Dark Slate", "#333941"),
            ("Slate", "#6d758d"),
            ("Light Slate", "#b3b9d1")
        ]
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("颜色匹配器")
        self.setGeometry(100, 100, 700, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # 输入区域
        input_layout = self.create_input_section()
        main_layout.addLayout(input_layout)
        
        # 当前颜色显示区域
        self.current_color_label = QLabel("当前颜色")
        self.current_color_label.setAlignment(Qt.AlignCenter)
        self.current_color_label.setFixedHeight(80)
        self.current_color_label.setStyleSheet("""
            QLabel {
                border: 2px solid #34495e;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px;
            }
        """)
        main_layout.addWidget(self.current_color_label)
        
        # 匹配结果标题
        results_title = QLabel(f"匹配结果 (从 {len(self.color_palette)} 种颜色中选出相似度最高的8种)")
        results_title.setAlignment(Qt.AlignCenter)
        results_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
                padding: 5px;
            }
        """)
        main_layout.addWidget(results_title)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                background: #ecf0f1;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #95a5a6;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7f8c8d;
            }
        """)
        
        # 创建滚动内容容器
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_content.setLayout(self.scroll_layout)
        
        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area)
        
        central_widget.setLayout(main_layout)
    
    def create_input_section(self) -> QVBoxLayout:
        """创建输入区域"""
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel("颜色输入")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin: 10px;
                padding: 8px;
            }
        """)
        layout.addWidget(title)
        
        # 颜色输入框
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("颜色代码:"))
        
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("输入颜色代码，如: #66ccff 或 rgb(102,204,255)")
        self.color_input.returnPressed.connect(self.match_from_input)
        self.color_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        input_layout.addWidget(self.color_input)
        
        match_btn = QPushButton("匹配颜色")
        match_btn.clicked.connect(self.match_from_input)
        match_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        input_layout.addWidget(match_btn)
        
        layout.addLayout(input_layout)
        
        # 剪贴板图片按钮
        clipboard_layout = QHBoxLayout()
        clipboard_btn = QPushButton("📋 从剪贴板获取图片颜色")
        clipboard_btn.clicked.connect(self.match_from_clipboard)
        clipboard_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        clipboard_layout.addWidget(clipboard_btn)
        
        # 添加颜色调色板数量显示
        palette_info = QLabel(f"💡 内置 {len(self.color_palette)} 种颜色")
        palette_info.setStyleSheet("color: #7f8c8d; font-size: 12px; font-weight: bold;")
        clipboard_layout.addWidget(palette_info)
        
        layout.addLayout(clipboard_layout)
        
        return layout
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c*2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """将RGB颜色转换为十六进制"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def parse_color(self, color_str: str) -> Tuple[int, int, int]:
        """解析颜色字符串"""
        color_str = color_str.strip()
        
        # 十六进制格式 #rrggbb 或 #rgb
        hex_match = re.match(r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$', color_str)
        if hex_match:
            return self.hex_to_rgb(color_str)
        
        # RGB格式 rgb(r,g,b)
        rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str.lower())
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            # 验证RGB值范围
            if all(0 <= val <= 255 for val in (r, g, b)):
                return (r, g, b)
            else:
                raise ValueError("RGB值必须在0-255范围内")
        
        raise ValueError("无效的颜色格式，支持格式: #rrggbb, #rgb, rgb(r,g,b)")
    
    def get_average_color_from_image(self, image: Image.Image) -> Tuple[int, int, int]:
        """计算图片的平均颜色"""
        # 转换为RGB模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 缩放图片以提高性能
        image = image.resize((100, 100))
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 计算平均色
        avg_color = np.mean(img_array, axis=(0, 1))
        
        return tuple(map(int, avg_color))
    
    def match_from_input(self):
        """从输入框匹配颜色"""
        try:
            color_str = self.color_input.text()
            if not color_str:
                QMessageBox.warning(self, "警告", "请输入颜色代码")
                return
            
            target_color = self.parse_color(color_str)
            self.display_current_color(target_color)
            self.start_color_matching(target_color)
            
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"颜色解析失败: {str(e)}")
    
    def match_from_clipboard(self):
        """从剪贴板匹配颜色"""
        try:
            clipboard = QApplication.clipboard()
            pixmap = clipboard.pixmap()
            
            if pixmap.isNull():
                QMessageBox.warning(self, "警告", "剪贴板中没有图片")
                return
            
            # 转换为PIL图片
            image = pixmap.toImage()
            width = image.width()
            height = image.height()
            
            ptr = image.constBits()
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA
            pil_image = Image.fromarray(arr).convert('RGB')  # 只取RGB
            pil_arr = np.array(pil_image)[:, :, ::-1]
            pil_image = Image.fromarray(pil_arr).convert('RGB')
            
            target_color = self.get_average_color_from_image(pil_image)
            self.display_current_color(target_color)
            self.start_color_matching(target_color)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理剪贴板图片失败: {str(e)}")
    
    def display_current_color(self, color: Tuple[int, int, int]):
        """显示当前颜色"""
        r, g, b = color
        hex_color = self.rgb_to_hex(r, g, b)
        
        # 根据颜色亮度选择文字颜色
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = 'white' if brightness < 128 else 'black'
        
        self.current_color_label.setText(
            f"🎨 当前颜色: {hex_color.upper()} | RGB({r}, {g}, {b})"
        )
        self.current_color_label.setStyleSheet(f"""
            QLabel {{
                background-color: {hex_color};
                color: {text_color};
                border: 2px solid #34495e;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px;
            }}
        """)
    
    def start_color_matching(self, target_color: Tuple[int, int, int]):
        """启动颜色匹配"""
        # 清空之前的结果
        self.clear_results()
        
        # 启动工作线程
        self.worker = ColorMatchWorker(target_color, self.color_palette)
        self.worker.finished.connect(self.display_results)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def clear_results(self):
        """清空结果显示"""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def display_results(self, matches: List[Tuple[str, str, Tuple[int, int, int], float]]):
        """显示匹配结果"""
        self.clear_results()
        
        for i, (name, hex_color, rgb_color, distance) in enumerate(matches, 1):
            color_item = ColorListItem(i, name, hex_color, rgb_color, distance)
            self.scroll_layout.addWidget(color_item)
        
        # 添加弹性空间
        self.scroll_layout.addStretch()
    
    def handle_error(self, error_msg: str):
        """处理错误"""
        QMessageBox.critical(self, "错误", f"颜色匹配失败: {error_msg}")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = ColorMatcherApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
