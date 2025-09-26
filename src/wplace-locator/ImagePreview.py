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
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_image)
    
    def update_display(self):
        """更新显示的图像"""
        # 缩放图像
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
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
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.DashLine))
        
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
    # 确保有QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = ImagePreviewDialog(pil_image, parent)
    
    if dialog.exec() == QDialog.Accepted:
        return dialog.get_selection_data()
    else:
        return None
