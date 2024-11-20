from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QToolBar, QStatusBar, QSplitter, QMessageBox,
                           QInputDialog, QListWidget, QListWidgetItem, QMenu,
                           QMenuBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from database.db_manager import get_db
from database.models import Script
from .script_editor import ScriptEditorWidget
from .execution_panel import ExecutionPanel
from utils.i18n import I18n

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18n()
        self.setWindowTitle(self.i18n.tr("脚本管理器"))
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
        
        # 创建菜单栏
        self.create_menu_bar()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 语言菜单
        language_menu = menubar.addMenu(self.i18n.tr("语言"))
        
        chinese_action = QAction(self.i18n.tr("中文"), self)
        chinese_action.triggered.connect(lambda: self.change_language("zh-CN"))
        language_menu.addAction(chinese_action)
        
        english_action = QAction(self.i18n.tr("英文"), self)
        english_action.triggered.connect(lambda: self.change_language("en"))
        language_menu.addAction(english_action)
    
    def change_language(self, language: str):
        """更改语言设置"""
        self.i18n.change_language(language)
        QMessageBox.information(
            self,
            self.i18n.tr("提示"),
            self.i18n.tr("语言设置将在重启应用后生效")
        )
    
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 新建脚本
        new_action = QAction(self.i18n.tr("新建脚本"), self)
        new_action.setStatusTip(self.i18n.tr("创建新的Python脚本"))
        new_action.triggered.connect(self.new_script)
        toolbar.addAction(new_action)
        
        # 保存脚本
        save_action = QAction(self.i18n.tr("保存"), self)
        save_action.setStatusTip(self.i18n.tr("保存当前脚本"))
        save_action.triggered.connect(self.save_script)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 运行脚本
        run_action = QAction(self.i18n.tr("运行"), self)
        run_action.setStatusTip(self.i18n.tr("运行当前脚本"))
        run_action.triggered.connect(self.run_script)
        toolbar.addAction(run_action)
        
        # 删除脚本
        delete_action = QAction(self.i18n.tr("删除脚本"), self)
        delete_action.setStatusTip(self.i18n.tr("删除当前选中的脚本"))
        delete_action.triggered.connect(self.delete_script)
        toolbar.addAction(delete_action)
    
    def create_main_ui(self):
        # 创建水平分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建脚本列表
        self.script_list = QListWidget()
        self.script_list.itemClicked.connect(self.on_script_selected)
        
        # 创建脚本编辑器
        self.editor = ScriptEditorWidget()
        
        # 创建执行面板
        self.execution_panel = ExecutionPanel()
        
        # 添加到分割器
        splitter.addWidget(self.script_list)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.execution_panel)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 1)  # 脚本列表
        splitter.setStretchFactor(1, 4)  # 编辑器
        splitter.setStretchFactor(2, 2)  # 执行面板
        
        self.layout.addWidget(splitter)
    
    def new_script(self):
        name, ok = QInputDialog.getText(self, self.i18n.tr("新建脚本"), self.i18n.tr("请输入脚本名称："))
        if ok and name:
            try:
                db = next(get_db())
                script = Script(
                    name=name,
                    content="# Write your Python code here\n",
                    type="python"
                )
                db.add(script)
                db.commit()
                
                self.current_script_id = script.id
                self.editor.set_content(script.content)
                self.statusBar.showMessage(self.i18n.tr("创建脚本：") + name)
                self.load_scripts()
            except Exception as e:
                QMessageBox.critical(self, self.i18n.tr("错误"), self.i18n.tr("创建脚本失败：") + str(e))
    
    def save_script(self):
        if not self.current_script_id:
            QMessageBox.warning(self, self.i18n.tr("警告"), self.i18n.tr("请先创建或选择一个脚本"))
            return
        
        try:
            db = next(get_db())
            script = db.query(Script).get(self.current_script_id)
            if script:
                script.content = self.editor.get_content()
                db.commit()
                self.statusBar.showMessage(self.i18n.tr("脚本已保存"))
        except Exception as e:
            QMessageBox.critical(self, self.i18n.tr("错误"), self.i18n.tr(f"保存脚本失败：{str(e)}"))
    
    def run_script(self):
        if not self.current_script_id:
            QMessageBox.warning(self, self.i18n.tr("警告"), self.i18n.tr("请先创建或选择一个脚本"))
            return
        
        content = self.editor.get_content()
        self.execution_panel.run_script(content)
    
    def load_scripts(self):
        """加载所有脚本到列表中"""
        try:
            self.script_list.clear()
            db = next(get_db())
            scripts = db.query(Script).all()
            
            for script in scripts:
                item = QListWidgetItem(script.name)
                item.setData(Qt.ItemDataRole.UserRole, script.id)
                self.script_list.addItem(item)
                
        except Exception as e:
            QMessageBox.critical(self, self.i18n.tr("错误"), self.i18n.tr(f"加载脚本列表失败：{str(e)}"))
    
    def on_script_selected(self, item):
        """当选择脚本列表中的项目时触发"""
        script_id = item.data(Qt.ItemDataRole.UserRole)
        try:
            db = next(get_db())
            script = db.query(Script).get(script_id)
            if script:
                self.current_script_id = script.id
                self.editor.set_content(script.content)
                self.statusBar.showMessage(self.i18n.tr("已加载脚本：") + script.name)
        except Exception as e:
            QMessageBox.critical(self, self.i18n.tr("错误"), self.i18n.tr("加载脚本失败：") + str(e))
    
    def delete_script(self):
        """删除当前选中的脚本"""
        if not self.current_script_id:
            QMessageBox.warning(self, self.i18n.tr("警告"), self.i18n.tr("请先选择一个脚本"))
            return
            
        reply = QMessageBox.question(self, self.i18n.tr("确认删除"), 
                                   self.i18n.tr("确定要删除这个脚本吗？此操作不可撤销。"),
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                db = next(get_db())
                script = db.query(Script).get(self.current_script_id)
                if script:
                    db.delete(script)
                    db.commit()
                    self.current_script_id = None
                    self.editor.set_content("")
                    self.load_scripts()  # 重新加载脚本列表
                    self.statusBar.showMessage(self.i18n.tr("脚本已删除"))
            except Exception as e:
                QMessageBox.critical(self, self.i18n.tr("错误"), self.i18n.tr(f"删除脚本失败：{str(e)}"))