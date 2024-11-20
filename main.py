import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import init_db

def main():
    # 初始化数据库
    init_db()
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 