import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image
import numpy as np

class ImagePreviewWidget(QLabel):
    """精简版图像预览控件 - 仅显示，自适应窗口"""
    
    def __init__(self, pil_image):
        super().__init__()
        self.original_pil_image = pil_image
        
        # 设置控件属性
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 200)
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
        """更新显示 - 自适应控件尺寸"""
        if self.original_pixmap.isNull():
            return
            
        # 获取控件尺寸
        widget_size = self.size()
        if widget_size.width() <= 0 or widget_size.height() <= 0:
            return
        
        # 缩放图像以适配控件，保持宽高比
        scaled_pixmap = self.original_pixmap.scaled(
            widget_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """窗口大小改变时重新调整图像"""
        super().resizeEvent(event)
        self.update_display()


class ImagePreviewDialog(QDialog):
    """精简版图像预览对话框"""
    
    def __init__(self, pil_image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像预览")
        self.setModal(True)
        self.resize(600, 450)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建图像预览控件
        self.preview_widget = ImagePreviewWidget(pil_image)
        layout.addWidget(self.preview_widget)
        
    def resizeEvent(self, event):
        """窗口大小改变时的处理"""
        super().resizeEvent(event)
        # preview_widget会自动响应大小变化


def show_image_preview(pil_image, parent=None):
    """显示精简版图像预览对话框的便捷函数"""
    # 确保有QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    dialog = ImagePreviewDialog(pil_image, parent)
    dialog.exec()


# 示例用法
def main():
    app = QApplication.instance()
    if app is None:
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
        draw.text((250, 50), "示例图像", fill=(255, 255, 255))
    
    show_image_preview(pil_image)

if __name__ == "__main__":
    main()
