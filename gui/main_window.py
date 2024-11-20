from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QToolBar, QStatusBar, QSplitter, QMessageBox,
                           QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from database.db_manager import get_db
from database.models import Script
from .script_editor import ScriptEditorWidget
from .execution_panel import ExecutionPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("脚本管理器")
        self.setMinimumSize(1000, 600)
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建主界面
        self.create_main_ui()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 当前脚本ID
        self.current_script_id = None
        
        # 加载脚本列表
        self.load_scripts()
    
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 新建脚本
        new_action = QAction("新建脚本", self)
        new_action.setStatusTip("创建新的Python脚本")
        new_action.triggered.connect(self.new_script)
        toolbar.addAction(new_action)
        
        # 保存脚本
        save_action = QAction("保存", self)
        save_action.setStatusTip("保存当前脚本")
        save_action.triggered.connect(self.save_script)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 运行脚本
        run_action = QAction("运行", self)
        run_action.setStatusTip("运行当前脚本")
        run_action.triggered.connect(self.run_script)
        toolbar.addAction(run_action)
    
    def create_main_ui(self):
        # 创建水平分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建脚本编辑器
        self.editor = ScriptEditorWidget()
        
        # 创建执行面板
        self.execution_panel = ExecutionPanel()
        
        # 添加到分割器
        splitter.addWidget(self.editor)
        splitter.addWidget(self.execution_panel)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        self.layout.addWidget(splitter)
    
    def new_script(self):
        name, ok = QInputDialog.getText(self, "新建脚本", "请输入脚本名称：")
        if ok and name:
            try:
                db = next(get_db())
                script = Script(
                    name=name,
                    content="# 在这里编写Python代码\n",
                    type="python"
                )
                db.add(script)
                db.commit()
                
                self.current_script_id = script.id
                self.editor.set_content(script.content)
                self.statusBar.showMessage(f"创建脚本：{name}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建脚本失败：{str(e)}")
    
    def save_script(self):
        if not self.current_script_id:
            QMessageBox.warning(self, "警告", "请先创建或选择一个脚本")
            return
        
        try:
            db = next(get_db())
            script = db.query(Script).get(self.current_script_id)
            if script:
                script.content = self.editor.get_content()
                db.commit()
                self.statusBar.showMessage("脚本已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存脚本失败：{str(e)}")
    
    def run_script(self):
        if not self.current_script_id:
            QMessageBox.warning(self, "警告", "请先创建或选择一个脚本")
            return
        
        content = self.editor.get_content()
        self.execution_panel.run_script(content)
    
    def load_scripts(self):
        """
        Load scripts from the configured directory
        """
        # Add your script loading logic here
        pass  # Temporary placeholder - replace with actual implementation 