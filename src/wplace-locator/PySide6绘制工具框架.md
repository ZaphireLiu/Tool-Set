# PySide6绘制工具框架

## 🧑‍💻 User

给出一个pyside6框架（后端逻辑留空即可）
主页面分为几行提供：
第1行：按钮【框选绘制区】，按钮【框选颜色区】
第2行：按钮【读取剪贴板模板】，按钮【预览模板】，按钮【指定绘制】
第2行：说明文字：Dimming + 一个滑动条 + 联动的输入框（0~90）
第3行：按钮【预览自动模板】，按钮【全自动绘制】

---
## 🤖 Assistant

以下是一个基于PySide6的应用程序框架：

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QSlider, 
    QLineEdit, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("绘制工具")
        self.setMinimumSize(600, 300)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 第1行：框选按钮
        row1_layout = QHBoxLayout()
        
        btn_select_draw_area = QPushButton("框选绘制区")
        btn_select_color_area = QPushButton("框选颜色区")
        
        btn_select_draw_area.clicked.connect(self.on_select_draw_area)
        btn_select_color_area.clicked.connect(self.on_select_color_area)
        
        row1_layout.addWidget(btn_select_draw_area)
        row1_layout.addWidget(btn_select_color_area)
        row1_layout.addStretch()  # 添加弹性空间
        
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
        self.dimming_slider = QSlider(Qt.Horizontal)
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
        
        # 将所有行添加到主布局
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        main_layout.addLayout(row3_layout)
        main_layout.addLayout(row4_layout)
        
        # 添加垂直弹性空间，使控件靠上排列
        main_layout.addStretch()
        
    # 第1行按钮的回调函数
    def on_select_draw_area(self):
        print("框选绘制区 - 功能待实现")
        # TODO: 实现框选绘制区功能
        
    def on_select_color_area(self):
        print("框选颜色区 - 功能待实现")
        # TODO: 实现框选颜色区功能
        
    # 第2行按钮的回调函数
    def on_read_clipboard(self):
        print("读取剪贴板模板 - 功能待实现")
        # TODO: 实现读取剪贴板模板功能
        
    def on_preview_template(self):
        print("预览模板 - 功能待实现")
        # TODO: 实现预览模板功能
        
    def on_specified_draw(self):
        print("指定绘制 - 功能待实现")
        # TODO: 实现指定绘制功能
        
    # 第3行 Dimming 控制的回调函数
    def on_slider_changed(self, value):
        """滑动条值改变时更新输入框"""
        self.dimming_input.setText(str(value))
        print(f"Dimming 值改变为: {value}")
        # TODO: 实现 Dimming 功能
        
    def on_input_changed(self, text):
        """输入框值改变时更新滑动条"""
        try:
            value = int(text)
            if 0 <= value <= 90:
                self.dimming_slider.setValue(value)
                print(f"Dimming 值改变为: {value}")
        except ValueError:
            pass  # 忽略非数字输入
        # TODO: 实现 Dimming 功能
        
    # 第4行按钮的回调函数
    def on_preview_auto(self):
        print("预览自动模板 - 功能待实现")
        # TODO: 实现预览自动模板功能
        
    def on_auto_draw(self):
        print("全自动绘制 - 功能待实现")
        # TODO: 实现全自动绘制功能

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

这个框架提供了：

1. **第1行**：两个按钮 - "框选绘制区" 和 "框选颜色区"
2. **第2行**：三个按钮 - "读取剪贴板模板"、"预览模板" 和 "指定绘制"
3. **第3行**：Dimming 控制 - 包含标签、滑动条（0-90范围）和联动的输入框
4. **第4行**：两个按钮 - "预览自动模板" 和 "全自动绘制"

**主要特性**：
- 滑动条和输入框实现双向联动
- 所有按钮都已连接到对应的回调函数
- 布局整齐，使用弹性空间使界面美观
- 后端逻辑留空，标注了 `TODO` 注释方便后续实现
- 控制台输出帮助调试功能触发

运行这个程序会显示一个包含所有要求控件的窗口，各个功能的具体实现可以在对应的回调函数中添加。

---
## 🧑‍💻 User

最底下添加2行
1. 一个0~100的进度条
2. 一个通过函数可以改变内容的文字

---
## 🤖 Assistant

以下是修改后的代码，在底部添加了进度条和可变文字：

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QSlider, 
    QLineEdit, QSpacerItem, QSizePolicy, QProgressBar
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("绘制工具")
        self.setMinimumSize(600, 350)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 第1行：框选按钮
        row1_layout = QHBoxLayout()
        
        btn_select_draw_area = QPushButton("框选绘制区")
        btn_select_color_area = QPushButton("框选颜色区")
        
        btn_select_draw_area.clicked.connect(self.on_select_draw_area)
        btn_select_color_area.clicked.connect(self.on_select_color_area)
        
        row1_layout.addWidget(btn_select_draw_area)
        row1_layout.addWidget(btn_select_color_area)
        row1_layout.addStretch()  # 添加弹性空间
        
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
        self.dimming_slider = QSlider(Qt.Horizontal)
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
        
    # 进度条控制函数
    def set_progress(self, value):
        """设置进度条值 (0-100)"""
        if 0 <= value <= 100:
            self.progress_bar.setValue(value)
            print(f"进度更新为: {value}%")
        
    def get_progress(self):
        """获取当前进度值"""
        return self.progress_bar.value()
    
    # 状态文字控制函数
    def set_status_text(self, text):
        """更改状态文字内容"""
        self.status_label.setText(text)
        print(f"状态文字更新为: {text}")
        
    def get_status_text(self):
        """获取当前状态文字"""
        return self.status_label.text()
        
    # 第1行按钮的回调函数
    def on_select_draw_area(self):
        print("框选绘制区 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在框选绘制区域...")
        self.set_progress(10)
        # TODO: 实现框选绘制区功能
        
    def on_select_color_area(self):
        print("框选颜色区 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在框选颜色区域...")
        self.set_progress(20)
        # TODO: 实现框选颜色区功能
        
    # 第2行按钮的回调函数
    def on_read_clipboard(self):
        print("读取剪贴板模板 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在读取剪贴板模板...")
        self.set_progress(30)
        # TODO: 实现读取剪贴板模板功能
        
    def on_preview_template(self):
        print("预览模板 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在预览模板...")
        self.set_progress(40)
        # TODO: 实现预览模板功能
        
    def on_specified_draw(self):
        print("指定绘制 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在执行指定绘制...")
        self.set_progress(50)
        # TODO: 实现指定绘制功能
        
    # 第3行 Dimming 控制的回调函数
    def on_slider_changed(self, value):
        """滑动条值改变时更新输入框"""
        self.dimming_input.setText(str(value))
        print(f"Dimming 值改变为: {value}")
        # 示例：更新状态
        self.set_status_text(f"Dimming 设置为 {value}")
        # TODO: 实现 Dimming 功能
        
    def on_input_changed(self, text):
        """输入框值改变时更新滑动条"""
        try:
            value = int(text)
            if 0 <= value <= 90:
                self.dimming_slider.setValue(value)
                print(f"Dimming 值改变为: {value}")
                # 示例：更新状态
                self.set_status_text(f"Dimming 设置为 {value}")
        except ValueError:
            pass  # 忽略非数字输入
        # TODO: 实现 Dimming 功能
        
    # 第4行按钮的回调函数
    def on_preview_auto(self):
        print("预览自动模板 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在预览自动模板...")
        self.set_progress(70)
        # TODO: 实现预览自动模板功能
        
    def on_auto_draw(self):
        print("全自动绘制 - 功能待实现")
        # 示例：更新状态和进度
        self.set_status_text("正在执行全自动绘制...")
        self.set_progress(100)
        # TODO: 实现全自动绘制功能

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**新增功能**：

**第5行 - 进度条**：
- `QProgressBar`: 范围 0-100
- `set_progress(value)`: 设置进度值的函数
- `get_progress()`: 获取当前进度值的函数
- 显示百分比文本

**第6行 - 状态文字**：
- `QLabel`: 显示状态信息
- `set_status_text(text)`: 改变文字内容的函数
- `get_status_text()`: 获取当前文字内容的函数
- 添加了样式使文字更突出

**示例使用**：
在各个按钮的回调函数中添加了示例代码，展示如何使用这些新功能：
- 点击不同按钮会更新状态文字和进度条
- Dimming 滑动条改变时也会更新状态文字

**主要控制函数**：
```python
# 控制进度条
window.set_progress(50)  # 设置进度为50%
current_progress = window.get_progress()

# 控制状态文字
window.set_status_text("正在处理...")  # 更改文字
current_status = window.get_status_text()
```

---
## 🧑‍💻 User

给出一段代码，传入PIL.Image的图像，弹出一个预览框，允许通过滚轮放大缩小，通过鼠标左键拖动可以框选某个区域，右下角提供重置和确认按钮，按下重置键可以重新框选，按下确认键返回这个框选区的数据

---
## 🤖 Assistant

以下是一个基于PySide6的图像预览和区域选择对话框：

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QRect, Signal, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QWheelEvent, QMouseEvent
from PIL import Image
import numpy as np

class ImagePreviewWidget(QLabel):
    """图像预览和选择控件"""
    
    def __init__(self, pil_image):
        super().__init__()
        self.original_pil_image = pil_image
        self.scale_factor = 1.0
        self.selection_rect = QRect()
        self.selecting = False
        self.start_point = QPoint()
        
        # 设置控件属性
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("border: 1px solid gray;")
        
        # 转换PIL图像为QPixmap
        self.original_pixmap = self.pil_to_qpixmap(pil_image)
        self.update_display()
        
    def pil_to_qpixmap(self, pil_image):
        """将PIL图像转换为QPixmap"""
        # 确保图像是RGB格式
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(pil_image)
        height, width, channel = img_array.shape
        bytes_per_line = 3 * width
        
        # 创建QPixmap
        from PySide6.QtGui import QImage
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)
    
    def update_display(self):
        """更新显示的图像"""
        # 缩放图像
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 如果有选择区域，绘制选择框
        if not self.selection_rect.isEmpty():
            scaled_pixmap = self.draw_selection_on_pixmap(scaled_pixmap)
        
        self.setPixmap(scaled_pixmap)
    
    def draw_selection_on_pixmap(self, pixmap):
        """在pixmap上绘制选择框"""
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
        
        # 计算缩放后的选择区域
        scaled_rect = QRect(
            int(self.selection_rect.x() * self.scale_factor),
            int(self.selection_rect.y() * self.scale_factor),
            int(self.selection_rect.width() * self.scale_factor),
            int(self.selection_rect.height() * self.scale_factor)
        )
        
        painter.drawRect(scaled_rect)
        painter.end()
        return pixmap
    
    def wheelEvent(self, event: QWheelEvent):
        """鼠标滚轮事件 - 缩放"""
        # 获取滚轮滚动方向
        delta = event.angleDelta().y()
        
        # 计算缩放因子
        scale_in = 1.15
        scale_out = 1 / scale_in
        
        if delta > 0:
            # 放大
            self.scale_factor *= scale_in
        else:
            # 缩小
            self.scale_factor *= scale_out
        
        # 限制缩放范围
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
        
        self.update_display()
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.selecting = True
            self.start_point = self.map_to_original_coords(event.position().toPoint())
            self.selection_rect = QRect()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if self.selecting:
            current_point = self.map_to_original_coords(event.position().toPoint())
            
            # 创建选择矩形
            self.selection_rect = QRect(
                min(self.start_point.x(), current_point.x()),
                min(self.start_point.y(), current_point.y()),
                abs(current_point.x() - self.start_point.x()),
                abs(current_point.y() - self.start_point.y())
            )
            
            # 确保选择区域在图像范围内
            img_rect = QRect(0, 0, self.original_pixmap.width(), self.original_pixmap.height())
            self.selection_rect = self.selection_rect.intersected(img_rect)
            
            self.update_display()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.selecting = False
    
    def map_to_original_coords(self, widget_point):
        """将控件坐标映射到原始图像坐标"""
        # 获取当前显示的pixmap尺寸
        current_pixmap = self.pixmap()
        if current_pixmap is None:
            return QPoint(0, 0)
        
        # 计算pixmap在控件中的位置（考虑居中对齐）
        widget_size = self.size()
        pixmap_size = current_pixmap.size()
        
        offset_x = (widget_size.width() - pixmap_size.width()) // 2
        offset_y = (widget_size.height() - pixmap_size.height()) // 2
        
        # 调整坐标
        adjusted_x = widget_point.x() - offset_x
        adjusted_y = widget_point.y() - offset_y
        
        # 映射到原始图像坐标
        original_x = int(adjusted_x / self.scale_factor)
        original_y = int(adjusted_y / self.scale_factor)
        
        return QPoint(original_x, original_y)
    
    def reset_selection(self):
        """重置选择"""
        self.selection_rect = QRect()
        self.update_display()
    
    def get_selection_data(self):
        """获取选择区域的数据"""
        if self.selection_rect.isEmpty():
            return None
        
        # 从PIL图像中裁剪选择区域
        left = self.selection_rect.x()
        top = self.selection_rect.y()
        right = left + self.selection_rect.width()
        bottom = top + self.selection_rect.height()
        
        # 确保坐标在有效范围内
        left = max(0, left)
        top = max(0, top)
        right = min(self.original_pil_image.width, right)
        bottom = min(self.original_pil_image.height, bottom)
        
        if left >= right or top >= bottom:
            return None
        
        # 裁剪图像
        cropped_image = self.original_pil_image.crop((left, top, right, bottom))
        
        return {
            'image': cropped_image,
            'coordinates': (left, top, right, bottom),
            'size': (right - left, bottom - top)
        }


class ImagePreviewDialog(QDialog):
    """图像预览对话框"""
    
    def __init__(self, pil_image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像预览和区域选择")
        self.setModal(True)
        self.resize(800, 600)
        
        self.selection_data = None
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        
        # 创建图像预览控件
        self.preview_widget = ImagePreviewWidget(pil_image)
        scroll_area.setWidget(self.preview_widget)
        
        layout.addWidget(scroll_area)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # 左侧弹性空间，使按钮靠右
        
        # 重置按钮
        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.on_reset)
        
        # 确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.on_confirm)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.confirm_button)
        
        layout.addLayout(button_layout)
        
        # 添加使用说明
        info_label = QLabel("使用说明：滚轮缩放，鼠标左键拖动选择区域")
        info_label.setStyleSheet("color: gray; font-size: 12px;")
        layout.addWidget(info_label)
    
    def on_reset(self):
        """重置选择"""
        self.preview_widget.reset_selection()
    
    def on_confirm(self):
        """确认选择"""
        self.selection_data = self.preview_widget.get_selection_data()
        if self.selection_data is None:
            # 如果没有选择区域，可以提示用户
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "请先选择一个区域")
            return
        
        self.accept()  # 关闭对话框并返回接受状态
    
    def get_selection_data(self):
        """获取选择区域数据"""
        return self.selection_data


def show_image_preview_dialog(pil_image, parent=None):
    """
    显示图像预览对话框的便捷函数
    
    Args:
        pil_image: PIL.Image 对象
        parent: 父窗口
    
    Returns:
        dict or None: 选择区域的数据，包含 'image', 'coordinates', 'size'
                     如果用户取消或没有选择区域，返回 None
    """
    dialog = ImagePreviewDialog(pil_image, parent)
    
    if dialog.exec() == QDialog.Accepted:
        return dialog.get_selection_data()
    else:
        return None


# 示例用法
def main():
    app = QApplication(sys.argv)
    
    # 创建示例图像
    try:
        # 尝试加载一个图像文件
        pil_image = Image.open("test_image.jpg")  # 替换为实际的图像路径
    except:
        # 如果没有图像文件，创建一个示例图像
        pil_image = Image.new('RGB', (800, 600), color=(100, 150, 200))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(pil_image)
        draw.rectangle([50, 50, 200, 150], fill=(255, 0, 0))
        draw.rectangle([300, 200, 500, 400], fill=(0, 255, 0))
        draw.text((250, 50), "示例图像", fill=(255, 255, 255))
    
    # 显示预览对话框
    result = show_image_preview_dialog(pil_image)
    
    if result:
        print("选择区域信息:")
        print(f"坐标: {result['coordinates']}")
        print(f"尺寸: {result['size']}")
        print(f"裁剪图像尺寸: {result['image'].size}")
        
        # 可以保存裁剪的图像
        result['image'].save("selected_region.png")
        print("选择区域已保存为 selected_region.png")
    else:
        print("用户取消了选择")

if __name__ == "__main__":
    main()
```

**主要功能**：

1. **图像显示**：
 - 将PIL图像转换为QPixmap显示
 - 居中对齐显示

2. **缩放功能**：
 - 鼠标滚轮放大缩小（范围0.1x到5x）
 - 平滑缩放效果

3. **区域选择**：
 - 鼠标左键拖动框选区域
 - 红色虚线框显示选择区域
 - 实时更新选择框

4. **控制按钮**：
 - **重置**：清除当前选择，重新框选
 - **确认**：返回选择区域数据

5. **返回数据**：
```python
   {
       'image': PIL.Image,           # 裁剪后的PIL图像
       'coordinates': (x1, y1, x2, y2),  # 选择区域坐标
       'size': (width, height)       # 选择区域尺寸
   }
   ```

**使用方法**：

```python
from PIL import Image

# 加载图像
pil_image = Image.open("your_image.jpg")

# 显示预览对话框
result = show_image_preview_dialog(pil_image)

if result:
 selected_image = result['image']
 coordinates = result['coordinates']
 size = result['size']

 # 处理选择的区域...
```

**特点**：
- 支持各种PIL图像格式
- 响应式界面，自动处理坐标映射
- 边界检查，确保选择区域在图像范围内
- 用户友好的交互体验

---
## 🧑‍💻 User

如何将这个框选器嵌入到之前提到的框架的某个按钮里

---
## 🤖 Assistant

以下是将图像框选器嵌入到之前框架中的完整代码：

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QSlider, 
    QLineEdit, QSpacerItem, QSizePolicy, QProgressBar,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PIL import Image

# 这里需要包含之前的图像预览器代码
from PySide6.QtWidgets import QDialog, QScrollArea
from PySide6.QtCore import QRect, Signal, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QWheelEvent, QMouseEvent
import numpy as np

class ImagePreviewWidget(QLabel):
    """图像预览和选择控件"""
    
    def __init__(self, pil_image):
        super().__init__()
        self.original_pil_image = pil_image
        self.scale_factor = 1.0
        self.selection_rect = QRect()
        self.selecting = False
        self.start_point = QPoint()
        
        # 设置控件属性
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("border: 1px solid gray;")
        
        # 转换PIL图像为QPixmap
        self.original_pixmap = self.pil_to_qpixmap(pil_image)
        self.update_display()
        
    def pil_to_qpixmap(self, pil_image):
        """将PIL图像转换为QPixmap"""
        # 确保图像是RGB格式
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(pil_image)
        height, width, channel = img_array.shape
        bytes_per_line = 3 * width
        
        # 创建QPixmap
        from PySide6.QtGui import QImage
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)
    
    def update_display(self):
        """更新显示的图像"""
        # 缩放图像
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 如果有选择区域，绘制选择框
        if not self.selection_rect.isEmpty():
            scaled_pixmap = self.draw_selection_on_pixmap(scaled_pixmap)
        
        self.setPixmap(scaled_pixmap)
    
    def draw_selection_on_pixmap(self, pixmap):
        """在pixmap上绘制选择框"""
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
        
        # 计算缩放后的选择区域
        scaled_rect = QRect(
            int(self.selection_rect.x() * self.scale_factor),
            int(self.selection_rect.y() * self.scale_factor),
            int(self.selection_rect.width() * self.scale_factor),
            int(self.selection_rect.height() * self.scale_factor)
        )
        
        painter.drawRect(scaled_rect)
        painter.end()
        return pixmap
    
    def wheelEvent(self, event: QWheelEvent):
        """鼠标滚轮事件 - 缩放"""
        # 获取滚轮滚动方向
        delta = event.angleDelta().y()
        
        # 计算缩放因子
        scale_in = 1.15
        scale_out = 1 / scale_in
        
        if delta > 0:
            # 放大
            self.scale_factor *= scale_in
        else:
            # 缩小
            self.scale_factor *= scale_out
        
        # 限制缩放范围
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
        
        self.update_display()
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.selecting = True
            self.start_point = self.map_to_original_coords(event.position().toPoint())
            self.selection_rect = QRect()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if self.selecting:
            current_point = self.map_to_original_coords(event.position().toPoint())
            
            # 创建选择矩形
            self.selection_rect = QRect(
                min(self.start_point.x(), current_point.x()),
                min(self.start_point.y(), current_point.y()),
                abs(current_point.x() - self.start_point.x()),
                abs(current_point.y() - self.start_point.y())
            )
            
            # 确保选择区域在图像范围内
            img_rect = QRect(0, 0, self.original_pixmap.width(), self.original_pixmap.height())
            self.selection_rect = self.selection_rect.intersected(img_rect)
            
            self.update_display()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.selecting = False
    
    def map_to_original_coords(self, widget_point):
        """将控件坐标映射到原始图像坐标"""
        # 获取当前显示的pixmap尺寸
        current_pixmap = self.pixmap()
        if current_pixmap is None:
            return QPoint(0, 0)
        
        # 计算pixmap在控件中的位置（考虑居中对齐）
        widget_size = self.size()
        pixmap_size = current_pixmap.size()
        
        offset_x = (widget_size.width() - pixmap_size.width()) // 2
        offset_y = (widget_size.height() - pixmap_size.height()) // 2
        
        # 调整坐标
        adjusted_x = widget_point.x() - offset_x
        adjusted_y = widget_point.y() - offset_y
        
        # 映射到原始图像坐标
        original_x = int(adjusted_x / self.scale_factor)
        original_y = int(adjusted_y / self.scale_factor)
        
        return QPoint(original_x, original_y)
    
    def reset_selection(self):
        """重置选择"""
        self.selection_rect = QRect()
        self.update_display()
    
    def get_selection_data(self):
        """获取选择区域的数据"""
        if self.selection_rect.isEmpty():
            return None
        
        # 从PIL图像中裁剪选择区域
        left = self.selection_rect.x()
        top = self.selection_rect.y()
        right = left + self.selection_rect.width()
        bottom = top + self.selection_rect.height()
        
        # 确保坐标在有效范围内
        left = max(0, left)
        top = max(0, top)
        right = min(self.original_pil_image.width, right)
        bottom = min(self.original_pil_image.height, bottom)
        
        if left >= right or top >= bottom:
            return None
        
        # 裁剪图像
        cropped_image = self.original_pil_image.crop((left, top, right, bottom))
        
        return {
            'image': cropped_image,
            'coordinates': (left, top, right, bottom),
            'size': (right - left, bottom - top)
        }


class ImagePreviewDialog(QDialog):
    """图像预览对话框"""
    
    def __init__(self, pil_image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像预览和区域选择")
        self.setModal(True)
        self.resize(800, 600)
        
        self.selection_data = None
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        
        # 创建图像预览控件
        self.preview_widget = ImagePreviewWidget(pil_image)
        scroll_area.setWidget(self.preview_widget)
        
        layout.addWidget(scroll_area)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # 左侧弹性空间，使按钮靠右
        
        # 重置按钮
        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.on_reset)
        
        # 确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.on_confirm)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.confirm_button)
        
        layout.addLayout(button_layout)
        
        # 添加使用说明
        info_label = QLabel("使用说明：滚轮缩放，鼠标左键拖动选择区域")
        info_label.setStyleSheet("color: gray; font-size: 12px;")
        layout.addWidget(info_label)
    
    def on_reset(self):
        """重置选择"""
        self.preview_widget.reset_selection()
    
    def on_confirm(self):
        """确认选择"""
        self.selection_data = self.preview_widget.get_selection_data()
        if self.selection_data is None:
            QMessageBox.warning(self, "警告", "请先选择一个区域")
            return
        
        self.accept()  # 关闭对话框并返回接受状态
    
    def get_selection_data(self):
        """获取选择区域数据"""
        return self.selection_data


def show_image_preview_dialog(pil_image, parent=None):
    """
    显示图像预览对话框的便捷函数
    """
    dialog = ImagePreviewDialog(pil_image, parent)
    
    if dialog.exec() == QDialog.Accepted:
        return dialog.get_selection_data()
    else:
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.dimming_slider = QSlider(Qt.Horizontal)
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
        
    def load_image_file(self):
        """加载图像文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图像文件",
            "",
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path:
            try:
                pil_image = Image.open(file_path)
                return pil_image
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载图像文件：{str(e)}")
                return None
        return None
    
    # 框选区域的回调函数
    def on_select_draw_area(self):
        """框选绘制区域"""
        self.set_status_text("请选择要加载的图像文件...")
        
        # 加载图像文件
        pil_image = self.load_image_file()
        if pil_image is None:
            self.set_status_text("取消选择图像文件")
            return
        
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
            
            # 可选：保存选择的区域图像
            result['image'].save("selected_draw_area.png")
            print(f"绘制区域保存为: selected_draw_area.png")
            print(f"坐标: {result['coordinates']}")
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
            
            # 可选：保存选择的区域图像
            result['image'].save("selected_color_area.png")
            print(f"颜色区域保存为: selected_color_area.png")
            print(f"坐标: {result['coordinates']}")
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
    def set_status_text(self, text):
        """更改状态文字内容"""
        self.status_label.setText(text)
    
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
        print("读取剪贴板模板 - 功能待实现")
        self.set_status_text("正在读取剪贴板模板...")
        self.set_progress(40)
        
    def on_preview_template(self):
        print("预览模板 - 功能待实现")
        # 检查是否已选择区域
        if self.draw_area_data:
            print(f"可以使用绘制区域数据: {self.draw_area_data['coordinates']}")
        if self.color_area_data:
            print(f"可以使用颜色区域数据: {self.color_area_data['coordinates']}")
        self.set_status_text("正在预览模板...")
        self.set_progress(50)
        
    def on_specified_draw(self):
        print("指定绘制 - 功能待实现")
        self.set_status_text("正在执行指定绘制...")
        self.set_progress(60)
        
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
        print("预览自动模板 - 功能待实现")
        self.set_status_text("正在预览自动模板...")
        self.set_progress(80)
        
    def on_auto_draw(self):
        print("全自动绘制 - 功能待实现")
        self.set_status_text("正在执行全自动绘制...")
        self.set_progress(100)


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**主要变化和集成功能**：

1. **集成图像选择器**：
 - 在`on_select_draw_area()`和`on_select_color_area()`中集成了图像预览对话框
 - 首先弹出文件选择对话框加载图像，然后打开框选器

2. **数据存储**：
 - 添加了`self.draw_area_data`和`self.color_area_data`存储选择的区域数据
 - 提供`get_draw_area_data()`和`get_color_area_data()`方法供其他功能使用

3. **用户反馈**：
 - 更新状态文字显示当前操作
 - 更新进度条显示操作进度
 - 按钮文字动态显示选择的区域尺寸

4. **文件处理**：
 - 支持多种图像格式（PNG、JPG、JPEG、BMP、GIF、TIFF）
 - 自动保存选择的区域为独立图像文件
 - 错误处理和用户提示

**使用流程**：
1. 点击"框选绘制区"或"框选颜色区"按钮
2. 在文件对话框中选择图像文件
3. 在预览对话框中使用鼠标框选区域
4. 点击"确认"保存选择，或"重置"重新选择
5. 选择的区域数据被存储，可供其他功能使用

**数据访问示例**：
```python
# 在其他方法中访问选择的数据
if self.draw_area_data:
    selected_image = self.draw_area_data['image']
    coordinates = self.draw_area_data['coordinates']
    size = self.draw_area_data['size']
```

---
## 🧑‍💻 User

告诉我核心修改是哪些

---
## 🤖 Assistant

核心修改的部分主要有以下几个：

## 1. **导入图像预览器类**
```python
# 需要将之前的ImagePreviewWidget、ImagePreviewDialog等类复制到主文件中
# 或者作为独立模块导入
```

## 2. **MainWindow类中添加数据存储属性**
```python
class MainWindow(QMainWindow):
    def __init__(self):
        # ... 其他初始化代码 ...
        
        # 核心添加：存储选择的区域数据
        self.draw_area_data = None
        self.color_area_data = None
```

## 3. **添加文件加载方法**
```python
def load_image_file(self):
    """加载图像文件"""
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        "选择图像文件",
        "",
        "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
    )
    
    if file_path:
        try:
            pil_image = Image.open(file_path)
            return pil_image
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法加载图像文件：{str(e)}")
            return None
    return None
```

## 4. **核心：修改框选按钮的回调函数**
```python
def on_select_draw_area(self):
    """框选绘制区域"""
    # 1. 加载图像文件
    pil_image = self.load_image_file()
    if pil_image is None:
        return
    
    # 2. 显示框选对话框
    result = show_image_preview_dialog(pil_image, self)
    
    # 3. 处理结果
    if result:
        self.draw_area_data = result  # 核心：保存选择数据
        self.btn_select_draw_area.setText(f"绘制区({result['size'][0]}x{result['size'][1]})")
        # 更新状态...

def on_select_color_area(self):
    """框选颜色区域"""
    # 类似的实现，保存到 self.color_area_data
```

## 5. **添加数据访问方法**
```python
def get_draw_area_data(self):
    """获取绘制区域数据"""
    return self.draw_area_data

def get_color_area_data(self):
    """获取颜色区域数据"""
    return self.color_area_data
```

## 核心逻辑总结：

**原来的按钮回调**：
```python
def on_select_draw_area(self):
    print("框选绘制区 - 功能待实现")
    # TODO: 实现框选绘制区功能
```

**修改后的按钮回调**：
```python
def on_select_draw_area(self):
    # 1. 加载图像 → 2. 调用框选器 → 3. 保存结果 → 4. 更新UI
    pil_image = self.load_image_file()
    if pil_image:
        result = show_image_preview_dialog(pil_image, self)
        if result:
            self.draw_area_data = result  # 关键：数据保存
            # 更新按钮文字、状态等...
```

**最关键的就是**：
- 将空的回调函数改为调用`show_image_preview_dialog()`
- 将返回的选择数据存储在实例变量中
- 更新UI反馈给用户

其他代码都是辅助功能（文件对话框、状态更新、错误处理等）。

---
## 🧑‍💻 User

重构预览控件，添加一个按住右键拖拽时移动图像位置的功能，方便更好的预览

---
## 🤖 Assistant

以下是重构后的预览控件，添加了右键拖拽移动功能：

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QRect, Signal, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QWheelEvent, QMouseEvent, QCursor
from PIL import Image
import numpy as np

class ImagePreviewWidget(QLabel):
    """图像预览和选择控件 - 支持右键拖拽移动"""
    
    def __init__(self, pil_image):
        super().__init__()
        self.original_pil_image = pil_image
        self.scale_factor = 1.0
        self.selection_rect = QRect()
        
        # 选择相关状态
        self.selecting = False
        self.selection_start_point = QPoint()
        
        # 拖拽移动相关状态
        self.panning = False
        self.pan_start_point = QPoint()
        self.image_offset = QPoint(0, 0)  # 图像偏移量
        
        # 设置控件属性
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        
        # 转换PIL图像为QPixmap
        self.original_pixmap = self.pil_to_qpixmap(pil_image)
        self.update_display()
        
    def pil_to_qpixmap(self, pil_image):
        """将PIL图像转换为QPixmap"""
        # 确保图像是RGB格式
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(pil_image)
        height, width, channel = img_array.shape
        bytes_per_line = 3 * width
        
        # 创建QPixmap
        from PySide6.QtGui import QImage
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)
    
    def update_display(self):
        """更新显示的图像"""
        # 缩放图像
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 创建显示用的pixmap，考虑偏移
        display_pixmap = self.create_display_pixmap(scaled_pixmap)
        
        # 如果有选择区域，绘制选择框
        if not self.selection_rect.isEmpty():
            display_pixmap = self.draw_selection_on_pixmap(display_pixmap, scaled_pixmap.size())
        
        self.setPixmap(display_pixmap)
    
    def create_display_pixmap(self, scaled_pixmap):
        """创建带偏移的显示pixmap"""
        widget_size = self.size()
        
        # 创建与控件大小相同的空白pixmap
        display_pixmap = QPixmap(widget_size)
        display_pixmap.fill(QColor(240, 240, 240))  # 背景色
        
        # 计算图像在控件中的位置（考虑偏移）
        image_pos = self.calculate_image_position(scaled_pixmap.size())
        
        # 绘制图像到显示pixmap上
        painter = QPainter(display_pixmap)
        painter.drawPixmap(image_pos, scaled_pixmap)
        painter.end()
        
        return display_pixmap
    
    def calculate_image_position(self, image_size):
        """计算图像在控件中的位置"""
        widget_size = self.size()
        
        # 基础居中位置
        center_x = (widget_size.width() - image_size.width()) // 2
        center_y = (widget_size.height() - image_size.height()) // 2
        
        # 加上偏移
        final_x = center_x + self.image_offset.x()
        final_y = center_y + self.image_offset.y()
        
        return QPoint(final_x, final_y)
    
    def draw_selection_on_pixmap(self, display_pixmap, scaled_image_size):
        """在显示pixmap上绘制选择框"""
        if self.selection_rect.isEmpty():
            return display_pixmap
            
        painter = QPainter(display_pixmap)
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
        
        # 计算选择区域在显示pixmap中的位置
        image_pos = self.calculate_image_position(scaled_image_size)
        
        scaled_rect = QRect(
            int(self.selection_rect.x() * self.scale_factor) + image_pos.x(),
            int(self.selection_rect.y() * self.scale_factor) + image_pos.y(),
            int(self.selection_rect.width() * self.scale_factor),
            int(self.selection_rect.height() * self.scale_factor)
        )
        
        painter.drawRect(scaled_rect)
        painter.end()
        return display_pixmap
    
    def wheelEvent(self, event: QWheelEvent):
        """鼠标滚轮事件 - 缩放"""
        # 获取滚轮滚动方向
        delta = event.angleDelta().y()
        
        # 计算缩放因子
        scale_in = 1.15
        scale_out = 1 / scale_in
        
        old_scale = self.scale_factor
        
        if delta > 0:
            # 放大
            self.scale_factor *= scale_in
        else:
            # 缩小
            self.scale_factor *= scale_out
        
        # 限制缩放范围
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
        
        # 如果缩放发生变化，调整偏移以保持鼠标位置为中心
        if self.scale_factor != old_scale:
            self.adjust_offset_for_zoom(event.position().toPoint(), old_scale)
        
        self.update_display()
    
    def adjust_offset_for_zoom(self, mouse_pos, old_scale):
        """调整偏移以保持缩放中心"""
        # 计算缩放比例变化
        scale_ratio = self.scale_factor / old_scale
        
        # 获取当前图像位置
        widget_size = self.size()
        old_image_size = self.original_pixmap.size() * old_scale
        old_image_pos = self.calculate_image_position(old_image_size)
        
        # 计算鼠标相对于图像的位置
        relative_mouse_x = mouse_pos.x() - old_image_pos.x()
        relative_mouse_y = mouse_pos.y() - old_image_pos.y()
        
        # 计算新的偏移
        new_relative_x = relative_mouse_x * scale_ratio
        new_relative_y = relative_mouse_y * scale_ratio
        
        offset_adjust_x = relative_mouse_x - new_relative_x
        offset_adjust_y = relative_mouse_y - new_relative_y
        
        self.image_offset.setX(self.image_offset.x() + int(offset_adjust_x))
        self.image_offset.setY(self.image_offset.y() + int(offset_adjust_y))
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            # 左键开始选择
            original_pos = self.map_to_original_coords(event.position().toPoint())
            if original_pos is not None:
                self.selecting = True
                self.selection_start_point = original_pos
                self.selection_rect = QRect()
                
        elif event.button() == Qt.RightButton:
            # 右键开始拖拽
            self.panning = True
            self.pan_start_point = event.position().toPoint()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if self.selecting and event.buttons() & Qt.LeftButton:
            # 左键拖拽选择
            current_pos = self.map_to_original_coords(event.position().toPoint())
            if current_pos is not None:
                # 创建选择矩形
                self.selection_rect = QRect(
                    min(self.selection_start_point.x(), current_pos.x()),
                    min(self.selection_start_point.y(), current_pos.y()),
                    abs(current_pos.x() - self.selection_start_point.x()),
                    abs(current_pos.y() - self.selection_start_point.y())
                )
                
                # 确保选择区域在图像范围内
                img_rect = QRect(0, 0, self.original_pixmap.width(), self.original_pixmap.height())
                self.selection_rect = self.selection_rect.intersected(img_rect)
                
                self.update_display()
                
        elif self.panning and event.buttons() & Qt.RightButton:
            # 右键拖拽移动
            current_pos = event.position().toPoint()
            delta = current_pos - self.pan_start_point
            
            self.image_offset += delta
            self.pan_start_point = current_pos
            
            self.update_display()
        else:
            # 鼠标悬停时更新光标样式
            if self.is_mouse_over_image(event.position().toPoint()):
                if not self.selecting and not self.panning:
                    self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.selecting = False
        elif event.button() == Qt.RightButton:
            self.panning = False
            self.setCursor(QCursor(Qt.ArrowCursor))
    
    def is_mouse_over_image(self, mouse_pos):
        """检查鼠标是否在图像区域内"""
        scaled_size = self.original_pixmap.size() * self.scale_factor
        image_pos = self.calculate_image_position(scaled_size)
        image_rect = QRect(image_pos, scaled_size)
        return image_rect.contains(mouse_pos)
    
    def map_to_original_coords(self, widget_point):
        """将控件坐标映射到原始图像坐标"""
        # 计算当前缩放图像的尺寸和位置
        scaled_size = self.original_pixmap.size() * self.scale_factor
        image_pos = self.calculate_image_position(scaled_size)
        
        # 检查点击是否在图像区域内
        image_rect = QRect(image_pos, scaled_size)
        if not image_rect.contains(widget_point):
            return None
        
        # 计算相对于图像的坐标
        relative_x = widget_point.x() - image_pos.x()
        relative_y = widget_point.y() - image_pos.y()
        
        # 映射到原始图像坐标
        original_x = int(relative_x / self.scale_factor)
        original_y = int(relative_y / self.scale_factor)
        
        # 确保坐标在有效范围内
        original_x = max(0, min(original_x, self.original_pixmap.width() - 1))
        original_y = max(0, min(original_y, self.original_pixmap.height() - 1))
        
        return QPoint(original_x, original_y)
    
    def reset_view(self):
        """重置视图（缩放和偏移）"""
        self.scale_factor = 1.0
        self.image_offset = QPoint(0, 0)
        self.update_display()
    
    def reset_selection(self):
        """重置选择"""
        self.selection_rect = QRect()
        self.update_display()
    
    def reset_all(self):
        """重置所有（视图和选择）"""
        self.reset_view()
        self.reset_selection()
    
    def get_selection_data(self):
        """获取选择区域的数据"""
        if self.selection_rect.isEmpty():
            return None
        
        # 从PIL图像中裁剪选择区域
        left = self.selection_rect.x()
        top = self.selection_rect.y()
        right = left + self.selection_rect.width()
        bottom = top + self.selection_rect.height()
        
        # 确保坐标在有效范围内
        left = max(0, left)
        top = max(0, top)
        right = min(self.original_pil_image.width, right)
        bottom = min(self.original_pil_image.height, bottom)
        
        if left >= right or top >= bottom:
            return None
        
        # 裁剪图像
        cropped_image = self.original_pil_image.crop((left, top, right, bottom))
        
        return {
            'image': cropped_image,
            'coordinates': (left, top, right, bottom),
            'size': (right - left, bottom - top)
        }


class ImagePreviewDialog(QDialog):
    """图像预览对话框 - 更新了按钮功能"""
    
    def __init__(self, pil_image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像预览和区域选择")
        self.setModal(True)
        self.resize(900, 700)
        
        self.selection_data = None
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建图像预览控件
        self.preview_widget = ImagePreviewWidget(pil_image)
        layout.addWidget(self.preview_widget)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 重置视图按钮
        self.reset_view_button = QPushButton("重置视图")
        self.reset_view_button.clicked.connect(self.on_reset_view)
        self.reset_view_button.setToolTip("重置缩放和位置到初始状态")
        
        # 重置选择按钮
        self.reset_selection_button = QPushButton("重置选择")
        self.reset_selection_button.clicked.connect(self.on_reset_selection)
        self.reset_selection_button.setToolTip("清除当前选择区域")
        
        button_layout.addWidget(self.reset_view_button)
        button_layout.addWidget(self.reset_selection_button)
        button_layout.addStretch()
        
        # 确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.on_confirm)
        
        button_layout.addWidget(self.confirm_button)
        
        layout.addLayout(button_layout)
        
        # 添加使用说明
        info_label = QLabel(
            "使用说明：滚轮缩放 | 左键拖动选择区域 | 右键拖动移动图像"
        )
        info_label.setStyleSheet("color: gray; font-size: 12px; padding: 5px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
    
    def on_reset_view(self):
        """重置视图"""
        self.preview_widget.reset_view()
    
    def on_reset_selection(self):
        """重置选择"""
        self.preview_widget.reset_selection()
    
    def on_confirm(self):
        """确认选择"""
        self.selection_data = self.preview_widget.get_selection_data()
        if self.selection_data is None:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "请先选择一个区域")
            return
        
        self.accept()
    
    def get_selection_data(self):
        """获取选择区域数据"""
        return self.selection_data


def show_image_preview_dialog(pil_image, parent=None):
    """显示图像预览对话框的便捷函数"""
    dialog = ImagePreviewDialog(pil_image, parent)
    
    if dialog.exec() == QDialog.Accepted:
        return dialog.get_selection_data()
    else:
        return None


# 示例用法
def main():
    app = QApplication(sys.argv)
    
    # 创建示例图像
    try:
        pil_image = Image.open("test_image.jpg")
    except:
        pil_image = Image.new('RGB', (800, 600), color=(100, 150, 200))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(pil_image)
        draw.rectangle([50, 50, 200, 150], fill=(255, 0, 0))
        draw.rectangle([300, 200, 500, 400], fill=(0, 255, 0))
        draw.text((250, 50), "示例图像 - 右键拖拽移动", fill=(255, 255, 255))
    
    result = show_image_preview_dialog(pil_image)
    
    if result:
        print("选择区域信息:")
        print(f"坐标: {result['coordinates']}")
        print(f"尺寸: {result['size']}")
    else:
        print("用户取消了选择")

if __name__ == "__main__":
    main()
```

**主要新增功能**：

1. **右键拖拽移动**：
 - 按住右键拖拽可以移动图像位置
 - 拖拽时光标变为抓手样式
 - 通过`image_offset`跟踪图像偏移量

2. **改进的缩放体验**：
 - 缩放时保持鼠标位置为中心点
 - 支持移动后的缩放

3. **视图控制**：
 - `reset_view()`: 重置缩放和位置
 - `reset_selection()`: 只重置选择区域
 - `reset_all()`: 重置所有状态

4. **增强的用户界面**：
 - 分离的"重置视图"和"重置选择"按钮
 - 更详细的使用说明
 - 工具提示说明按钮功能

5. **改进的坐标映射**：
 - 考虑图像偏移的坐标转换
 - 边界检查确保选择在图像范围内

**操作说明**：
- **滚轮**：缩放图像
- **左键拖拽**：选择区域
- **右键拖拽**：移动图像位置
- **重置视图**：恢复初始缩放和位置
- **重置选择**：清除选择区域

这样用户可以先用右键拖拽找到合适的视图位置，再用左键精确选择需要的区域。

---
## 🧑‍💻 User

（不要给出完整代码，仅说明必要修改）
我在notebook里测试时，关闭了出现的窗口，下次运行报错
RuntimeError: Please destroy the QApplication singleton before creating a new QApplication instance.

---
## 🤖 Assistant

这是因为QApplication单例没有被正确销毁导致的。在notebook环境中需要做以下修改：

## 核心修改点：

### 1. 修改`main()`函数
```python
def main():
    # 检查是否已存在QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        created_new_app = True
    else:
        created_new_app = False
    
    # 你的窗口代码...
    result = show_image_preview_dialog(pil_image)
    
    # 只有当创建了新的app时才调用exec
    if created_new_app:
        sys.exit(app.exec())
    
    return result  # 在notebook中返回结果
```

### 2. 或者更简单的方案 - 修改函数结构
```python
def show_image_preview_dialog(pil_image, parent=None):
    """显示图像预览对话框的便捷函数"""
    # 确保有QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = ImagePreviewDialog(pil_image, parent)
    
    if dialog.exec() == QDialog.Accepted:
        return dialog.get_selection_data()
    else:
        return None

# 在notebook中直接调用，不需要main()
def test_in_notebook():
    from PIL import Image
    pil_image = Image.new('RGB', (400, 300), color=(100, 150, 200))
    result = show_image_preview_dialog(pil_image)
    return result
```

### 3. 在MainWindow集成时的修改
在你的主框架中，按钮回调函数不需要修改，因为主程序已经有QApplication实例了。

**关键点**：
- 不要在notebook中调用`sys.exit(app.exec())`
- 使用`QApplication.instance()`检查现有实例
- 让对话框直接返回结果，而不是通过应用程序事件循环

这样就能在notebook中多次运行而不报错。

---
## 🧑‍💻 User

主框架关闭时提醒：
An exception has occurred, use %tb to see the full traceback.

SystemExit: 0

d:\Software\miniconda3\envs\myenv\Lib\site-packages\IPython\core\interactiveshell.py:3707: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)

有必要修复吗？如果有，给出修改部分（不要给出完整代码

---
## 🤖 Assistant

这个警告不是严重错误，但在notebook环境中确实应该修复。问题是`sys.exit(app.exec())`导致的。

## 核心修改：

### 修改`main()`函数
```python
def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    # 在notebook中不要调用sys.exit
    if hasattr(sys, 'ps1') or 'ipykernel' in sys.modules:
        # 在notebook环境中
        return app.exec()
    else:
        # 在正常Python脚本中
        sys.exit(app.exec())
```

### 或者更简单的方案
```python
def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    # 直接返回执行结果，不调用sys.exit
    return app.exec()
```

### 在notebook中的调用方式
```python
# 在notebook cell中这样调用
if __name__ == "__main__":
    main()  # 不再有sys.exit，只是正常函数返回
```

**关键修改**：
- 移除或条件化`sys.exit()`调用
- 让`main()`函数正常返回而不是系统退出
- 在notebook中，窗口关闭后程序自然结束，不需要强制退出

这样修改后，关闭窗口就不会再有SystemExit警告了。

---
## 🧑‍💻 User

在正常的运行中是不是不需要管这个问题？

---
## 🤖 Assistant

是的，在正常的Python脚本运行中（比如直接运行`.py`文件），**不需要管这个问题**。

这个警告只出现在notebook环境中，因为：

1. **正常脚本运行**：`sys.exit(app.exec())`是标准做法，程序结束时正常退出
2. **Notebook环境**：IPython内核不期望程序调用`sys.exit()`，因为它要保持运行状态供后续cell使用

所以：
- 如果你的代码主要在**正常Python环境**中使用 → **不用修改**
- 如果经常在**Notebook**中测试 → 建议修改避免警告
- 如果**两种环境都用** → 可以用条件判断来处理

最简单的处理方式是保持现有代码不变，**只在notebook测试时忽略这个警告**即可。这个警告不影响功能，只是IPython的一个提醒。
