import sys
from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow

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

if __name__ == "__main__":
    main()
