import sys, time, random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QSlider, 
    QLineEdit, QSpacerItem, QSizePolicy, QProgressBar,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PIL import Image, ImageGrab
import screeninfo
import pyautogui

from ImagePreview import show_image_preview_dialog

class MainWindow(QMainWindow):
    
    def __draw_layout(self):
        self.setWindowTitle("绘制工具")
        self.setMinimumSize(600, 350)
        
        # 存储选择的区域数据
        self.draw_area_data = None
        self.color_area_data = None
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 第1行：框选按钮
        row1_layout = QHBoxLayout()
        
        self.btn_select_draw_area = QPushButton("框选绘制区")
        self.btn_select_color_area = QPushButton("框选颜色区")
        
        self.btn_select_draw_area.clicked.connect(self.on_select_draw_area)
        self.btn_select_color_area.clicked.connect(self.on_select_color_area)
        
        row1_layout.addWidget(self.btn_select_draw_area)
        row1_layout.addWidget(self.btn_select_color_area)
        row1_layout.addStretch()
        
        # 第2行：模板和绘制按钮
        row2_layout = QHBoxLayout()
        
        btn_read_clipboard = QPushButton("读取剪贴板模板")
        btn_preview_template = QPushButton("预览模板")
        btn_specified_draw = QPushButton("指定绘制")
        
        btn_read_clipboard.clicked.connect(self.on_read_clipboard)
        btn_preview_template.clicked.connect(self.on_preview_template)
        btn_specified_draw.clicked.connect(self.on_specified_draw)
        
        row2_layout.addWidget(btn_read_clipboard)
        row2_layout.addWidget(btn_preview_template)
        row2_layout.addWidget(btn_specified_draw)
        row2_layout.addStretch()
        
        # 第3行：Dimming 控制
        row3_layout = QHBoxLayout()
        
        dimming_label = QLabel("Dimming")
        
        # 滑动条
        self.dimming_slider = QSlider(Qt.Orientation.Horizontal)
        self.dimming_slider.setRange(0, 90)
        self.dimming_slider.setValue(0)
        self.dimming_slider.setFixedWidth(200)
        
        # 输入框
        self.dimming_input = QLineEdit()
        self.dimming_input.setText("0")
        self.dimming_input.setFixedWidth(60)
        
        # 连接信号和槽，实现联动
        self.dimming_slider.valueChanged.connect(self.on_slider_changed)
        self.dimming_input.textChanged.connect(self.on_input_changed)
        
        row3_layout.addWidget(dimming_label)
        row3_layout.addWidget(self.dimming_slider)
        row3_layout.addWidget(self.dimming_input)
        row3_layout.addStretch()
        
        # 第4行：自动绘制按钮
        row4_layout = QHBoxLayout()
        
        btn_preview_auto = QPushButton("预览自动模板")
        btn_auto_draw = QPushButton("全自动绘制")
        
        btn_preview_auto.clicked.connect(self.on_preview_auto)
        btn_auto_draw.clicked.connect(self.on_auto_draw)
        
        row4_layout.addWidget(btn_preview_auto)
        row4_layout.addWidget(btn_auto_draw)
        row4_layout.addStretch()
        
        # 第5行：进度条 (0-100)
        row5_layout = QHBoxLayout()
        
        progress_label = QLabel("进度:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        
        row5_layout.addWidget(progress_label)
        row5_layout.addWidget(self.progress_bar)
        
        # 第6行：状态文字
        row6_layout = QHBoxLayout()
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("QLabel { font-weight: bold; color: #333; }")
        
        row6_layout.addWidget(self.status_label)
        row6_layout.addStretch()
        
        # 将所有行添加到主布局
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        main_layout.addLayout(row3_layout)
        main_layout.addLayout(row4_layout)
        main_layout.addLayout(row5_layout)
        main_layout.addLayout(row6_layout)
        
        # 添加垂直弹性空间，使控件靠上排列
        main_layout.addStretch()
    
    def __get_monitors_info(self):
        self.monitors = []
        self.offset_x = 0
        self.offset_y = 0
        for i, monitor in enumerate(screeninfo.get_monitors()):
            self.monitors.append(monitor)
            self.offset_x = min(self.offset_x, monitor.x)
            self.offset_y = min(self.offset_y, monitor.y)
            self.set_status_text(f"显示器数据获取中...\n显示器{i}: {monitor.name if hasattr(monitor, 'name') else str(i+1)} ({monitor.x}, {monitor.y}) {monitor.width}x{monitor.height}")
        self.set_status_text(f"显示器数据获取完毕")
        
    def __move_to(self, x, y, duration=0):
        pyautogui.moveTo(x + self.offset_x, y + self.offset_y, duration=duration)
        
    def __click(self, x: None | int = None, y: None | int = None):
        if x is not None and y is not None:
            pyautogui.click(x + self.offset_x, y + self.offset_y)
        else:
            pyautogui.click()
    
    def __init__(self):
        super().__init__()
        self.offset_x = 0
        self.offset_y = 0
        self.status_label.setText('')
        self.__draw_layout()
        self.__get_monitors_info()
        
    def load_image_file(self):
        """加载图像文件"""
        try:
            img = ImageGrab.grab(all_screens=True)
            return img
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法加载图像文件：{str(e)}")
            return None
    
    # 框选区域的回调函数
    def on_select_draw_area(self):
        """框选绘制区域"""
        
        # 加载图像文件
        pil_image = self.load_image_file()
        
        self.set_status_text("正在框选绘制区域...")
        self.set_progress(10)
        
        # 显示图像预览对话框进行区域选择
        result = show_image_preview_dialog(pil_image, self)
        
        if result:
            self.draw_area_data = result
            self.set_status_text(f"绘制区域已选择 - 尺寸: {result['size']}")
            self.set_progress(30)
            
            # 更新按钮文本显示已选择
            self.btn_select_draw_area.setText(f"绘制区({result['size'][0]}x{result['size'][1]})")
            
        else:
            self.set_status_text("取消选择绘制区域")
            self.set_progress(0)
        
    def on_select_color_area(self):
        """框选颜色区域"""
        self.set_status_text("请选择要加载的图像文件...")
        
        # 加载图像文件
        pil_image = self.load_image_file()
        if pil_image is None:
            self.set_status_text("取消选择图像文件")
            return
        
        self.set_status_text("正在框选颜色区域...")
        self.set_progress(15)
        
        # 显示图像预览对话框进行区域选择
        result = show_image_preview_dialog(pil_image, self)
        
        if result:
            self.color_area_data = result
            self.set_status_text(f"颜色区域已选择 - 尺寸: {result['size']}")
            self.set_progress(35)
            
            # 更新按钮文本显示已选择
            self.btn_select_color_area.setText(f"颜色区({result['size'][0]}x{result['size'][1]})")

        else:
            self.set_status_text("取消选择颜色区域")
            self.set_progress(0)
    
    # 进度条控制函数
    def set_progress(self, value):
        """设置进度条值 (0-100)"""
        if 0 <= value <= 100:
            self.progress_bar.setValue(value)
    
    def get_progress(self):
        """获取当前进度值"""
        return self.progress_bar.value()
    
    # 状态文字控制函数
    def set_status_text(self, text, append=False):
        """更改状态文字内容"""
        print(text)
        set_text_preset = self.status_label.text() + '\n' if append else ''
        self.status_label.setText(f"{set_text_preset}{text}")
    
    def get_status_text(self):
        """获取当前状态文字"""
        return self.status_label.text()
    
    # 获取选择数据的公共方法
    def get_draw_area_data(self):
        """获取绘制区域数据"""
        return self.draw_area_data
    
    def get_color_area_data(self):
        """获取颜色区域数据"""
        return self.color_area_data
        
    # 其他按钮的回调函数
    def on_read_clipboard(self):
        # TODO on_read_clipboard
        pass
        
    def on_preview_template(self):
        print("预览模板 - 功能待实现")
        # 检查是否已选择区域
        if self.draw_area_data:
            print(f"可以使用绘制区域数据: {self.draw_area_data['coordinates']}")
        if self.color_area_data:
            print(f"可以使用颜色区域数据: {self.color_area_data['coordinates']}")
        # TODO on_preview_template
        pass
        
    def on_specified_draw(self):
        # TODO on_specified_draw
        pass
        
    def on_slider_changed(self, value):
        """滑动条值改变时更新输入框"""
        self.dimming_input.setText(str(value))
        self.set_status_text(f"Dimming 设置为 {value}")
        
    def on_input_changed(self, text):
        """输入框值改变时更新滑动条"""
        try:
            value = int(text)
            if 0 <= value <= 90:
                self.dimming_slider.setValue(value)
                self.set_status_text(f"Dimming 设置为 {value}")
        except ValueError:
            pass
        
    def on_preview_auto(self):
        # TODO on_preview_auto
        pass
        
    def on_auto_draw(self):
        # TODO on_auto_draw
        pass
